import struct

from ...client import ENCODING
from ... import Command
from ...formats.result_format_and_description import ResultFormatAndDescription


class GetPeakMarkerValue(Command):
	def __init__(self, window_name, display_zone_type='', marker_number='', get_details='1'):
		super().__init__(name=None,
		                 parameters=[window_name, str(display_zone_type), str(marker_number), str(get_details)])

		self.window_name = window_name
		self.display_zone_type = display_zone_type
		self.marker_number = marker_number
		self.get_details = str(get_details)

		self.value = None

		self.marker_number = None
		self.trace = None  # 0 = all traces, 1 = active trace, 2 = specific trace describe by result description below
		self.absolute_threshold = None
		self.ignore_under_threshold = None
		self.number_of_marker = None
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
			self.absolute_threshold = struct.unpack('f', response[0:4])[0]
			self.value.append(self.absolute_threshold)

			self.ignore_under_threshold = struct.unpack('f', response[4:8])[0]
			self.value.append(self.ignore_under_threshold)

			response = response[8:]

		self.number_of_marker = struct.unpack('I', response[0:4])[0]
		self.value.append(self.number_of_marker)
		response = response[4:]

		self.number_of_trace = struct.unpack('I', response[0:4])[0]
		self.value.append(self.number_of_trace)
		response = response[4:]

		list_marker_description = []

		contents_splitted = response.split(b'-')
		# Fix issue if "-" in the input name (e.g. "Input-1"), because it's used as a separator for this command
		new_contents_splitted = []
		for content in contents_splitted:
			test_pre_parse = self.pre_parse_response_marker(content)
			# If result False, then we need to concatenate the previous content with the current content
			if test_pre_parse:
				new_contents_splitted.append(content)
			else:
				new_contents_splitted[-1] = b'-'.join([new_contents_splitted[-1], content])

		for content in new_contents_splitted:
			current_marker_description = []

			if self.get_details == '1':
				current = self.parse_response_marker(content)
				current.window_name = self.window_name
				current.display_zone_type = self.display_zone_type

				if len(content[14:].split(b'\0')) > 1 and current.reference_channel_number != 0:
					current.input_name_reference_channel_number = str(content[14:].split(b'\0')[1].decode(ENCODING))
					content = content[14:].split(b'\0', 2)[2]
				else:
					current.input_name_reference_channel_number = ''
					content = content[14:].split(b'\0', 1)[1]

				current_marker_description.append(current)

			number_peak = struct.unpack('I', content[0:4])[0]
			current_marker_description.append(number_peak)

			list_couple = []
			for i in range(number_peak):
				# List of couple of float (x, y)
				peak = struct.unpack('ff', content[4 + 8 * i:12 + 8 * i])
				list_couple.append(peak)

			current_marker_description.append(list_couple)

			content = content[4 + 8 * number_peak:]

			list_marker_description.append(current_marker_description)

		self.value.append(list_marker_description)

	@staticmethod
	def parse_response_marker(contents):
		result_format_and_description = ResultFormatAndDescription().from_bytes(contents=contents)
		return result_format_and_description

	@staticmethod
	def pre_parse_response_marker(contents):
		"""
		Pre-parse the response to get the list of result format and description and check if error
		"""
		try:
			test = ResultFormatAndDescription().from_bytes(contents=contents)
			if test.input_name is not None and test.input_name != '':
				return True
			else:
				return False
		except Exception:
			return False

		return True
