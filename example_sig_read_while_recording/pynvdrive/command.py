from .client import NVDriveCommandError, NVDriveCommandParsing
from .client import ENCODING, ENCODING_MBCS


def split_response(response, separator=b'\0'):
	"""
	Split the response into a list of strings.
	It also removes the last empty string.
	:param response: The response to split.
	"""
	contents = response.split(separator)
	if contents[-1] == b'':
		contents = contents[:-1]
	return contents


class Command:
	"""A NVDrive command"""

	def __init__(self, name=None, parameters=None):
		if parameters is None:
			parameters = []
		if name is None:
			self.name = self.__class__.__name__
		else:
			self.name = name
		if isinstance(parameters, str):
			self.parameters = [parameters]
		else:
			self.parameters = parameters
		self.error = None
		return

	def send(self, client):
		return client.send_command(self)

	def parse_response(self, response):
		"""
		Parse the response. May raise ParseError.
		:param response: bytes to parse
		:return: None
		"""
		raise NVDriveCommandParsing()

	def parse_error(self, error):
		"""
		Parse the response. May raise ParseError.
		:param error: The error code returned by the server.
		:return: None
		"""
		e = NVDriveCommandError()
		e.error = error
		self.error = error
		raise e

	@staticmethod
	def parse_response_string(contents):
		"""
		Parse the response. May raise ParseError.
		:param contents: bytes to parse
		:return: None
		"""
		# Try in standard encoding, if failed then mbcs
		if contents.endswith(b'\0'):
			contents = contents[:-1]
		try:
			return contents.decode(ENCODING)
		except UnicodeDecodeError:
			return contents.decode(ENCODING_MBCS)

	@staticmethod
	def parse_response_list_string(contents):
		# contents = split_response(response=contents)
		contents = contents.split(b'\0')
		try:
			contents = [x.decode(ENCODING) for x in contents[:-1]]
		except Exception:
			contents = [x.decode(ENCODING_MBCS) for x in contents[:-1]]
		return contents


class CommandAction(Command):
	"""
	This class represent an action command: action that does not return anything Classes
	inherited from this class must be named as the NVDCommand (see run method)
	"""
	ACTION_NOT_RUN = 'not_run'
	ACTION_SUCCESS = 'success'
	ACTION_FAILURE = 'failure'

	def __init__(self, name=None, parameters=None):
		super().__init__(name, parameters)
		self.action_result = CommandAction.ACTION_NOT_RUN
		return

	def parse_response(self, response):
		self.action_result = CommandAction.ACTION_SUCCESS
		return

	def parse_error(self, error):
		self.action_result = CommandAction.ACTION_FAILURE
		super().parse_error(error)
		return

	@property
	def success(self):
		return self.action_result == CommandAction.ACTION_SUCCESS

	@property
	def failed(self):
		return self.action_result == CommandAction.ACTION_FAILURE
