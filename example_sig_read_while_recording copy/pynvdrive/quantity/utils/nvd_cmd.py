from ...command import Command
import struct
from pynvdrive import ENCODING


class GetMagnitudeList(Command):
	def __init__(self):
		super().__init__(name=None, parameters=[])
		self.value = None
		return

	def parse_response(self, response):
		try:
			_, _ = response.split(b'\0', 1)
		except Exception:
			raise NotImplementedError('No window displayed into chosen layout')

		self.value = self.parse_response_list_string(response)
		

class GetUnitList(Command):
	def __init__(self, magnitude_name):
		super().__init__(name=None, parameters=[magnitude_name])
		self.value = None
		return

	def parse_response(self, response):
		try:
			_, _ = response.split(b'\0', 1)
		except Exception:
			raise NotImplementedError('No window displayed into chosen layout')

		self.value = self.parse_response_list_string(response)


class GetUnitInfo(Command):
	def __init__(self, magnitude_name, unit_name):
		super().__init__(name=None, parameters=[magnitude_name, unit_name])
		self.value = None

		self.coeffA = None
		self.coeffB = None
		self.userunit_label = None
		self.userunit_name = unit_name
		self.si_unit = None

		return

	def parse_response(self, response):
		contents = response.split(b'\0')

		self.si_unit = self.parse_response_string(contents=contents[4])

		temp = response[:-17]
		temp = temp.split(b'\0')
		self.userunit_label = self.parse_response_string(contents=temp[-1])

		self.coeffA = struct.unpack('f', response[-16:-12])[0]
		self.coeffB = struct.unpack('f', response[-12:-8])[0]


class GetMagnitudeInfo(Command):
	def __init__(self, magnitude_key):
		super().__init__(name=None, parameters=[magnitude_key])
		self.value = None
		self.magnitude_name = None
		self.unit_name = None
		self.unit_label = None
		return

	def parse_response(self, response):
		try:
			_, _ = response.split(b'\0', 1)
		except Exception:
			raise NotImplementedError('No window displayed into chosen layout')

		self.value = self.parse_response_list_string(response)

		self.magnitude_name = self.value[0]
		self.unit_name = self.value[1]
		self.unit_label = self.value[2]
