import pynvdrive
from .marker_description import MarkerDescription, MarkerType
from ..commands.marker import GetFreeMarkerValue
from ..quantity.quantity_provider import QuantityProvider
import json
from datetime import datetime
from .result_format_and_description import ResultFormatAndDescription
from .process import processes_to_tcp
from pynvdrive.formats.utils.octave import OCTAVE_BAND_VALUES
from ..quantity.unit import Unit


class Marker:
	"""
    This class is a generic class for a marker.
    """

	def __init__(self, marker_description: MarkerDescription, quantity_provider: QuantityProvider = None):

		if quantity_provider:
			self.quantity_provider = quantity_provider
		else:
			self.quantity_provider = QuantityProvider()

		self.marker_description = marker_description

		self._value = None

	def get_marker_type(self):
		"""
		Get the type of the marker

		:return: str
		"""
		return self.marker_description.marker_type

	def get_marker_number(self):
		"""
		Get the marker number

		"""
		return self.marker_description.marker_number

	def get_marker_location(self):
		"""
		Get the location of the marker

		:return: Location
		"""
		return self.marker_description.location

	def get_marker_window_name(self):
		return self.marker_description.window_name

	def get_marker_display_zone(self):
		"""
		Get the marker display zone

		"""
		return self.marker_description.display_zone_type

	def get_marker_position(self):
		"""
		Get the position of the marker

		"""
		return self.marker_description.marker_position

	def get_marker_name(self):
		"""
		Get the name of the marker

		"""
		return self.marker_description.marker_name

	def get_marker_description(self):
		return self.marker_description

	def get_result_format_and_description(self) -> ResultFormatAndDescription:
		"""
		Get the result format and description
		"""
		return self.marker_description.result_format_and_description

	def get_unit(self, update=False, client=None) -> Unit:
		"""
		Get the unit of the result
		"""
		if update:
			self.update_unit(client=client)

		return self.marker_description.unit

	def update_unit(self, client=None):
		"""
		Update the unit of the result
		"""
		if self.marker_description.result_format_and_description:
			self.marker_description.result_format_and_description.update_unit(client=client,
		                                                                  quantity_provider=self.quantity_provider)

	def get_value(self, update=False, client=None):
		"""
		Get the value of the result

		"""
		if update:
			self.update_value(client=client)

		return self._value

	def update_value(self, client=None):
		"""
		Update the value of the result
		"""
		if MarkerType(self.marker_description.marker_type) == MarkerType.Free:
			try:
				cmd = GetFreeMarkerValue(window_name=self.marker_description.window_name,
				                         display_zone_type=self.marker_description.display_zone_type,
				                         marker_number=self.marker_description.marker_number)
				client.send_command(cmd)
				self._value = cmd.list_value
			except pynvdrive.NVDriveCommandError as e:
				print('error GetFreeMarkerValue ', e.error)

	def json_default(self, value):
		if hasattr(value, '__dict__'):
			return value.__dict__
		if isinstance(value, datetime):
			return dict(year=value.year, month=value.month, day=value.day)
		else:
			return value.__dict__

	def to_json(self):
		return json.dumps(self, default=self.json_default, sort_keys=True, indent=4, ensure_ascii=False)

	def to_dict(self):
		dict = {}
		dict['marker_description'] = self.marker_description.to_dict()
		dict['value'] = self._value
		return dict

	def from_dict(self, result_dict):
		"""
        Convert a result from a dict to a result

        """
		return self


class ResultException(Exception):
	pass


class ResultTypeError(ResultException):
	"""
    Result type error
    """
	pass


class ResultToBinaryError(ResultException):
	"""
    Error while converting to binary
    """
	pass


class ResultBlockMissing(ResultException):
	"""
    Error if a block is missing into result
    """
	pass


class TCPProcessIDError(ResultException):
	"""
    Error if process_id is not found in mapping
    """
	pass
