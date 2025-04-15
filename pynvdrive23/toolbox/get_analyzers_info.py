import pynvdrive
from ..commands.analyzers import GetAnalyzersBatteryStatus, GetAnalyzersCount, GetAnalyzersIpAddress, GetDiskInfo, GetNVGateInfo
from enum import Enum
from copy import copy


class DiskInfo:
	def __init__(self, hard_size=None, hard_free=None, local_size=None, local_free=None, disk_serial_number=None,
	             disk_model_name=None):
		self.hard_size = hard_size
		self.hard_free = hard_free
		self.local_size = local_size
		self.local_free = local_free
		self.disk_serial_number = disk_serial_number
		self.disk_model_name = disk_model_name

	def to_dict(self):
		return {'hard_size': self.hard_size, 'hard_free': self.hard_free, 'local_size': self.local_size,
		        'local_free': self.local_free, 'disk_serial_number': self.disk_serial_number,
		        'disk_model_name': self.disk_model_name}

	@classmethod
	def from_dict(cls, analyzer_dict):
		return cls(hard_size=analyzer_dict['hard_size'], hard_free=analyzer_dict['hard_free'],
		           local_size=analyzer_dict['local_size'], local_free=analyzer_dict['local_free'],
		           disk_serial_number=analyzer_dict['disk_serial_number'], disk_model_name=analyzer_dict['disk_model_name'])


class AnalyzerInfo:
	def __init__(self, type, serial_number, chain_position, ip_address=None, connected=None, battery_level=None, disk_info=None):
		self.type = type
		self.serial_number = serial_number
		self.chain_position = chain_position
		self.ip_address = ip_address
		self.connected = connected

		self.battery_level = battery_level
		self.disk_info: DiskInfo = disk_info

		self._is_charging = None
		self._last_battery_level = None

	def update(self, analyzer_info):
		analyzer_info = copy(analyzer_info)
		self.type = analyzer_info.type
		self.serial_number = analyzer_info.serial_number
		self.chain_position = analyzer_info.chain_position
		self.ip_address = analyzer_info.ip_address
		self.connected = analyzer_info.connected

		self.battery_level = analyzer_info.battery_level
		self.disk_info: DiskInfo = analyzer_info.disk_info

		# Check if the battery is charging or not
		if self._last_battery_level is None:
			self._last_battery_level = self.battery_level
		else:
			if self.battery_level > self._last_battery_level:
				self._is_charging = True
			elif self.battery_level < self._last_battery_level:
				self._is_charging = False
			self._last_battery_level = self.battery_level

	def is_plugged(self):
		if self._is_charging is None:
			return True
		else:
			return self._is_charging

	def is_daq(self):
		if self.type.upper() in ('O4'):
			return True
		else:
			return False

	def to_dict(self):
		return {'type': self.type, 'serial_number': self.serial_number, 'chain_position': self.chain_position,
		        'ip_address': self.ip_address, 'connected': self.connected, 'battery_level': self.battery_level,
		        'disk_info': self.disk_info.to_dict()}

	@classmethod
	def from_dict(cls, analyzer_dict):
		return cls(type=analyzer_dict['type'], serial_number=analyzer_dict['serial_number'],
		           chain_position=analyzer_dict['chain_position'], ip_address=analyzer_dict['ip_address'],
		           connected=analyzer_dict['connected'], battery_level=analyzer_dict['battery_level'],
		           disk_info=DiskInfo.from_dict(analyzer_dict['disk_info']))


def get_analyzers_info(client=None):
	"""
	Retrieve informations from analyzers currently running with NVGate
	"""
	if client is None:
		client = pynvdrive.Client()
		client.connect()
	else:
		client.connect()

	if not client.is_connected():
		return []

	list_analyzers_info = []
	analyzer_count = None

	# Get number of analyzers
	try:
		analyzers_count = GetAnalyzersCount()
		client.send_command(analyzers_count)
		analyzer_count = analyzers_count.value
	except pynvdrive.NVDriveCommandError as e:
		pass
	except pynvdrive.NVDriveConnectionError:
		print('error NVDrive is not connected (GetAnalyzersCount)')
		return None

	if analyzer_count is None:
		return None

	# print('Analyzers count: {}'.format(analyzer_count))

	for idx_analyzer in range(1, analyzer_count + 1):
		# Get GetNVGateInfo
		try:
			nvgate_info = GetNVGateInfo(analyzer_index=idx_analyzer)
			client.send_command(nvgate_info)
			# print("GetNVGateInfo: {}".format(nvgate_info.value))
		except pynvdrive.NVDriveCommandError as e:
			print('error GetNVGateInfo ', e.error)
		except pynvdrive.NVDriveConnectionError:
			return None

		# Get GetDiskInfo spaces of analyzers
		try:
			disk_info = GetDiskInfo(analyzer_index=idx_analyzer)
			client.send_command(disk_info)
			# print("GetDiskInfo: {}".format(disk_info.value))
		except pynvdrive.NVDriveCommandError as e:
			print("Error GetDiskInfo : {}".format(e))
		except pynvdrive.NVDriveConnectionError:
			return None

		# Get IP addresses of analyzers
		try:
			analyzers_ip_addresses = GetAnalyzersIpAddress()
			client.send_command(analyzers_ip_addresses)
			# print("GetAnalyzersIpAddress: {}".format(analyzers_ip_addresses.value))
		except pynvdrive.NVDriveCommandError as e:
			print("Error GetAnalyzersIpAddress : {}".format(e))
		except pynvdrive.NVDriveConnectionError:
			return None

		# Get IP addresses of analyzers
		try:
			analyzers_battery = GetAnalyzersBatteryStatus()
			client.send_command(analyzers_battery)
		except pynvdrive.NVDriveCommandError as e:
			print("Error GetAnalyzersBatteryStatus : {}".format(e))
		except pynvdrive.NVDriveConnectionError:
			return None

		if len(analyzers_ip_addresses.value) >= idx_analyzer:
			analyzer_ip_address = analyzers_ip_addresses.value[idx_analyzer - 1]
		else:
			analyzer_ip_address = None

		analyzer_type = nvgate_info.hard_type
		if 'O4' in analyzer_type.upper():
			analyzer_type = 'O4'

		battery_value = 100
		try:
			battery_value = analyzers_battery.value[idx_analyzer - 1]
		except Exception:
			pass

		analyzer_info = AnalyzerInfo(type=analyzer_type, serial_number=nvgate_info.serial_number,
		                             chain_position=idx_analyzer, ip_address=analyzer_ip_address,
		                             battery_level=battery_value,
		                             disk_info=DiskInfo(hard_size=disk_info.hard_size, hard_free=disk_info.hard_free,
		                                                local_size=disk_info.local_size, local_free=disk_info.local_free,
		                                                disk_serial_number=disk_info.disk_serial_number,
		                                                disk_model_name=disk_info.disk_model_name))
		list_analyzers_info.append(analyzer_info)

	return list_analyzers_info
