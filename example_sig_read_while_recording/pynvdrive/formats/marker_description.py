import struct
from .result_format_and_description import ResultFormatAndDescription
from enum import Enum

# DisplayZoneType
# 0	Default display zone	Octave – Time – Profile
# 1	Imaginary part display zone	Spectral – CBT – 2D Waterfall
# 2	Real part display zone	Spectral – CBT – 2D Waterfall
# 3	Phase display zone	Spectral – CBT – 2D Waterfall
# 4	Module display zone		Spectral – CBT – 2D Waterfall
# 5	YZ section zone	3D waterfall
# 6	XY section zone	3D waterfall
# 7	Order section zone	3D waterfall
# 8	3D zone	3D waterfall (warning: this display zone can not contain markers)


class MarkerType(Enum):
	Free = 0
	Sideband = 1
	Harmonics = 2
	Peak = 3
	Max = 4
	Powerband = 5
	Record = 6
	NthOctave = 7
	Period = 8
	Kinematic = 9

	@classmethod
	def from_int(cls, value):
		return cls(value)


class MarkerDescription:
	"""
	Marker description as described in NVDrive documentation
	"""

	def __init__(self, marker_type=None, marker_number=None, location=None, result_format_and_description=None,
	             layout_name=None, window_name=None, display_zone_type=None, marker_position=None, marker_name=None,
	             interpolation_type=None):
		self._marker_type = marker_type
		self._marker_number = marker_number
		self._location = location  # 0 if all traces, 1 if active trace, 2 if specific trace then ResultsFormatsAndDescription
		self._result_format_and_description = result_format_and_description

		# Not in the documentation
		self.layout_name = layout_name

		# From GetMarkerList
		self.window_name = window_name
		self.display_zone_type = display_zone_type

		# From GetFreeMarkerParameters
		self.marker_position = marker_position
		self.marker_name = marker_name
		self.interpolation_type = interpolation_type

	@property
	def marker_type(self):
		return self._marker_type

	@property
	def marker_number(self):
		return self._marker_number

	@property
	def location(self):
		return self._location

	@property
	def unit(self):
		if self._result_format_and_description is not None:
			return self._result_format_and_description.unit
		return None

	def set_unit(self, unit):
		if self._result_format_and_description is not None:
			self._result_format_and_description.set_unit(unit)

	@property
	def result_format_and_description(self):
		return self._result_format_and_description

	def set_result_format_and_description(self, result_format_and_description):
		self._result_format_and_description = result_format_and_description

	def set_location(self, location):
		self._location = location

	@classmethod
	def from_bytes(cls, contents):
		# Marker type
		marker_type = struct.unpack('H', contents[0:2])[0]
		# Marker number
		marker_number = struct.unpack('I', contents[2:6])[0]
		# Location
		location = struct.unpack('H', contents[6:8])[0]

		if location == 2:
			result_format_and_description = ResultFormatAndDescription.from_bytes(contents[8:])
		else:
			result_format_and_description = None

		return cls(marker_type=marker_type, marker_number=marker_number, location=location,
		           result_format_and_description=result_format_and_description)

	def to_dict(self):
		my_dict = {'marker_type': self._marker_type, 'marker_number': self._marker_number, 'location': self._location}
		if self.layout_name is not None:
			my_dict['layout_name'] = self.layout_name
		if self.window_name is not None:
			my_dict['window_name'] = self.window_name
		if self.display_zone_type is not None:
			my_dict['display_zone_type'] = self.display_zone_type
		if self.marker_position is not None:
			my_dict['marker_position'] = self.marker_position
		if self.marker_name is not None:
			my_dict['marker_name'] = self.marker_name
		if self.interpolation_type is not None:
			my_dict['interpolation_type'] = self.interpolation_type
		if self._result_format_and_description is not None:
			my_dict['result_format_and_description'] = self._result_format_and_description.to_dict()
		return my_dict

	@classmethod
	def from_dict(cls, my_dict):
		marker_type = my_dict.get('marker_type')
		marker_number = my_dict.get('marker_number')
		location = my_dict.get('location')

		layout_name = my_dict.get('layout_name', None)
		window_name = my_dict.get('window_name', None)
		display_zone_type = my_dict.get('display_zone_type', None)
		marker_position = my_dict.get('marker_position', None)
		marker_name = my_dict.get('marker_name', None)
		interpolation_type = my_dict.get('interpolation_type', None)

		result_format_and_description = my_dict.get('result_format_and_description')
		if result_format_and_description is not None:
			result_format_and_description = ResultFormatAndDescription.from_dict(result_format_and_description)
		return cls(marker_type=marker_type, marker_number=marker_number, location=location,
		           result_format_and_description=result_format_and_description, layout_name=layout_name,
		           window_name=window_name, display_zone_type=display_zone_type, marker_position=marker_position,
		           marker_name=marker_name, interpolation_type=interpolation_type)

	def copy(self):
		return MarkerDescription.from_dict(self.to_dict())
