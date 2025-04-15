"""
Define the record class.
"""

from .channel import Channel
from .measurement_exceptions import NVGateRecordException
from .nvg_signal_typedef import RecordMetadataStr, NvgsRecordMultiPartMode


class Record(object):
	"""
	Define the record class.
	"""

	def __init__(self, channels=[]):
		"""
		Define the record class.
		"""
		self._record_id = None

		self._metadata_dict = {}

		self._channels = []
		for channel in channels:
			self.add_channel(channel)

		self._record_idx = None  # Position in the measurement record list. [0 ... nb_records - 1]
		self._parent_measurement = None  # Associated parent measurement

		# Set the default part length to single part file
		self.set_part_length(NvgsRecordMultiPartMode.NvgsSinglePartFile)

	@property
	def record_id(self):
		"""
		Get the record id.

		:returns: the record id
		:rtype: int
		"""
		return self._metadata_dict.get(RecordMetadataStr.recordId.value, None)

	def set_record_id(self, record_id):
		"""
		Set the record id.
		"""
		self._metadata_dict[RecordMetadataStr.recordId.value] = record_id

	def set_record_idx(self, record_idx):
		"""
		Set the record idx, position in the measurement record list. [0 ... nb_records - 1]
		"""
		self._record_idx = record_idx

	def get_record_idx(self):
		"""
		Get the record idx, position in the measurement record list. [0 ... nb_records - 1]
		"""
		return self._record_idx

	def set_parent_measurement(self, measurement):
		"""
		Set the parent measurement.
		"""
		self._parent_measurement = measurement

	def get_parent_measurement(self):
		"""
		Get the parent measurement.
		"""
		return self._parent_measurement

	@property
	def abs_date(self):
		"""
		Get the abs date.
		"""
		return self._metadata_dict.get(RecordMetadataStr.absDate.value, None)

	@property
	def duration(self):
		"""
		Get the duration.
		"""
		return self._metadata_dict.get(RecordMetadataStr.duration.value, None)

	@property
	def rel_date(self):
		"""
		Get the rel date.
		"""
		return self._metadata_dict.get(RecordMetadataStr.relDate.value, None)

	@property
	def recording(self):
		"""
		Get the recording status.
		"""
		return self._metadata_dict.get(RecordMetadataStr.recording.value, None)

	def is_recording(self):
		"""
		Check if the record is recording.
		"""
		if self._metadata_dict.get(RecordMetadataStr.recording.value, None) == 1:
			return True
		else:
			return False

	def set_part_length(self, part_length: NvgsRecordMultiPartMode):
		"""
		Set the part length, part_length is store in seconds but set in NVGSRecordMultiPartMode.
		:param part_length: the part length
		:type part_length: NVGSRecordMultiPartMode
		"""
		self._metadata_dict[RecordMetadataStr.partLength.value] = part_length.get_time()

	@property
	def part_length(self):
		"""
		Get the part length.
		:return: the part length
		:rtype: float
		"""
		return self._metadata_dict.get(RecordMetadataStr.partLength.value, 0.0)

	def add_channel(self, channel: Channel):
		"""
		Add a channel to the record.
		"""
		channel.set_parent_record(self)
		self._channels.append(channel)

	def get_channels(self) -> list:
		"""
		Get the channels.
		"""
		return self._channels

	def get_channel(self, index) -> Channel:
		"""
		Get the channel at the index.

		:param index: index of the channel [1 ... nb_channels]
		:return: the channel
		:rtype: Channel
		"""
		real_index = index - 1  # cause index starts at 1
		if real_index < 0 or real_index >= len(self._channels):
			raise NVGateRecordException("Invalid channel index")
		return self._channels[index-1]

	def load_metadata_from_record_vect(self, record_vect: dict):
		"""
		Load the record from a record_vect.
		"""
		# Create or update the metadata dict
		self._metadata_dict.update(record_vect)

	def get_metadata_value(self, key) -> object:
		"""
		Get the metadata.

		:param key: The metadata key
		:type key: str
		:return: the metadata value
		:rtype: object
		"""
		return self._metadata_dict.get(key, None)

	def get_metadata_dict(self) -> dict:
		"""
		Get the metadata dict.
		"""
		return self._metadata_dict

	def get_max_sampling_rate(self):
		"""
		Get the max sampling rate.
		"""
		max_sampling_rate = 0
		for channel in self._channels:
			if channel.sampling > max_sampling_rate:
				max_sampling_rate = channel.sampling
		return max_sampling_rate

	def __repr__(self):
		"""
		Define the representation of the record.
		"""
		return "Record(record_id: {} abs_date: {} duration: {} rel_date: {}, part_length: {}, recording: {}, channels : {})".format(
			self.record_id, self.abs_date, self.duration, self.rel_date, self.part_length, self.recording, self._channels)
