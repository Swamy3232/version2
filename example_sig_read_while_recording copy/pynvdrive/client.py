import socket

from .quoter import quote_escape_list, quote_escape_byte, convert_parameters_none

ENCODING = 'utf-8-sig'
ENCODING_MBCS = 'mbcs'


class NVDriveException(Exception):
	pass


class NVDriveCommandError(NVDriveException):
	"""NVDrive error (server returned a properly formatted error)"""
	pass


class NVDriveCommandParsing(NVDriveException):
	"""Parsing of the command response failed"""
	pass


class NVDriveProtocolError(NVDriveException):
	"""Protocol error (server and client could not understand each other)"""
	pass


class NVDriveConnectionError(NVDriveException):
	"""Connection error (could not connect to server)"""
	pass


_BOM = b'\xEF\xBB\xBF'


class Client:
	"""
	This class is the entrypoint for NVDrive commands, it connects to NVGate
	and manage commands sent and keep information about it.

	Example::

		client = NVDClient()
		client.connect()
		cmd = Run()
		client.run(cmd)
		client.disconnect()

	"""

	def __init__(self, host_port=('127.0.0.1', 3000), compatibility_level='V14.00', enable_utf8=True):
		self.socket = None
		self._renew_socket()
		self.host_port = host_port
		self.compatibility_level = compatibility_level

		self._enable_utf8 = enable_utf8
		self._is_utf8_enabled = None
		return

	def __enter__(self):
		self.connect()
		return self

	def __exit__(self, exc_type, exc_val, exc_tb):
		self.disconnect()
		return

	def _renew_socket(self):
		"""Renew socket connection"""
		if self.socket:
			self.socket.close()
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.reader = None
		return

	def connect(self):
		if self.is_connected():
			return True
		else:
			try:
				self._renew_socket()
				self.socket.connect(self.host_port)
				self.reader = self.socket.makefile(mode='rb')
				self.enable_utf8()
				return True
			except socket.error as e:
				return False

	def disconnect(self):
		if self.is_connected():
			self.reader.close()
			self.socket.close()
		return

	def is_connected(self):
		"""Check if client is connected
		:return: True if connected, False otherwise
		"""
		try:
			self.socket.sendall(b'0\n')
			try:
				header_bytes = self.receive_header()
			except Exception:
				return False
			if header_bytes.startswith(b'1'):
				return True
			elif header_bytes.startswith(b'0'):
				response_byte_count = int(header_bytes)
				if response_byte_count > 0:
					self.receive_response(response_byte_count)
				return False
		except socket.error as e:
			return False

	def send_command(self, command):
		"""
		Send a command
		:param byte command: Command to send
		:return: sent success
		"""
		command.compatibility_level = self.compatibility_level
		command_bytes = self.get_command_bytes(command)
		try:
			self.socket.sendall(command_bytes)
		except Exception:
			print('NVDrive connection error (send_command)')
			# raise NVDriveConnectionError('NVDrive connection error')
			return False
		else:
			try:
				header_bytes = self.receive_header()
			except Exception:
				print('NVDrive connection error (receive_header)')
				# raise NVDriveConnectionError('NVDrive connection error')
				return False
			else:
				if header_bytes.startswith(b'1') or header_bytes.startswith(b'2'):
					# Server returned an NVDrive-encoded error code
					command.parse_error(header_bytes)
				elif header_bytes.startswith(b'0'):
					response_byte_count = int(header_bytes)
					if response_byte_count < 0:
						raise NVDriveProtocolError('unexpected reponse size ' + str(header_bytes))
					response_bytes = self.receive_response(response_byte_count)
					command.parse_response(response_bytes)
				else:
					raise NVDriveProtocolError('expected header starting with 012, received ' + str(header_bytes))
					return False
		return True

	def receive_header(self):
		"""Receive response header
		:return: Header bytes
		"""
		bytes = self.reader.read(10)
		if len(bytes) != 10:
			raise NVDriveProtocolError('invalid header size ' + str(len(bytes)))
		return bytes

	def receive_response(self, byte_count):
		"""Receive response contents
		:param byte_count: Contents length as defined in header
		:return: Contents bytes
		"""
		bytes = self.reader.read(byte_count)
		if len(bytes) != byte_count:
			raise NVDriveProtocolError('invalid response size ' + str(len(bytes)))
		return bytes

	@staticmethod
	def get_command_bytes(command):
		"""Convert command to bytes
		:param command: NVDrive command
		:type command: pynvdrive.command.Command class
		:return: Command bytes value
		"""
		name_bytes = command.name.encode('unicode-escape')
		type_byte = False
		if len(command.parameters) == 1:
			if isinstance(command.parameters[0], bytes):
				type_byte = True

		if command.name == 'GetResultEx':
			quoted = False
		else:
			quoted = True

		if 'TCPResultChannel' in command.name and command.name not in ["GetTCPResultChannelList", "RemoveTCPResultChannel"]:
			param_bytes = [command.parameters[0]]  # No escape bytes
		else:
			if type_byte:
				param_bytes = [quote_escape_byte(command.parameters[0])]
			else:
				param_bytes = quote_escape_list(command.parameters, quoted)

		eol = b'\n'

		if 'TCPResultChannel' in command.name and command.name not in ["GetTCPResultChannelList",
		                                                               "RemoveTCPResultChannel"]:  # No bom for CreateTCPResultChannel
			return name_bytes + b' '.join(param_bytes) + eol
		else:
			return _BOM + name_bytes + b' ' + b' '.join(param_bytes) + eol

	def enable_utf8(self):
		"""Enable UTF-8 encoding
		"""
		if self._enable_utf8 and not self._is_utf8_enabled:
			from .commands.configuration.enableutf8 import EnableUTF8
			try:
				self.send_command(EnableUTF8())
				self._is_utf8_enabled = True
			except Exception as e:
				pass
