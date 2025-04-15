import cython

import malloc, free
from orostk.file.measurement_exceptions import (
	NVGSException,
	NVGSRecordException,
	NVGSTreeException
)

def create_new_measurement(record_path, record_name, sampling_rate_base):
  """
        Create a new measurement directory and return the measurement id

        :param record_path: the path of the record
        :type record_path: str
        :param record_name: the name of the record
        :type record_name: str
        :param sampling_rate_base: the sampling rate base
        :type sampling_rate_base: int
        :return: the measurement id
        :rtype: int
        """
  ...

def open_measurement(measurement_path) -> int:
  """
        Open a measurement and return the measurement id

        :param measurement_path: the path of the measurement (the one containing the .osfh and records directories)
        :type measurement_path: str
        :return: the measurement id
        :rtype: int
        """
  ...

def open_nvgate_record(nvdrive_port=3000, notification_port=4300, ip_address='127.0.0.1'):
  """
        Opens the current recording in NvGate
        Warning : Until a recording has started (in NvGate) all calls to the metadata or sample reading functions will return 0

        :param nvdrive_port: the port of the NVGate drive
        :type nvdrive_port: int
        :param notification_port: the port of the NVGate notification
        :type notification_port: int
        :param ip_address: the ip address of the NVGate
        :type ip_address: str
        :return: the measurement id
        :rtype: int
        """
  ...

def open_nvgate_record_default():
  """
        Opens the current recording in NvGate
        Warning : Until a recording has started (in NvGate) all calls to the metadata or sample reading functions will return 0

        :return: the measurement id
        :rtype: int
        """
  ...

def is_end_of_reading(opened_measurement_id, channel_index):
  """
        Test if all the signal of channel channel_index has been read

        :param opened_measurement_id: the measurement id
        :type opened_measurement_id: int
        :param channel_index: the channel index to write [1...number of channels]
        :type channel_index: int
        :return: the return code, 2: NvGate mode : recorder is stopped, nothing more to read, Normal mode : the last record was read completely, 1: the end of the current recording has been reached, call NVGS_CloseRecord, NVGS_GetRecordsVect and NVGS_OpenRecord to read next record, 0 : NvGate mode : record in progress, Normal mode : end of record not reached, -1: invalid openedMeasurementId, -2: the measurement is not open, -3  : invalid channel index
        :rtype: intvc
        """
  ...

def close_measurement(opened_measurement_id):
  """
        Close a measurement

        :param opened_measurement_id: the measurement id
        :type opened_measurement_id: int
        :return: the return code, 0 if success, -1 if invalid openedMeasurementId
        :rtype: int
        """
  ...

def close_all_measurements():
  """
        Close all opened measurements

        :return: the return code, 0 if success, -1 otherwise
        """
  ...

def search_measurements(search_path):
  """
        Search measurements in a record

        Returns the list of all the records found in the subdirectories of the directory record_path
        :param search_path: the path of the record
        :type search_path: str
        :return: the list of measurements
        :rtype: list
        """
  ...

def get_measurement_path(opened_measurement_id):
  """
        Return the measurement path

        :param opened_measurement_id: the measurement id
        :type opened_measurement_id: int
        :return: the measurement path
        :rtype: str
        """
  ...

def start_record(opened_measurement_id, utc_date=None):
  """
        Start the record of the measurement

        :param opened_measurement_id: the measurement id
        :type opened_measurement_id: int
        :param utc_date: the UTC date of the first sample (UTC date in number of step of 100 ns since 01/01/1601, Windows format)
        :type utc_date: int
        :return: the return code, 0 if success, -1 if invalid openedMeasurementId, -2 if measurement deleted or not ready, -3 if channel list is empty, -4 if unable to save record metadata, -5 if unable to start record
        """
  ...

def stop_record(opened_measurement_id):
  """
        Stop the record

        :param opened_measurement_id: the measurement id
        :type opened_measurement_id: int
        :return: the return code, 0 if success, -1 if invalid openedMeasurementId, -2 if unable to update metadata

        """
  ...

def get_records_vect(opened_measurement_id):
  """
        Get the records list of the measurement

        :param opened_measurement_id: the measurement id
        :type opened_measurement_id: int
        :return: the records vector
        :rtype: list of dict
        """
  ...

def get_list_records(opened_measurement_id):
  """
        Get the records list of the measurement

        :param opened_measurement_id: the measurement id
        :type opened_measurement_id: int
        :return: the records list
        :rtype: list of dict
        """
  ...

def open_record(opened_measurement_id, record_id):
  """
        Open a record

        :param opened_measurement_id: the measurement id
        :type opened_measurement_id: int
        :param record_id: the record id
        :type record_id: int
        :return: the return code, 1 if success, 0 recorder not started, -1 if invalid openedMeasurementId, -2 if the measurement is not open, -3 if record already opened, -4 if unable to open record
        :rtype: int
        """
  ...

def close_record(opened_measurement_id):
  """
        Close the record

        :param opened_measurement_id: the measurement id
        :type opened_measurement_id: int
        :return: the return code, 1 if success, 0 recorder not started, -1 if invalid openedMeasurementId, -2 if the measurement is not open, -3 if invalid record index (or already closed)
        :rtype: int
        """
  ...

def get_opened_record_index(opened_measurement_id):
  """
        Get the opened record index

        :param opened_measurement_id: the measurement id
        :type opened_measurement_id: int
        :return: the opened record index [1...number of records]
        :rtype: int
        """
  ...

def get_record_length(opened_measurement_id):
  """
        Get the record length

        :param opened_measurement_id: the measurement id
        :type opened_measurement_id: int
        :return: the record length
        :rtype: float
        """
  ...

def add_channel(opened_measurement_id, channel_type, sampling_rate):
  """
        Add a channel to the measurement

        :param opened_measurement_id: the measurement id
        :type opened_measurement_id: int
        :param channel_type: the channel type
        :type channel_type: int
        :param sampling_rate: the sampling rate
        :type sampling_rate: float
        :return: the return code, 0 if success, -1 if invalid openedMeasurementId, -2 if measurement deleted or not ready, -3 if invalid sampling rate, -4 if unable to create a new record, -5 if unable to add a new channel
        :rtype: int
        """
  ...

def get_channel_list(opened_measurement_id):
  """
        Get the channel list

        :param opened_measurement_id: the measurement id
        :type opened_measurement_id: int
        :return: the channel list
        :rtype: list
        """
  ...

def set_channel_coeff_to_si(opened_measurement_id, channel_index, coeff_to_si, offset_to_si):
  """
        Set the channel coefficient to SI

        Initialize the unit conversion coefficient of a channel. These coefficients are used to convert the samples to SI units.
        Call this function only if the source samples are not in SI units. The conversion formula is :
        sample_si = sample_not_si * coeffToSI + offsetToSI

        :param opened_measurement_id: the measurement id
        :type opened_measurement_id: int
        :param channel_index: the channel index
        :type channel_index: int
        :param coeff_to_si: the coefficient to SI
        :type coeff_to_si: float
        :param offset_to_si: the offset to SI
        :type offset_to_si: float
        :return: the return code, 0 if success, -1 if invalid openedMeasurementId, -2 if measurement deleted or not ready, -3 if invalid channel index, -4 if unable to set channel coefficient to SI
        :rtype: int
        """
  ...

def write_sample_block(opened_measurement_id, channel_index, data):
  """
        Write a sample block

        :param opened_measurement_id: the measurement id
        :type opened_measurement_id: int
        :param channel_index: the channel index to write [1...number of channels]
        :type channel_index: int
        :param data: the data to write
        :type data: list
        :return: the return code, 0 if success, -1 if invalid openedMeasurementId, -2 if measurement deleted or not ready, -3 if invalid channel index, -4 if unable to write samples block
        """
  ...

def get_read_position(opened_measurement_id: OpenedMeasurementId_t, channel_index: int):
  """
        Get the read position

        :param opened_measurement_id: the measurement id
        :type opened_measurement_id: int
        :param channel_index: the channel index to write [1...number of channels]
        :type channel_index: int
        :return: current_record_id, current_sample_index [0..number of samples in the current record], (current_record_id, current_sample_index)
        :rtype: (int, int)
        """
  ...

def set_read_position(opened_measurement_id: OpenedMeasurementId_t, time: float):
  """
        Set the read position (for all channels)

        :param opened_measurement_id: the measurement id
        :type opened_measurement_id: int
        :param time: the time to set, relative position in the record in seconds
        :type time: float
        :return: the return code, 0 if success, -1 if invalid openedMeasurementId, -2 if the measurement is not open, -3 if invalid record index, -4 if unable to set read position, -5 if unable to open record (if change)
        :rtype: int
        """
  ...

def read_sample_block(opened_measurement_id, channel_index, sample_count):
  """
        Read a sample block

        :param opened_measurement_id: the measurement id
        :type opened_measurement_id: int
        :param channel_index: the channel index to write [1...number of channels]
        :type channel_index: int
        :param sample_count: the number of samples to read
        :type sample_count: int
        :return: the data read
        :rtype: list of float
        """
  ...

def get_compressed_signal(opened_measurement_id, channel_index, start, stop, requested):
  """
        Get the compressed signal

        :param opened_measurement_id: the measurement id
        :type opened_measurement_id: int
        :param channel_index: the channel index to write [1...number of channels]
        :type channel_index: int
        :param start: Relative start position from the begining of the record (in seconds).
        If it is a multi-record, the relative date uses the cumulative durations of the records to determine the reading position
        (without taking into account the durations between 2 records)
        :type start: float
        :param stop: Relative stop position from the begining of record (in seconds)
        If it is a multi-record, the relative @p stop date may not be in the same record as the relative @p start date.
        All records between the @p start and @p stop dates are compressed as if they were consecutive.
        :type stop: float
        :param requested: Minimum number of min/max pairs requested
        :type requested: int
        :return: the data read (min/max pairs)
        :rtype: list of pairs of float
        """
  ...

def get_measurement_metadata_type(opened_measurement_id, key):
  """
        Get the metadata type of a measurement

        :param opened_measurement_id: the measurement id
        :type opened_measurement_id: int
        :param key: the key of the metadata
        :type key: str
        :return: the metadata type
        """
  ...

def get_measurement_metadata_key_list(opened_measurement_id):
  """
        Get the metadata key list of a measurement

        :param opened_measurement_id: the measurement id
        :type opened_measurement_id: int
        :return: the metadata key list
        :rtype: list
        """
  ...

def get_measurement_metadata(opened_measurement_id, key):
  """
        Get the metadata of a measurement, depending on the type of the metadata

        :param opened_measurement_id: the measurement id
        :type opened_measurement_id: int
        :param key: the key of the metadata
        :type key: str
        """
  ...

def get_measurement_metadata_dict(opened_measurement_id):
  """
        Get all metadata of a measurement

        :param opened_measurement_id: the measurement id
        :type opened_measurement_id: int
        :return: the metadata of the measurement
        :rtype: dict
        """
  ...

def set_measurement_metadata(opened_measurement_id, key, value):
  """
        Set the metadata of a measurement, by key string

        :param opened_measurement_id: the measurement id
        :type opened_measurement_id: int
        :param key: the metadata key
        :type key: str
        :param value: the value of the metadata

        """
  ...

def set_measurement_metadata_by_type(opened_measurement_id, meta, value):
  """
        Set the metadata of a measurement, by key int (meta)

        :param opened_measurement_id: the measurement id
        :type opened_measurement_id: int
        :param meta: the metadata
        :type meta: Metadata_t
        :param value: the value of the metadata

        """
  ...

def get_measurement_properties(opened_measurement_id):
  """
        Get the measurement properties

        :param opened_measurement_id: the measurement id
        :type opened_measurement_id: int
        :return: the measurement properties
        :rtype: list of dict
        """
  ...

def add_measurement_property(opened_measurement_id, measurement_properties):
  """
        Add a measurement property, must be called after a start record.

        :param opened_measurement_id: the measurement id
        :type opened_measurement_id: int
        :param measurement_properties: the measurement properties
        :type measurement_properties: dict
        :return: the return code, 0 if success, -1 if invalid openedMeasurementId, -2 if measurement deleted or not ready, -3 if invalid property type, -4 if unable to add property
        :rtype: int
        """
  ...

def add_analyzers(opened_measurement_id, name, sn, disk_name, disk_sn):
  """
        Add an analyzer properties to the measurement

        :param opened_measurement_id: the measurement id
        :type opened_measurement_id: int
        :param name: the name of the analyzer
        :type name: str
        :param sn: the serial number of the analyzer
        :type sn: str
        :param disk_name: the name of the disk
        :type disk_name: str
        :param disk_sn: the serial number of the disk
        :type disk_sn: str
        :return: the return code, 0 if success, -1 if invalid openedMeasurementId, -2 if measurement deleted or not ready
        :rtype: int
        """
  ...

def get_analyzers(opened_measurement_id):
  """
        Get the analyzers of the measurement

        :param opened_measurement_id: the measurement id
        :type opened_measurement_id: int
        :return: the analyzers
        :rtype: list of dict
        """
  ...

def get_channel_metadata_type(opened_measurement_id, channel_index, key):
  """
        Get the metadata type of a channel

        :param opened_measurement_id: the measurement id
        :type opened_measurement_id: int
        :param channel_index: the channel index
        :type channel_index: int
        :param key: the key of the metadata
        :type key: str
        """
  ...

def get_channel_metadata_key_list(opened_measurement_id, channel_index):
  """
        Get the metadata key list of a channel

        :param opened_measurement_id: the measurement id
        :type opened_measurement_id: int
        :param channel_index: the channel index
        :type channel_index: int
        :return: the metadata key list
        :rtype: list
        """
  ...

def get_channel_metadata(opened_measurement_id, channel_index, key=None):
  """
        Get the metadata of a channel, depending on the type of the metadata

        :param opened_measurement_id: the measurement id
        :type opened_measurement_id: int
        :param channel_index: the channel index
        :type channel_index: int
        :param key: the key of the metadata
        :type key: str
        """
  ...

def get_channel_metadata_dict(opened_measurement_id, channel_index):
  """
        Get all metadata of a channel

        :param opened_measurement_id: the measurement id
        :type opened_measurement_id: int
        :param channel_index: the channel index
        :type channel_index: int
        :return: the metadata of the channel
        :rtype: dict
        """
  ...

def set_channel_metadata(opened_measurement_id, channel_index, key, value):
  """
        Set the metadata of a channel, by key string

        :param opened_measurement_id: the measurement id
        :type opened_measurement_id: int
        :param channel_index: the channel index
        :type channel_index: int
        :param meta: the metadata
        :type meta: Metadata_t
        :param value: the value of the metadata
        """
  ...

def set_channel_metadata_by_type(opened_measurement_id, channel_index, meta, value):
  """
        Set the metadata of a channel, by key int (meta)

        :param opened_measurement_id: the measurement id
        :type opened_measurement_id: int
        :param channel_index: the channel index
        :type channel_index: int
        :param meta: the metadata
        :type meta: Metadata_t
        :param value: the value of the metadata
        """
  ...

def get_markers(opened_measurement_id):
  """
        Get the markers of the measurement

        :param opened_measurement_id: the measurement id
        :type opened_measurement_id: int
        :return: the markers
        :rtype: list of dict
        """
  ...

def add_marker(opened_measurement_id, position, comment):
  """
        Add a marker to the measurement, must be called while recording

        :param opened_measurement_id: the measurement id
        :type opened_measurement_id: int
        :param position: the position of the marker
        :type position: float
        :param comment: the comment of the marker
        :type comment: str
        :return: the return code, 0 if success, -1 if invalid openedMeasurementId, -2 if the measurement is not open, -3 if cannot read markers file
        :rtype: int
        """
  ...

def set_record_multi_part(opened_measurement_id, length):
  """
        Set the record multi part

        :param opened_measurement_id: the measurement id
        :type opened_measurement_id: int
        :param length: the length of the multi part, in the NvgsRecordMultiPartMode enum
        :type length: int
        :return: 0 if success, -1 if unknown mode
        :rtype: int
        """
  ...

def start_editing(opened_measurement_id):
  """
        Start the editing of the measurement

        :param opened_measurement_id: the measurement id
        :type opened_measurement_id: int
        :return: the return code, 0 if success, -1 if invalid openedMeasurementId, -2 if the measurement is not open, -3 if unable to start editing
        :rtype: int
        """
  ...

def stop_editing(opened_measurement_id):
  """
        Stop the editing of the measurement

        :param opened_measurement_id: the measurement id
        :type opened_measurement_id: int
        :return: the return code, 0 if success, -1 if invalid openedMeasurementId, -2 if the measurement is not open, -3 if unable to stop editing
        :rtype: int
        """
  ...

def split(opened_measurement_id, first_part_of_new_record):
  """
        Split the record in two parts:
        - First: [begin, firstPartOfNewRecord - 1],
        - Second: [firstPartOfNewRecord, end]
        The part number can be computed with record_duration/NVGS_GetRecordPartLength()
        The opened record becomes the second part.
        This operation cannot be done during recording.

        :param opened_measurement_id: the measurement id
        :type opened_measurement_id: int
        :param first_part_of_new_record: the first part of the new record
        :type first_part_of_new_record: int
        :return: the return code, 0 if success
        :rtype: int
        """
  ...

def erase_part(opened_measurement_id, channel_index, from_part, to_part):
  """
        Set a part to zero to save disk space. The signal duration stay unchanged.
        The number of parts can be computed with record_duration/part_length
        This operation cannot be done during recording.

        :param opened_measurement_id: the measurement id
        :type opened_measurement_id: int
        :param channel_index: the channel index
        :type channel_index: int
        :param from_part: the first part to erase (>= 0)
        :type from_part: int
        :param to_part: the last part to erase (>= 0)
        :type to_part: int
        :return: the return code, 0 if success, -1 if invalid openedMeasurementId, -2 if the measurement is not open, -3 if invalid record index, -4 if unable to erase part
        :rtype: int
        """
  ...

def remove_channel(opened_measurement_id, channel_index):
  """
        Remove one channel
        This operation cannot be done when the record is opened.

        :param opened_measurement_id: the measurement id
        :type opened_measurement_id: int
        :param channel_index: the channel index [1..number of channels]
        :type channel_index: int
        :return: the return code, 0 if success, -1 if invalid openedMeasurementId, -2 if the measurement is not open, -3 if invalid channel index, -4 if unable to remove channel
        :rtype: int
        """
  ...

def remove_record(opened_measurement_id, record_id):
  """
        Remove one record
        This operation cannot be done when the record is opened.

        :param opened_measurement_id: the measurement id
        :type opened_measurement_id: int
        :param record_id: the record id
        :type record_id: int
        :return: the return code, 0 if success, -1 if invalid openedMeasurementId, -2 if the measurement is not open, -3 if invalid record index, -4 if unable to remove record
        :rtype: int
        """
  ...

def initialize_dll():
  """
        Initialize the libraries, needed to load OROS unit inside the dll
        """
  ...
