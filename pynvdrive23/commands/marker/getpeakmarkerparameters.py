from ... import Command

import struct


class GetPeakMarkerParameters(Command):
	def __init__(self, window_name, marker_number, display_zone_type=''):
		super().__init__(name=None, parameters=[window_name, str(display_zone_type), str(marker_number)])
		self.value = None

		self.threshold = None
		self.absolute_threshold = None
		self.maximum_number_of_peaks_per_marker = None
		self.interpolation_type = None
		self.sort_by_frequency = None
		self.display_damping_ratio = None
		return

	def parse_response(self, response):
		self.value = []

		if len(response) >= 16:
			self.threshold = struct.unpack('f', response[0:4])[0]
			self.absolute_threshold = struct.unpack('f', response[4:8])[0]
			self.maximum_number_of_peaks_per_marker = struct.unpack('I', response[8:12])[0]
			self.interpolation_type = struct.unpack('I', response[12:16])[0]
			self.sort_by_frequency = struct.unpack('?', response[16:17])[0]

		if len(response) > 17:
			self.display_damping_ratio = struct.unpack('?', response[17:18])[0]

		self.value = [self.threshold, self.absolute_threshold, self.maximum_number_of_peaks_per_marker,
		              self.interpolation_type, self.sort_by_frequency, self.display_damping_ratio]
