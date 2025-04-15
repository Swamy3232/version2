import struct

from ... import Command
from ...formats.result_format_and_description import ResultFormatAndDescription


class GetFreeMarkerValue(Command):
	def __init__(self, window_name, display_zone_type='', marker_number='', get_details='1'):
		super().__init__(name=None,
		                 parameters=[window_name, str(display_zone_type), str(marker_number), str(get_details)])

		self.get_details = str(get_details)

		self.value = None

		self.marker_number = None
		self.trace = None
		self.marker_label = None
		self.position_x = None
		self.number_of_trace = None
		self.list_result_format_and_description = []
		self.list_value = []
		return

	def parse_response(self, response):
		self.value = []
		self.marker_number = struct.unpack('I', response[0:4])[0]
		self.value.append(self.marker_number)

		self.trace = struct.unpack('H', response[4:6])[0]
		self.value.append(self.trace)

		response = response[6:]

		# Getting details if asked
		if self.get_details == '1':
			response = response.split(b'\0', 1)

			self.marker_label = self.parse_response_string(response[0])
			self.value.append(self.marker_label)

			response = response[1]

			self.position_x = struct.unpack('f', response[0:4])[0]
			self.value.append(self.position_x)

			response = response[4:]

		self.number_of_trace = struct.unpack('I', response[0:4])[0]
		self.value.append(self.number_of_trace)
		response = response[4:]

		list_response = response.split(b'\n')
		if len(list_response) <= 0:
			return
		elif len(list_response) == 1 and (list_response[0] == b'' or list_response[0] == b'\0'):
			return
		elif len(list_response) > 1 and (list_response[0] == b'' or list_response[0] == b'\0'):
			list_response = list_response[1:]

		if len(list_response) != self.number_of_trace:
			raise ValueError('Number of trace is not correct')

		for response in list_response:
			# Getting details if asked
			if self.get_details == '1':
				response = b'\n' + response

				result_format_and_description = ResultFormatAndDescription().from_bytes(contents=response)
				response = response[14:].split(b'\0', 1)[1]

				if result_format_and_description.reference_channel_number != 0:
					response = response.split(b'\0', 1)[1]

			positionY = struct.unpack('f', response[0:4])[0]
			self.list_value.append(positionY)
			response = response[4:]

