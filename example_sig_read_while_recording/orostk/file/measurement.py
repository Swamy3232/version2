"""
Define the measurement class.
"""

import logging
import os.path
import datetime
import time
import typing

from ..utils.time_utils import datetime_to_windows_time_int, date_string_to_datetime

from .nvg_signal_typedef import (MeasurementMetadataStr_Predef, is_measurement_metadata_valid,
                                 NvgsRecordMultiPartMode, ReadingStatus)
from .record import Record, RecordMetadataStr
from .channel import Channel, BLOCK_SIZE, ChannelMetadataStr_Predef, ChannelType

# Import Cython modules
from . import nvg_signal
from .measurement_exceptions import *


class Measurement(object):
	"""
	This class implements the Toolkit NVGS management, implementing the NVGateSignal library.

	You can either use the NVGS library on your own (nvg_signal.pyd), documentation is available in the
	nvg_signal.pyi/nvg_signal_export.pyd and it implements all NVGateSignal functions.

	Or you can use the Measurement class to manage the NVGS library, some methods are implemented to help you, but some are
	missing, you can use the nvg_signal.pyd directly to implement them.

	Note :
		- Read/Write/Remove/Erase methods call NVGS methods and apply the changes to the measurement object directly
		- Get/Set methods only apply the changes to the measurement object, you have to call the write methods to apply
			the changes to the measurement. (get_data get data from the measurement object, read_data read data from the
			measurement file, meaning you have to read the data before getting it)

	Examples
	----------
	Example read measurement, including whole data::

		measurement = Measurement.read_measurement("C:/path/to/measurement", read_data=True)
		channel_1 = measurement.get_record(0).get_channel(1)
		data = channel_1.get_data()
		measurement_metadata = measurement.get_metadata_dict()
		channel_metadata = channel_1.get_metadata_dict()
		measurement.close_measurements()


	Example read measurement, data later::

		measurement = Measurement.read_measurement("C:/path/to/measurement", read_data=False)
		measurement_metadata = measurement.get_metadata_dict()
		measurement.read_signal_data()  # Read signal data here
		measurement.close_measurements()

	Example read measurement, data later, block by block::

		# It allows to read new signal because it read it directly from signal file not in measurement cached data
		measurement = Measurement.read_measurement("C:/path/to/measurement", read_data=False)
		measurement_metadata = measurement.get_metadata_dict()
		data = []
		for nb_block in range(0, 10):
			data.extend(measurement.read_signal_data_block(record_idx=0, channel_idx=1, block_size=4096))
		measurement.close_measurements()

	Example read measurement while NVGate is recording::

		measurement = Measurement.read_measurement_recording()  # Open the measurement while recording
		while not measurement.is_recording_started():  # Wait for NVGate to start recording
			time.sleep(0.5)
		measurement.read_metadata()
		while measurement.is_end_of_reading() == 0:  # Read the measurement while stopped and end reading not reached
		    # Update measurement/record/channel metadata and check if the measurement is still opened
		    # (not closed by NVGate, like when stopped and renaming)
			if not measurement.read_metadata():
				time.sleep(0.5)
				continue
			data = measurement.read_signal_data_block(record_idx=0, channel_idx=1, block_size=4096)
			# Do something with data
			time.sleep(0.01)

	"""

	def __init__(self, records: typing.List[Record] = None):
		"""
		Define the measurement class.

		:param records: The records list (optional)
		:type records: list[Record]
		"""
		if records is None:
			records = []
		self._measurement_id = None
		self._measurement_path = None
		self._nvgate_recording_measurement = False  # Keep track if it's a measurement opened while recording by NVGate

		self._records = []
		for record in records:
			self.add_record(record)

		self._metadata_dict = {}
		self._properties = []

		self._markers = []

		self._opened = False  # Keep track if the measurement is opened
		self._opened_record_idx = None  # Keep track of the opened record index, [0 ... nb_records]
		self._editing = False  # Keep track if the measurement is in editing mode

	def __del__(self):
		"""
		Destructor of the measurement class.
		"""
		try:
			self._close_measurement()
		except (Exception,):
			pass

	def __repr__(self):
		records_str = ""
		for record in self._records:
			records_str += str(record) + ", "
		records_str = records_str[:-2]
		return "Measurement(id={}, records=[{}])".format(self._measurement_id, records_str)

	# --------------------------------- Methods while recording ---------------------------------
	def _is_nvgate_recording_measurement(self) -> bool:
		"""
		Is the measurement being recorded by NVGate.

		:return: True if the measurement is being recorded by NVGate, False otherwise
		"""
		return self._nvgate_recording_measurement

	def is_recording_started(self) -> bool:
		"""
		Is the measurement recording is started (can be in paused state, but not stopped/ended).

		:return: True if the measurement recording was started, False otherwise
		"""
		is_recording_started = False
		if not self._is_nvgate_recording_measurement():
			return False
		try:
			nvg_signal.get_measurement_metadata_key_list(self._measurement_id)
			is_recording_started = True
		except NVGSTreeException:
			is_recording_started = False
		except NVGSRecordException:
			is_recording_started = False
		except (Exception,):
			pass

		return is_recording_started

	def is_recording(self) -> bool:
		"""
		Is the measurement currently recording.

		:return: True if the measurement is recording, False otherwise
		"""
		is_recording = False
		if not self._is_nvgate_recording_measurement():
			return False

		if not self.is_recording_started():
			return False

		try:
			records_vect = nvg_signal.get_records_vect(self._measurement_id)
			for record_vect in records_vect:
				if record_vect.get('recording') == 1:
					is_recording = True
					break
			is_recording = True
		except NVGSTreeException:
			is_recording = False
		except NVGSRecordException:
			is_recording = False
		except:
			pass

		return is_recording

	# --------------------------------- END Methods while recording ---------------------------------

	def add_record(self, record: Record):
		"""
		Add a record to the measurement.

		:param record: The record to add
		:type record: Record
		"""
		record.set_parent_measurement(self)
		record.set_record_idx(len(self._records))
		self._records.append(record)

	def get_records(self) -> list:
		"""
		Get the records list.

		:return: the records list
		"""
		return self._records

	def get_record(self, index) -> Record:
		"""
		Get the record at the index.

		:param index: index of the record [0 ... nb_records - 1]
		:return: the record
		:rtype: Record
		"""
		if index >= len(self._records):
			raise NVGateMeasurementException("The record index is out of range")
		return self._records[index]

	def get_record_by_id(self, record_id) -> Record or None:
		"""
		Get the record with the given id.

		:param record_id: id of the record
		:return: the record
		:rtype: Record, None if not found
		"""
		for record in self._records:
			if record.record_id == record_id:
				return record
		return None

	def set_measurement_id(self, measurement_id):
		"""
		Set the measurement id.

		:param measurement_id: The measurement id to set
		:type measurement_id: int
		"""
		self._measurement_id = measurement_id

	@property
	def measurement_id(self) -> int:
		"""
		Get the measurement id.

		:return: the measurement id
		"""
		return self._measurement_id

	def set_measurement_name(self, measurement_name):
		"""
		Set the measurement name.

		:param measurement_name: The measurement name to set
		:type measurement_name: str
		"""
		self.set_metadata_value(key=str(MeasurementMetadataStr_Predef.META_MEAS_MEASUREMENT_NAME.value),
		                        value=measurement_name)

	@property
	def measurement_name(self) -> str:
		"""
		Get the measurement name.

		:return: the measurement name
		"""
		return self.get_metadata_value(key=str(MeasurementMetadataStr_Predef.META_MEAS_MEASUREMENT_NAME.value))

	def set_sampling_rate(self, sampling_rate):
		"""
		Set the sampling rate.

		:param sampling_rate: The sampling rate to set
		:type sampling_rate: float
		"""
		self.set_metadata_value(key=str(MeasurementMetadataStr_Predef.META_MEAS_SAMPLING_FRONT_END.value),
		                        value=sampling_rate)

	def compute_sampling_rate(self):
		"""
		Compute the sampling rate from the channels sampling rate.
		"""
		sampling_rate = None
		for record in self.get_records():
			for channel in record.get_channels():
				if sampling_rate is None or channel.sampling > sampling_rate:
					sampling_rate = channel.sampling
		self.set_sampling_rate(sampling_rate)

	@property
	def sampling_rate(self) -> float:
		"""
		Get the sampling rate.

		:return: the sampling rate
		"""
		return self.get_metadata_value(key=str(MeasurementMetadataStr_Predef.META_MEAS_SAMPLING_FRONT_END.value))

	def set_part_length(self, part_length: NvgsRecordMultiPartMode):
		"""
		Set the part length for the whole measurement (all records).

		:param part_length: The multi part length to set
		:type part_length: NvgsRecordMultiPartMode
		"""
		for record in self.get_records():
			record.set_part_length(part_length)

	def write_part_length(self, part_length: NvgsRecordMultiPartMode = NvgsRecordMultiPartMode.NvgsSinglePartFile):
		"""
		Write the part length for the whole measurement (all records).

		:param part_length: The multi part length to set
		:type part_length: int (NvgsRecordMultiPartMode)
		"""
		self._open_measurement_if_needed()

		nvg_signal.set_record_multi_part(self._measurement_id, part_length.value)

	def get_duration(self) -> float:
		"""
		Get the duration of the measurement.

		:return: the duration of the measurement
		"""
		return self.get_metadata_value(key=str(MeasurementMetadataStr_Predef.META_MEAS_DURATION.value))

	def set_metadata_value(self, key, value):
		"""
		Set the metadata.

		:param key: The metadata key
		:type key: str
		:param value: The metadata value
		:type value: object
		"""
		if is_measurement_metadata_valid(key):
			self._metadata_dict[key] = value
			return True
		else:
			return False

	def get_metadata_value(self, key) -> typing.Union[object, str, int, float, bool, None]:
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

	def get_properties(self) -> list:
		"""
		Get the properties list.
		"""
		return self._properties

	def get_property(self, key) -> typing.Union[object, str, int, float, bool, None]:
		"""
		Get the property value.

		:param key: The property key
		:type key: str
		:return: the property value
		:rtype: object
		"""
		for record_property in self._properties:
			if record_property['title'] == key:
				return record_property.get('value', None)
		return None

	def set_property(self, key, value):
		"""
		Set/add a property to the measurement.

		:param key: The property key
		:type key: str
		:param value: The property value
		:type value: object
		"""
		property_dict = {'title': key, 'value': value}
		# Check if title already exists
		for idx, property in enumerate(self._properties):
			if property['title'] == key:
				self._properties[idx] = property_dict
				return
		# Add new property if not exists
		self._properties.append(property_dict)

	def _open_measurement(self, measurement_path: str = None):
		"""
		Open the measurement.
		"""
		# print('Opening measurement : {}'.format(self._measurement_path))
		self._measurement_id = nvg_signal.open_measurement(measurement_path)
		# print('Measurement id : {}'.format(self._measurement_id))
		self._measurement_path = measurement_path

		if self._measurement_id < 0:
			raise NVGateMeasurementException("Error while opening the measurement")

		self._opened = True
		self._opened_record_idx = 0
		self._nvgate_recording_measurement = False

		return self._measurement_id

	def _open_measurement_recording(self, nvdrive_port: int, notification_port: int, ip_address: str):
		"""
		Open the measurement.
		"""
		# print('Opening measurement : {}'.format(self._measurement_path))
		self._measurement_id = nvg_signal.open_nvgate_record(nvdrive_port=nvdrive_port,
		                                                     notification_port=notification_port,
		                                                     ip_address=ip_address)
		# print('Measurement id : {}'.format(self._measurement_id))
		self._measurement_path = None

		if self._measurement_id < 0:
			raise NVGateMeasurementException("Error while opening the measurement")

		self._opened = True
		self._read_opened_record_idx()  # Set self._opened_record_idx, can be None if record didn't start yet
		self._nvgate_recording_measurement = True

		return self._measurement_id

	def _close_measurement(self):
		"""
		Close the measurement.
		"""
		time.sleep(0.1)  # This is a workaround to avoid crash/issues when closing/opening quickly a measurement

		if not self._is_opened():
			self._opened = False
			return

		# print('Closing measurement {} : {}'.format(self._measurement_id, self._measurement_path))
		self._stop_editing()
		ret = nvg_signal.close_measurement(self._measurement_id)
		self._opened_record_idx = None
		self._opened = False

	def close_measurement(self):
		"""
		Close the measurement.
		"""
		self._close_measurement()

	@staticmethod
	def close_all_measurements():
		"""
		Close all opened measurements.
		"""
		ret = nvg_signal.close_all_measurements()

	def _is_opened(self):
		"""
		Is the measurement opened.

		:return: True if the measurement is opened, False otherwise
		"""
		test = None

		if self._is_nvgate_recording_measurement():
			test = self.is_end_of_reading(channel_idx=1)
		else:
			try:
				test = nvg_signal.get_measurement_path(self._measurement_id)
			except:
				pass
		return test is not None

	def _open_measurement_if_needed(self):
		"""
		Open the measurement if needed.
		"""
		# Flag way
		if not self._opened:
			self._open_measurement(measurement_path=self._measurement_path)

	def _open_record_by_id(self, record_id: int):
		"""
		Open the given record.

		:param record_id: The record id to open
		:type record_id: int
		"""
		self._open_measurement_if_needed()
		try:
			ret = nvg_signal.open_record(self._measurement_id, record_id)
		except:
			raise NVGateMeasurementException("Error while opening the record")

	def _open_record_by_idx(self, record_idx: int = 0):
		"""
		Open the record, if no record index is given, open the first record.

		:param record_idx: The record index to open [0 ... nb_records - 1]
		:type record_idx: int
		"""
		record_id = self._records[record_idx].record_id
		self._open_record_by_id(record_id=record_id)

	def open_record(self, record_idx=None, record_id=None):
		"""
		Open the record, using idx [0 ... nb_records - 1] or id.

		:param record_idx: The record index to open
		:type record_idx: int
		:param record_id: The record id to open
		:type record_id: int
		"""
		asked_record = None
		if record_idx is not None:
			asked_record = self.get_record(index=record_idx)
		elif record_id is not None:
			asked_record = self.get_record_by_id(record_id=record_id)

		if not asked_record:
			raise NVGateMeasurementException("The record is not known by measurement python object")

		if self._opened_record_idx == asked_record.get_record_idx():
			return  # The record is already opened

		opened_record_idx = self._read_opened_record_idx()

		# Check if a record is already opened, if yes, close it before opening the new one
		if opened_record_idx is not None:
			self.close_record()

		self._open_record_by_id(record_id=asked_record.record_id)

	def _close_record(self):
		"""
		Close the record.
		"""
		nvg_signal.close_record(self._measurement_id)
		# self._opened = False  # Measurement is not closed, only the record is closed
		self._opened_record_idx = None

	def close_record(self):
		"""
		Close the record.
		"""
		self._close_record()

	def is_record_opened(self) -> bool:
		"""
		Is the record opened.

		:return: True if the record is opened, False otherwise
		"""
		return self._read_opened_record_idx() is not None

	def _read_opened_record_idx(self) -> int:
		"""
		Get the opened record index.

		:return: the opened record index [0 ... nb_records - 1], None if no record is opened
		:rtype: int or None
		"""
		try:
			opened_record_idx = nvg_signal.get_opened_record_index(self._measurement_id)
		except:
			opened_record_idx = -1

		if opened_record_idx > 0:
			opened_record_idx -= 1
		else:
			opened_record_idx = None
		self._opened_record_idx = opened_record_idx

		return opened_record_idx

	def get_opened_record(self):
		"""
		Get the opened record.

		:return: the opened record
		:rtype: Record
		"""
		self._read_opened_record_idx()
		self.read_records_metadata()

		if self._opened_record_idx is None:
			return None

		return self.get_record(index=self._opened_record_idx)

	def _start_editing(self):
		"""
		Start editing the measurement.
		"""
		self._editing = True if nvg_signal.start_editing(self._measurement_id) == 0 else False

	def _stop_editing(self):
		"""
		Stop editing the measurement.
		"""
		self._editing = False if nvg_signal.stop_editing(self._measurement_id) == 0 else True

	def start_record(self, date: datetime.datetime = None):
		"""
		Start the record, write the metadata and allow writing signal data.
		"""
		if date is None:
			date = datetime.datetime.now()
		# Convert to UTC format
		date = datetime_to_windows_time_int(date)
		nvg_signal.start_record(self._measurement_id, date)

	def stop_record(self):
		"""
		Stop the record, stop writing the metadata and signal data.
		"""
		nvg_signal.stop_record(self._measurement_id)
		self._opened = False
		self._opened_record_idx = None

	def read_signal_data_record(self, record_idx: int = 0):
		"""
		Read the data from a record, if no record index is given, read the first record.
		Record must be opened before calling this method.

		:param record_idx: The record index to read [0 ... nb_records - 1]
		:type record_idx: int
		"""
		if record_idx >= len(self._records):
			raise NVGateMeasurementException("The record index is out of range")

		# Open the correct record
		record = self._records[record_idx]

		self.open_record(record_idx=record_idx)
		self.set_read_position(0.0)

		for channel in record.get_channels():
			self.read_signal_data_channel(channel_idx=channel.channel_id, record_idx=record_idx)

	def read_signal_data_channel(self, channel_idx: int = 1, record_idx: int = 0):
		"""
		Read the data from a channel, if no record index is given, read the first record.
		Record must be opened before calling this method.

		:param channel_idx: The channel index to read [1 ... nb_channels]
		:type channel_idx: int
		:param record_idx: The record index to read [0 ... nb_records - 1], if set to -1, read all records
		:type record_idx: int
		"""
		if record_idx >= len(self._records):
			raise NVGateMeasurementException("The record index is out of range")

		# Read all records
		if record_idx == -1:
			# print('read_signal_data_channel for all records')
			for idx, record in enumerate(self._records):
				# Open the correct record
				# print('Record : {}'.format(idx))

				self.open_record(record_idx=idx)

				opened_record = self.get_opened_record()
				# print('Opened record : {}'.format(opened_record))

				# Set time_position as the beginning of the record
				time_position = record.rel_date
				self.set_read_position(time=0.0)
				self.read_signal_data_channel(channel_idx=channel_idx, record_idx=idx)
			return

		# Open the correct record
		record = self._records[record_idx]

		if channel_idx > len(record.get_channels()):
			raise NVGateMeasurementException("The channel index is out of range")

		channel = record.get_channel(index=channel_idx)

		self.open_record(record_idx=record_idx)

		channel_duration = channel.get_metadata_value(str(ChannelMetadataStr_Predef.RECORD_DURATION))
		channel_sampling = channel.get_metadata_value(str(ChannelMetadataStr_Predef.CHANNEL_SAMPLING_RATE))
		expected_loop = int(channel_duration * channel_sampling / BLOCK_SIZE) + 1

		channel.clear_data()

		# print('Reading measurement {} record {} channel {}'.format(self._measurement_id, record.record_id, channel.channel_id))
		for i in range(0, expected_loop):
			data = nvg_signal.read_sample_block(self._measurement_id, channel.channel_id, BLOCK_SIZE)
			# print('Read {} samples'.format(len(data)))
			channel.add_data(data)

		# print('Channel duration: {}'.format(channel_duration))
		# print('Channel sampling: {}'.format(channel_sampling))

		# Check if the data is correct
		if len(channel.get_data()) != channel_duration * channel_sampling:
			logging.error("The channel data is not complete")

	def read_signal_data(self):
		"""
		Read the data from the measurement.
		"""
		for idx, record in enumerate(self._records):
			self.read_signal_data_record(record_idx=idx)

	def read_signal_data_block(self, record_idx=0, channel_idx=1, block_size=BLOCK_SIZE, reset_position: float = None):
		"""
		Read the data from a channel, if no record index is given, read the first record.
		Use to be faster than read_signal_data_channel if have to process data while reading.
		Note that the position is moving forward following block size read, if you want to reset the position, use
		reset_position parameter.

		:param record_idx: The record index to read [0 ... nb_records - 1]
		:type record_idx: int
		:param channel_idx: The channel index to read [1 ... nb_channels]
		:type channel_idx: int
		:param block_size: The block size to read
		:type block_size: int
		:param reset_position: The position to reset the channel to, while reading position is moving forward following block size read
			if set to None, the position is not reset, if set to 0.0, the position is reset to the beginning of the channel
			if set to 1.0 the position is reset to 1.0s. From the beginning of the record.
		:type reset_position: float, in seconds
		:return: The data read
		"""
		if record_idx >= len(self._records):
			raise NVGateMeasurementException("The record index is out of range")

		# Open the correct record
		record = self._records[record_idx]
		if channel_idx > len(record.get_channels()):
			raise NVGateMeasurementException("The channel index is out of range")

		channel = record.get_channel(index=channel_idx)

		if not self._is_nvgate_recording_measurement():
			# print('Opened record : {}'.format(self._read_opened_record_idx()))
			self.open_record(record_idx=record_idx)
		# print('After, opened record : {}'.format(self._read_opened_record_idx()))

		# record_id, sample_index = self.get_read_position(channel_idx=channel_idx)

		if reset_position is not None:
			self.set_read_position(time=reset_position)

		data = nvg_signal.read_sample_block(self._measurement_id, channel.channel_id, block_size)

		# is_opened = self.is_record_opened() & self._is_opened()
		# print('self.is_record_opened() & self._is_opened(): {}'.format(is_opened))
		# if is_opened:
		# 	time.sleep(0.1)
		# 	is_end_of_reading = nvg_signal.is_end_of_reading(self._measurement_id, channel_idx)
		# 	print('is_end_of_reading: {}'.format(is_end_of_reading))

		return data

	def read_signal_data_block_by_sample(self, record_idx=0, channel_idx=1, block_size=BLOCK_SIZE, sample_begin=0):
		"""
		Read the data from a channel, if no record index is given, read the first record.
		Use to be faster than read_signal_data_channel if have to process data while reading.
		Note that the position is moving forward following block size read, if you want to reset the position, use
		reset_position parameter.

		:param record_idx: The record index to read [0 ... nb_records - 1]
		:type record_idx: int
		:param channel_idx: The channel index to read [1 ... nb_channels]
		:type channel_idx: int
		:param block_size: The block size to read
		:type block_size: int
		:param sample_begin: The sample to begin reading
		:type sample_begin: int
		:return: The data read
		"""
		record = self._records[record_idx]
		channel = record.get_channel(index=channel_idx)

		time_position = sample_begin / channel.sampling

		data = self.read_signal_data_block(record_idx=record_idx, channel_idx=channel_idx, block_size=block_size,
		                                   reset_position=time_position)

		return data

	def get_reading_status(self, channel_idx):
		"""
		Get the reading status of a channel.
		"""
		reading_status = ReadingStatus.MeasurementNotOpened

		try:
			is_end_of_reading = nvg_signal.is_end_of_reading(self._measurement_id, channel_idx)
			if is_end_of_reading == 0:
				reading_status = ReadingStatus.RecordReading
			elif is_end_of_reading == 1:
				reading_status = ReadingStatus.RecordRead
			elif is_end_of_reading == 2:
				reading_status = ReadingStatus.MeasurementRead
		except NVGSTreeException:
			reading_status = ReadingStatus.MeasurementNotOpened
		except Exception as e:
			reading_status = ReadingStatus.Unknown

		return reading_status

	def is_end_of_reading(self, channel_idx=1):
		"""
		Is the end of reading of a channel for the whole measurement.

		:param channel_idx: The channel index to read [1 ... nb_channels]
		:type channel_idx: int
		:return: True if the end of reading is reached, False otherwise, None if measurement is not opened
		:rtype: int
		"""
		reading_status = self.get_reading_status(channel_idx=channel_idx)
		if reading_status == ReadingStatus.MeasurementNotOpened:
			return None
		elif reading_status == ReadingStatus.MeasurementRead:
			return True
		else:
			return False

	def get_read_position(self, channel_idx=1):
		"""
		Get the read position of a channel.
		Record have to be opened before calling this method.

		:param channel_idx: The channel index to read [1 ... nb_channels]
		:type channel_idx: int
		:return: The read record id and sample index
		:rtype: tuple of int
		"""
		record_id, sample_index = nvg_signal.get_read_position(self._measurement_id, channel_index=channel_idx)
		# print("Read position: record_id={}, sample_index={}".format(record_id, sample_index))
		return record_id, sample_index

	def set_read_position(self, time=0.0):
		"""
		Set the read position of a channel.
		Record have to be opened before calling this method.

		:param time: The time to set the read position to
		:type time: float, in seconds
		"""
		# print("Set read position to {}".format(time))
		nvg_signal.set_read_position(self.measurement_id, time=time)
		self.get_opened_record()  # Record can change if time is in another record

	def read_compressed_signal_data_channel(self, channel_idx: int, requested_nb_pairs: int, start: float = 0.0,
	                                        stop: float = None):
		"""
		Read the compressed data from a channel

		:param channel_idx: The channel index to read [1 ... nb_channels]
		:type channel_idx: int
		:param requested_nb_pairs: The requested number of pairs
		:type requested_nb_pairs: int
		:param start: The start time of the data to read
		:type start: float, in seconds
		:param stop: The stop time of the data to read, if None, read until the end. Cumulative time from
			beginning if multirecords
		:type stop: float, in seconds
		:return: The compressed data
		:rtype: list of pairs of float (min, max)
		"""
		self._open_measurement_if_needed()

		if stop is None:
			stop = self.get_duration()

		data = nvg_signal.get_compressed_signal(self._measurement_id, channel_idx, start, stop, requested_nb_pairs)

		return data

	def read_metadata(self):
		"""
		Read/Update measurement, records and channels metadata and properties.

		Note : This method is not reading the signal data, only the metadata and properties.
		:return: True if the metadata and properties are read, False otherwise
		"""
		self._open_measurement_if_needed()

		try:
			self.read_measurement_metadata()
		except NVGSException:
			print('Error while reading measurement metadata')
			return False

		try:
			self.read_measurement_properties()
		except NVGSException:
			print('Error while reading measurement properties')
			return False

		try:
			self.read_records_metadata()
		except NVGSException:
			print('Error while reading records metadata')
			return False

		return True

	def read_measurement_metadata(self):
		"""
		Read/Update measurement metadata.
		"""
		self._open_measurement_if_needed()

		list_measurement_metadata = nvg_signal.get_measurement_metadata_dict(self._measurement_id)

		self._metadata_dict.update(list_measurement_metadata)

	def read_measurement_properties(self):
		"""
		Read/Update measurement properties.
		Properties are metadata defined by the user.
		"""
		self._open_measurement_if_needed()

		self._properties.clear()
		properties = nvg_signal.get_measurement_properties(self._measurement_id)
		if properties:
			self._properties.extend(properties)

	def read_records_metadata(self):
		"""
		Read/Update records metadata, if new records are added, they are added to the measurement.

		Note :

		"""
		# TODO : Incomplete, what do we do for deleted channels/records ?

		self._open_measurement_if_needed()

		records_vect = nvg_signal.get_records_vect(self._measurement_id)

		# Update existing records, using record_id attributes and recordId key in records_vect
		for record in self._records:
			for record_vect in records_vect:
				if record.record_id == record_vect[RecordMetadataStr.recordId.value]:
					record.load_metadata_from_record_vect(record_vect)

		# Add new records
		for record_vect in records_vect:
			if record_vect[RecordMetadataStr.recordId.value] not in [record.record_id for record in self._records]:
				record = Record()
				record.load_metadata_from_record_vect(record_vect)
				self.add_record(record)

		# TODO : Improve that, does not need to update this each time, only at creation, are not supposed to changed
		# Or it is futurproof haha
		channels_list = nvg_signal.get_channel_list(self._measurement_id)
		channels_metadata = []
		for i in range(0, len(channels_list)):
			channel_metadata = nvg_signal.get_channel_metadata_dict(self._measurement_id, i + 1)
			channels_metadata.append(channel_metadata)

		# Update existing channels, using channel_id attributes and channelId key in channels_metadata
		for record in self.get_records():
			for channel in record.get_channels():
				for channel_metadata in channels_metadata:
					if channel.channel_id == channel_metadata[str(ChannelMetadataStr_Predef.CHANNEL_NUMBER)]:
						channel.load_metadata_from_metadata_dict(channel_metadata)

		# Add new channels
		for record in self.get_records():
			for idx, channel_metadata in enumerate(channels_metadata):
				ch_id = idx + 1
				if ch_id not in [channel.channel_id for channel in record.get_channels()]:
					ch_name = channel_metadata.get(str(ChannelMetadataStr_Predef.CHANNEL_NAME), None)
					ch_sampling = channel_metadata.get(str(ChannelMetadataStr_Predef.CHANNEL_SAMPLING_RATE), None)
					ch_type = ChannelType[channel_metadata.get(str(ChannelMetadataStr_Predef.CHANNEL_TYPE), 'Dynamic')]
					channel = Channel(name=ch_name, sampling=ch_sampling, type=ch_type)
					channel.set_channel_id(ch_id)
					channel.load_metadata_from_metadata_dict(channel_metadata)
					record.add_channel(channel)

	@classmethod
	def read_measurement(cls, measurement_path: str, read_data: bool = True):
		"""
		Read a measurement from a file.
		"""
		# print('Reading measurement {}'.format(measurement_path))
		time_init = time.time()
		measurement = cls()

		measurement_id = measurement._open_measurement(measurement_path=measurement_path)

		if measurement_id < 0:
			raise NVGateMeasurementException("Error while opening the measurement")

		measurement.set_measurement_id(measurement_id)

		measurement.read_metadata()

		# Read the channels data
		if read_data:
			measurement.read_signal_data()
		# measurement.close_record()
		# print('Read measurement id : {}'.format(measurement_id))

		# Close the measurement
		measurement._close_measurement()

		# print('Reading measurement {} in {}'.format(measurement.measurement_name, time.time() - time_init))

		return measurement

	@classmethod
	def read_measurement_recording(cls, nvdrive_port=3000, notification_port=4300, ip_address='127.0.0.1'):
		"""
		Read the measurement being recorded by NVGate.
		"""
		# print('Opening the measurement being recorded by NVGate')
		measurement = cls()

		measurement_id = measurement._open_measurement_recording(nvdrive_port=nvdrive_port,
		                                                         notification_port=notification_port,
		                                                         ip_address=ip_address)

		if measurement_id < 0:
			raise NVGateMeasurementException("NVGate must be opened before reading a measurement while recording")

		measurement.set_measurement_id(measurement_id)

		is_recording = measurement.is_recording_started()
		if is_recording:
			measurement.read_metadata()
		else:
			print('Measurement is not recording, we cannot retrieve the metadata')

		return measurement

	def remove_channel(self, channel: Channel):
		"""
		Remove a channel from the measurement. All records have to be closed before removing a channel.

		:param channel: The channel to remove
		:type channel: Channel
		"""
		self._open_measurement_if_needed()
		self._start_editing()
		nvg_signal.remove_channel(self._measurement_id, channel_index=channel.channel_id)
		self._stop_editing()

	def remove_record(self, record: Record):
		"""
		Remove a record from the measurement.

		:param record: The record to remove
		:type record: Record
		"""
		self._open_measurement_if_needed()
		self._start_editing()
		ret = nvg_signal.remove_record(self._measurement_id, record.record_id)
		self._stop_editing()
		if ret == 0:
			self._records.remove(record)

	def erase_part(self, record: Record, channel: Channel, from_part: int, to_part: int):
		"""
		Erase a part from a record.

		:param record: The record to erase the part
		:type record: Record
		:param channel: The channel to erase the part
		:type channel: Channel
		:param from_part: The first part to erase
		:type from_part: int
		:param to_part: The last part to erase
		:type to_part: int
		"""
		self.open_record(record_id=record.record_id)
		self._start_editing()
		ret = nvg_signal.erase_part(self._measurement_id, channel.channel_id, from_part, to_part)
		self._stop_editing()

	def split_record(self, record: Record, first_part_of_new_record: int):
		"""
		Split a record in multiple parts.

		:param record: The record to split
		:type record: Record
		:param first_part_of_new_record: The first part where to split the record (this part will be on the right of the split)
		:type first_part_of_new_record: int
		"""
		# Open the correct record
		self.open_record(record_id=record.record_id)
		self._start_editing()
		nvg_signal.split(self._measurement_id, first_part_of_new_record)
		self._stop_editing()

	def read_markers(self):
		self._markers.clear()
		marker_list = nvg_signal.get_markers(self._measurement_id)
		if marker_list:
			self._markers.extend(marker_list)

	def get_marker_list(self):
		"""
		Get the marker list.

		:return: The marker list
		:rtype: list of Marker
		"""
		return self._markers

	def write_marker(self, position, comment):
		"""
		Write a marker to the measurement, measurement must be in recording.

		:param position: The position of the marker, in seconds
		:type position: float
		:param comment: The comment of the marker
		:type comment: str
		"""
		ret = nvg_signal.add_marker(self._measurement_id, position=position, comment=comment)

	def write_signal_data_record(self, record_idx=0):
		"""
		Write the data from a record, if no record index is given, write the first record.

		:param record_idx: The record index to write [0 ... nb_records - 1]
		:type record_idx: int
		"""
		record = self._records[record_idx]

		date = self.get_metadata_value(key=str(MeasurementMetadataStr_Predef.META_MEAS_DATE))
		if date:
			date = date_string_to_datetime(date)

		self.write_part_length(part_length=NvgsRecordMultiPartMode.get_enum_from_time(record.part_length))

		# Start record to open the write
		self.start_record(date)

		# Write the channels data
		for channel in record.get_channels():
			self.write_signal_data_channel(record_idx=record_idx, channel=channel)

		self.write_measurement_properties()

		# Stop record
		self.stop_record()

	def write_signal_data_channel(self, channel: Channel, record_idx=0):
		"""
		Write the data from a channel, if no record index is given, write the first record.

		:param channel: The channel to write the data
		:type channel: Channel
		:param record_idx: The record index to write [0 ... nb_records - 1]
		:type record_idx: int
		"""
		for data in channel.get_data_block(BLOCK_SIZE):
			self.write_signal_data_block(data=data, record_idx=record_idx, channel_idx=channel.channel_id)

	def write_signal_data(self):
		"""
		Write the data from the measurement.
		"""
		for idx, record in enumerate(self._records):
			self.write_signal_data_record(record_idx=idx)

	def write_measurement_metadata(self):
		"""
		Write the measurement metadata.
		"""
		# Write measurement metadata
		metadata_dict = self.get_metadata_dict()

		# Remove some metadata that can't be written for measurement
		read_only_measurement_metadata = [MeasurementMetadataStr_Predef.META_MEAS_SAMPLING_FRONT_END,
		                                  MeasurementMetadataStr_Predef.META_MEAS_SAMPLE_FORMAT]
		for key in read_only_measurement_metadata:
			metadata_dict.pop(key.value, None)

		for key, value in metadata_dict.items():
			try:
				nvg_signal.set_measurement_metadata(self._measurement_id, key, value)
			except:
				pass
			else:
				pass

	def write_measurement_properties(self):
		"""
		Write the measurement properties.
		Properties are metadata defined by the user.
		"""
		self._open_measurement_if_needed()

		# Write measurement properties
		for property in self.get_properties():
			ret = nvg_signal.add_measurement_property(self._measurement_id, property)

	def write_channels_metadata(self, record):
		"""
		Write the channels metadata for a record.

		:param record: The record to write the channels metadata
		:type record: Record
		"""
		for channel in record.get_channels():
			self.write_channel_metadata(channel)

	def write_channel_metadata(self, channel):
		"""
		Write the channel metadata, channel must be added to the measurement before calling this method.

		:param channel: The channel to write the metadata
		:type channel: Channel
		"""
		type_int = channel.get_type_int()
		channel.set_channel_id(
			nvg_signal.add_channel(self._measurement_id, channel.get_type_int(), int(channel.sampling)))

		# Write channel metadata
		metadata_dict = channel.get_metadata_dict()

		# Remove some metadata that can't be written for channel
		read_only_channels_metadata = [ChannelMetadataStr_Predef.CHANNEL_SAMPLING_RATE,
		                               ChannelMetadataStr_Predef.RECORD_DURATION]
		for key in read_only_channels_metadata:
			metadata_dict.pop(key.value, None)

		for key, value in metadata_dict.items():
			try:
				nvg_signal.set_channel_metadata(self._measurement_id, channel.channel_id, key, value)
			except:
				print("Error while writing channel metadata {}={}".format(key, value))
			else:
				pass

	# print('Success writing channel metadata {}={}'.format(key, value))

	def write_signal_data_block(self, data, record_idx=0, channel_idx=1):
		"""
		Write the data from a channel, if no record index is given, write the first record.
		Currently only the first record can be written

		:param data: The data to write
		:type data: list of float
		:param record_idx: The record index to write [0 ... nb_records - 1]
		:type record_idx: int
		:param channel_idx: The channel index to write [1 ... nb_channels]
		:type channel_idx: int
		"""
		try:
			nvg_signal.write_sample_block(self._measurement_id, channel_index=channel_idx, data=data)
			return True
		except:
			return False

	def write_measurement(self, project_path: str):
		"""
		Write the measurement to a file.

		:param project_path: The project path to write the measurement to
		:type project_path: str
		"""
		# print('Writing measurement {}'.format(self.measurement_name))

		self.compute_sampling_rate()

		# Check needed metadata
		if self.measurement_name is None:
			raise NVGateMeasurementException("Measurement name is not set")
		if self.sampling_rate is None:
			raise NVGateMeasurementException("Sampling rate is not set")

		self._measurement_id = nvg_signal.create_new_measurement(project_path, self.measurement_name,
		                                                         self.sampling_rate)

		if self._measurement_id < 0:
			raise NVGateMeasurementException("Error while creating the measurement")

		self._measurement_path = nvg_signal.get_measurement_path(self._measurement_id)
		self._opened = True
		self._opened_record_idx = 0

		if len(self._records) > 1:
			logging.warning("Currently toolkit allow only the create for 1 record per measurement "
			                "(but can read multiple records)")
		if len(self._records) == 0:
			logging.warning("No record to write")
			return

		self.write_measurement_metadata()

		record_idx = 0
		self.write_channels_metadata(record=self._records[record_idx])

		# TODO FUTURE : Allow multiple records calling self.write_signal_data()
		self.write_signal_data_record(record_idx=record_idx)

	# self.write_measurement_properties()

	@staticmethod
	def search_measurements(search_path: str):
		"""
		Search measurements in a path.

		:param search_path: The path to search in.
		:return: A list of measurements path
		"""
		list_dict_measurements = nvg_signal.search_measurements(search_path)
		list_measurements = []
		for dict_measurement in list_dict_measurements:
			path = os.path.join(dict_measurement['ProjectPath'], dict_measurement['ProjectName'],
			                    dict_measurement['MeasurementName'])
			path = os.path.abspath(path)
			list_measurements.append(path)
		return list_measurements
