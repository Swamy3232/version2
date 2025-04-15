"""
Define the channel class.
"""
from .nvg_signal_typedef import (OSFFChannelType as ChannelType, ChannelMetadataStr_Predef, get_input_type_int_from_str,
                                 ReadingStatus)

BLOCK_SIZE = 4096  # 4096 samples per block to read/write by default


class Channel(object):
	"""
	This class represents a NVGate channels/track
	"""

	def __init__(self, name, sampling, type=ChannelType.Dynamic):
		self._metadata_dict = {}
		self._channel_id = None

		# Minimum attributes for a channel
		self.set_type(type)

		self._metadata_dict[ChannelMetadataStr_Predef.CHANNEL_NAME.value] = name
		self._metadata_dict[ChannelMetadataStr_Predef.CHANNEL_SAMPLING_RATE.value] = sampling

		self._data = None

		self._data_block_generator = None
		self._generator_env = None

		self._parent_record = None  # Associated parent record

	def set_parent_record(self, record):
		"""
		Set the parent record.
		"""
		self._parent_record = record

	def get_parent_record(self):
		"""
		Get the parent record.
		"""
		return self._parent_record

	@property
	def name(self):
		"""
		Get the name of the channel.
		"""
		return self._metadata_dict.get(ChannelMetadataStr_Predef.CHANNEL_NAME.value, None)

	@property
	def sampling(self):
		"""
		Get the sampling of the channel.
		"""
		return self._metadata_dict.get(ChannelMetadataStr_Predef.CHANNEL_SAMPLING_RATE.value, None)

	@property
	def type(self):
		"""
		Get the type of the channel.

		:rtype: ChannelType
		"""
		return self._type

	def set_type(self, channel_type: ChannelType):
		"""
		Set the type of the channel.

		:param channel_type: the channel type
		:type channel_type: ChannelType
		"""
		self._type = channel_type
		self._metadata_dict[ChannelMetadataStr_Predef.CHANNEL_TYPE.value] = str(channel_type)

	@property
	def coupling(self):
		"""
		Get the coupling of the channel.
		"""
		return self._metadata_dict.get(ChannelMetadataStr_Predef.CHANNEL_COUPLING.value, None)

	def set_coupling(self, coupling):
		"""
		Set the coupling of the channel.
		"""
		self._metadata_dict[ChannelMetadataStr_Predef.CHANNEL_COUPLING.value] = coupling

	@property
	def physical_quantity(self):
		"""
		Get the physical quantity of the channel.
		"""
		return self._metadata_dict.get(ChannelMetadataStr_Predef.CHANNEL_PHYSICAL_QUANTITY.value, None)

	def set_magnitude(self, magnitude):
		"""
		Set the magnitude of the channel.
		"""
		self._metadata_dict[ChannelMetadataStr_Predef.CHANNEL_PHYSICAL_QUANTITY.value] = magnitude

	@property
	def unit(self):
		"""
		Get the unit of the channel.
		"""
		return self._metadata_dict.get(ChannelMetadataStr_Predef.CHANNEL_UNIT.value, None)

	@property
	def frequency(self):
		"""
		Get the frequency of the channel.
		"""
		return self._metadata_dict.get(ChannelMetadataStr_Predef.CHANNEL_SAMPLING_RATE.value, None)

	@property
	def range_peak(self):
		"""
		Get the range peak of the channel.
		"""
		return self._metadata_dict.get(ChannelMetadataStr_Predef.CHANNEL_RANGE_PEAK.value, None)

	def set_range_peak(self, range_peak):
		"""
		Set the range peak of the channel.
		"""
		self._metadata_dict[ChannelMetadataStr_Predef.CHANNEL_RANGE_PEAK.value] = range_peak

	@property
	def duration(self):
		"""
		Get the duration of the channel inside its record.
		"""
		return self._metadata_dict.get(ChannelMetadataStr_Predef.RECORD_DURATION.value, None)

	def set_duration(self, duration):
		"""
		Set the duration of the channel.
		"""
		self._metadata_dict[ChannelMetadataStr_Predef.RECORD_DURATION.value] = duration

	def get_type_int(self):
		"""
		Get the type of the channel as int. Used for NVGate setmetadata which required int as key.
		"""
		return int(self._type)

	def is_tach(self):
		"""
		Get if the channel is a tach channel.

		:rtype: bool
		"""
		return self._metadata_dict.get(ChannelMetadataStr_Predef.CHANNEL_IS_TACH.value, None)

	@property
	def channel_id(self):
		"""
		Get the channel id, channel index in the record. [1 ... nb_channels]
		"""
		return self._channel_id

	def set_channel_id(self, channel_id):
		"""
		Set the channel id.
		"""
		self._channel_id = channel_id

	def get_data(self):
		"""
		Get the data already read from the channel.

		:return: the data
		:rtype: list of float
		"""
		data = []
		for data_block in self.get_data_block(BLOCK_SIZE):
			data.extend(data_block)

		if not data:
			return None

		return data

	def get_data_block(self, block_size=BLOCK_SIZE):
		"""
		Get the data blocks already read from the channel.

		:return: the data blocks
		:rtype: list of list of float
		"""
		return self.get_data_block_generator(block_size=block_size)

	def get_data_block_generator(self, block_size=BLOCK_SIZE):
		"""
		Get the data block generator from the channel. Data already read from the channel.
		Note: This is a generator, so it can be used in a for loop.

		:param block_size: the block size
		:return: the data block generator
		:rtype: generator
		"""
		if self._data_block_generator is None:
			self._data_block_generator = self.base_data_generator
		return self._data_block_generator(block_size=block_size)

	def set_data_block_generator(self, data_block_generator):
		"""
		Set the data block generator for the channel.

		:param data_block_generator: the data block generator
		"""
		if data_block_generator is None:
			self._data_block_generator = self.base_data_generator
		self._data_block_generator = data_block_generator.__get__(self, Channel)

	def read_data_via_generator(self):
		"""
		Read the data blocks from the channel file directly. Using generator is more efficient.
		Note : this methods will not work for recording in progress, use measurement.read_data_block instead.
		:return: the data
		:rtype: list of float
		"""
		data = []
		for data_block in self.read_data_block_via_generator(BLOCK_SIZE):
			data.extend(data_block)

		if not data:
			return None

		return data

	def read_data_block_via_generator(self, block_size=BLOCK_SIZE):
		"""
		Read the data blocks from the channel file directly. Using generator, allows to read data block by block.
		Note : this methods will not work for recording in progress, use measurement.read_data_block instead.
		:return: the data blocks
		:rtype: list of list of float
		"""
		return self.base_data_generator(block_size=block_size, read_from_file=True)

	def base_data_generator(self, block_size=BLOCK_SIZE, read_from_file=False):
		"""
		This generator is the default data generator, it reads data of the channel and yield it by block.
		The generator will be used by the data_blocks method to write data in a signal file.
		
		:param block_size: the block size
		:type block_size: int
		:param read_from_file: if True, read data from file, else read from loaded data
		:type read_from_file: bool
		:return: the data block generator
		:rtype: generator
		"""
		if read_from_file:
			# TODO : improve and explicit usage + allow a reset of the generator for read_from_file
			if not self.get_measurement():
				return

			while True:
				data = self.read_data_block(block_size=block_size)

				# print('reading_status: {}'.format(reading_status))
				if not data:
					# reading_status = self.get_reading_status(channel_idx=self.channel_id)
					# print('reading_status: {}'.format(reading_status))
					# print('No more data to read')
					break
				yield data
		else:
			# Read from loaded data
			if self._data is None:
				return
			if (self.nb_samples % block_size) == 0:
				nb_blocks = self.nb_samples // block_size
			else:
				nb_blocks = (self.nb_samples // block_size) + 1
			for i in range(nb_blocks):
				begin = i * block_size
				end = (i + 1) * block_size
				data = self._data[begin:end]
				yield data

	# Same but not using generator, NVGS manage the position so a generator is not always needed
	def read_data(self):
		"""
		Read the data from the channel file directly.
		:return: the data
		:rtype: list of float
		"""
		data = []
		reading_status = ReadingStatus.RecordReading
		last_read_size = 1
		while (reading_status not in (ReadingStatus.MeasurementRead, ReadingStatus.RecordRead)) or (last_read_size > 0):
			read_data = self.read_data_block()
			last_read_size = len(read_data)
			data.extend(read_data)
			reading_status = self.get_reading_status()
		return data

	def read_data_block(self, block_size=BLOCK_SIZE):
		"""
		This method reads data from the channel and returns it in blocks.
		It is used by the `data_blocks` method to write data to a signal file.

		:param block_size: the block size
		:type block_size: int
		:return: the data block
		:rtype: list
		"""
		if not self.get_measurement():
			return None

		# We will use the measurement's `read_by_block` method
		record_idx = self.get_parent_record().get_record_idx()

		data_blocks = []

		data_blocks = self.get_measurement().read_signal_data_block(record_idx, channel_idx=self.channel_id,
		                                                            block_size=block_size)
		if not data_blocks:
			# reading_status = self.get_measurement().get_reading_status(channel_idx=self.channel_id)
			pass
			# print('No more data to read')

		return data_blocks

	# ------------------- Data block generator ------------------- #
	def get_generator_env(self):
		"""
		Get the generator env from the channel.

		:return: the generator env
		:rtype: dict
		"""
		return self._generator_env

	def set_generator_env(self, generator_env):
		"""
		Set the generator env from the channel.

		:param generator_env: the generator env
		"""
		self._generator_env = generator_env

	# ------------------- END Data block generator ------------------- #

	def get_reading_status(self):
		"""
		Get the reading status of the channel.

		:return: the reading status
		:rtype: ReadingStatus
		"""
		if self.get_measurement() is None:
			return None
		return self.get_measurement().get_reading_status(channel_idx=self.channel_id)

	@property
	def nb_samples(self):
		"""
		Get the nb_samples of the data from the channel.

		:return: the length of the data
		:rtype: int
		"""
		sampling_rate = self.sampling
		duration = self.duration

		if sampling_rate is None or duration is None:
			return len(self._data)
		else:
			return int(sampling_rate * duration)

	def clear_data(self):
		"""
		Clear the data from the channel.
		"""
		self._data = []

	def set_data(self, data):
		"""
		Set the data from the channel.

		:param data: the data to set
		"""
		self._data = data

	def add_data(self, data):
		"""
		Add data to the channel.

		:param data: the data to add
		"""
		self._data.extend(data)

	def load_metadata_from_metadata_dict(self, metadata_dict):
		"""
		Update the metadata from a metadata dict.
		"""
		self._metadata_dict.update(metadata_dict)

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

		:return: the metadata dict but map some metadata value to string
		"""
		metadata_dict = {}
		for key, value in self._metadata_dict.items():
			if key == ChannelMetadataStr_Predef.CHANNEL_COUPLING.value:
				value = get_input_type_int_from_str(value)
			elif key == ChannelMetadataStr_Predef.CHANNEL_TYPE.value:
				# Associate it to according int
				value = self.get_type_int()
			elif key == ChannelMetadataStr_Predef.CHANNEL_FREQUENCY_CORR.value:
				value = None
			metadata_dict[key] = value

		return metadata_dict

	def get_measurement(self):
		"""
		Get the measurement from the channel.

		:return: the measurement
		:rtype: Measurement, None if no linked between channel and measurement
		"""
		if self.get_parent_record() is None:
			return None
		else:
			if self.get_parent_record().get_parent_measurement() is None:
				return None

		return self.get_parent_record().get_parent_measurement()

	def __repr__(self):
		return "Channel(name={}, sampling={}, type={})".format(self.name, self.sampling, self.type)
