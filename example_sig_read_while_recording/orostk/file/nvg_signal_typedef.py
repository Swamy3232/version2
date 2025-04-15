"""
This file contains the definition of the NVGate signal types.
It is written accordingly to the .pyx equivalent file.
"""
from enum import Enum


class ReadingStatus(Enum):
	"""
	Define the reading status, from NVGS_IsEndOfReading, for a channel.
	"""
	MeasurementNotOpened = 0
	Unknown = 1  # Unknown status
	RecordReading = 2  # End of current record not reached
	RecordRead = 3  # Reached end of current record
	MeasurementRead = 4  # Reached end of last record, meaning end of measurement


class OSFFChannelType(Enum):
	Dynamic = 0  # Dynamic input
	Parametric = 1  # Slow DC input
	Trigger = 2  # Fast trigger input

	def __int__(self):
		return self.value

	def __str__(self):
		return str(self.name)


class RecordMetadataStr(Enum):
	recordId = "recordId"
	absDate = "absDate"
	relDate = "relDate"
	duration = "duration"
	partLength = "partLength"
	recording = "recording"

	def __str__(self):
		return self.value


class MeasurementMetadata(Enum):
	rec_DateAndTime = 0  # read-only, string, the date of the begining of the record (format ISO8601), initialized when NVGS_StartRecord
	rec_DateDayOfWeek = 1
	rec_ReferenceTime = 2
	rec_Mode = 3  # read-only, string, the mode of record, can be "Start to stop", "Start to time" or "Time to stop"
	rec_Duration = 4
	rec_StartDelay = 5  # float, the delay between the run command (in NvGate) and the begining of the record (in secondes, 0.0 by default)
	rec_NVGateVersion = 6  # string, the version of NvGate used to create the record
	rec_SignalFileName = 7  # read-only, string, the name of the signal file
	rec_ProjectName = 8  # string, the name of the project associated to the record
	rec_UserName = 9  # string, the name of the user who created the record
	rec_MeasurementName = 10  # string, the name of the measure associated to the record
	rec_Comment = 11  # string, the comment associated to the record
	rec_FileSize = 12
	rec_NumberOfChannels = 13
	rec_SampleFormat = 14  # read-only, string, the sample format can be "Normal" or "Compacted"
	rec_SamplingFrontEnd = 15  # read-only, float, the sampling rate of the front-end, also the sampling rate of the trigger input (in samples/s)
	rec_Sampling1 = 16  # read-only, float, the first sampling rate of the dynamic input
	rec_Sampling2 = 17  # read-only, float, the second sampling rate of the dynamic input
	rec_SamplingDC = 18  # read-only, float, the sampling rate of the parametric input

	def __int__(self):
		return self.value


class MeasurementMetadataStr(Enum):
	rec_DateAndTime = "DateAndTime"
	rec_DateDayOfWeek = "DateDayOfWeek"
	rec_ReferenceTime = "ReferenceTime"
	rec_Mode = "Mode"
	rec_Duration = "Duration"
	rec_StartDelay = "StartDelay"
	rec_NVGateVersion = "NVGateVersion"
	rec_SignalFileName = "SignalFileName"
	rec_ProjectName = "ProjectName"
	rec_UserName = "UserName"
	rec_MeasurementName = "MeasurementName"
	rec_Comment = "Comment"
	rec_FileSize = "FileSize"
	rec_NumberOfChannels = "NumberOfChannels"
	rec_SampleFormat = "SampleFormat"
	rec_SamplingFrontEnd = "SamplingFrontEnd"
	rec_Sampling1 = "Sampling1"
	rec_Sampling2 = "Sampling2"
	rec_SamplingDC = "SamplingDC"

	def __str__(self):
		return self.value


def get_measurement_metadata_int_from_str(str_value):
	"""
	Get the measurement metadata int from the C enum given the metadata string value

	:param str_value: The string value of the metadata, from MeasurementMetadataStr
	"""
	for member in MeasurementMetadata:
		if MeasurementMetadataStr[member.name].value == str_value:
			return int(member)
	return None


def get_measurement_metadata_str_from_int(int_value):
	"""
	Get the measurement metadata string from the C enum given the metadata int value

	:param int_value: The int value of the metadata, from MeasurementMetadata
	"""
	for member in MeasurementMetadata:
		if int(member) == int_value:
			return str(MeasurementMetadataStr[member.name].value)
	return None


class MeasurementMetadataStr_Predef(Enum):
	# As defined in predef_metadata_measurement.h
	META_MEAS_DATE = "DateAndTime"
	META_MEAS_DATE_DAY_OF_WEEK = "DateDayOfWeek"
	META_MEAS_EDITING = "Editing"
	META_MEAS_REFERENCE_TIME = "ReferenceTime"
	META_MEAS_MODE = "Mode"
	META_MEAS_DURATION = "Duration"
	META_MEAS_START_DELAY = "StartDelay"
	META_MEAS_NVGATE_VERSION = "NVGateVersion"
	META_MEAS_SIGNAL_FILE_NAME = "SignalFileName"
	META_MEAS_PROJECT_NAME = "ProjectName"
	META_MEAS_USER_NAME = "UserName"
	META_MEAS_MEASUREMENT_NAME = "MeasurementName"
	META_MEAS_COMMENT = "Comment"
	META_MEAS_RECORD_FILES_SIZE = "FileSize"
	META_MEAS_NUMBER_OF_CHANNELS = "NumberOfChannels"
	META_MEAS_SAMPLE_FORMAT = "SampleFormat"
	META_MEAS_SAMPLING_FRONT_END = "SamplingFrontEnd"
	META_MEAS_SAMPLING_1 = "Sampling1"
	META_MEAS_SAMPLING_2 = "Sampling2"
	META_MEAS_SAMPLING_DC = "SamplingDC"
	SAMPLE_FORMAT_NORMAL = "Normal"
	SAMPLE_FORMAT_COMPACTED = "Compacted"
	META_MEAS_CHANNELS = "ChannelsToRemove"

	def __str__(self):
		return self.value


class ChannelMetadata(Enum):
	ch_Name = 0  # string, the name of the recorded channel
	ch_SourceName = 1  # string, the name of the source signal (same as ch_Name by default)
	ch_Coupling = 2  # long, input coupling (0 (default) : AC, 1 : DC, 2 : ICP, 3 : AC float, 4 : DC float, ...)
	ch_RangePeak = 3  # float
	ch_RangeInfo = 4  # float, idem ch_RangePeak by default, the range peak (in SI unit)
	ch_Sensitivity = 5  # float, the input sensitivity (in Volt/SI)
	ch_Offset = 6  # float, the input offset (0 by default)
	ch_PhysicalQuantity = 7  # string, the physical quantity of the channel (must be a valid key from the OROS unit data base)
	ch_Unit = 8  # string, the SI unit label (automatically initialized when changing the physical quantity)
	ch_TranducerId = 9  # string, the transducer id ("None" by default)
	ch_Polarity = 10  # long, 1 (default) or -1
	ch_FreqCorr = 11  # float array of size coeffNb
	ch_NodeNumber = 12  # string, the input node number
	ch_NodeDirection = 13  # string, the input node direction
	ch_NodeComponent = 14  # string, the input node component
	ch_NodeType = 15  # string, the input node type
	ch_IsTacho = 16  # bool, false (default) or true (only for input of type osff_Trigger)
	ch_ExtSyncMode = 17  # long, the trigger mode (0 : trigger, 1 : tacho, 2 : torsionnal, 3 : tors + tach, 4 : sampling, 5 : sampling + tors, 6 : sampling + tach, 7 : sampling + tach + tors) (only for input of type osff_Trigger)
	ch_MissingTeeth = 18  # long, the trigger missing teeth (only for input of type osff_Trigger)
	ch_PulsePerRev = 19  # float, the number of pulse per revolution (only for input of type osff_Trigger)
	ch_PreDivider = 20  # long, the trigger predivider (only for input of type osff_Trigger)
	ch_DeviceName = 21  # string, the input device name
	ch_DeviceType = 22  # string, the input device type
	ch_DeviceVersion = 23  # string, the input device version
	ch_DeviceSN = 24  # string, the input device serial number
	ch_DeviceFWVersion = 25  # string, the input device firmware version
	ch_DiskName = 26  # string, the input device disk name
	ch_DiskSN = 27  # string, the input device disk serial number
	ch_RecordedSource = 28  # string, the idn string of the recorded source

	def __int__(self):
		return self.value


class ChannelMetadataStr(Enum):
	ch_Name = "Name"
	ch_SourceName = "SourceName"
	ch_Coupling = "Coupling"
	ch_RangePeak = "RangePeak"
	ch_RangeInfo = "RangeInfo"
	ch_Sensitivity = "Sensitivity"
	ch_Offset = "Offset"
	ch_PhysicalQuantity = "PhysicalQuantity"
	ch_Unit = "Unit"
	ch_TranducerId = "TransducerID"
	ch_Polarity = "Polarity"
	ch_FreqCorr = "FreqCorr"
	ch_NodeNumber = "NodeNumber"
	ch_NodeDirection = "NodeDirection"
	ch_NodeComponent = "NodeComponent"
	ch_NodeType = "NodeType"
	ch_IsTacho = "IsTach"
	ch_ExtSyncMode = "ExtSyncMode"
	ch_MissingTeeth = "MissingTeeth"
	ch_PulsePerRev = "PulsePerRev"
	ch_PreDivider = "PreDivider"
	ch_DeviceName = "DeviceName"
	ch_DeviceType = "DeviceType"
	ch_DeviceVersion = "DeviceVersion"
	ch_DeviceSN = "DeviceSN"
	ch_DeviceFWVersion = "DeviceFirmWareVersion"
	ch_DiskName = "DeviceDiskName"
	ch_DiskSN = "DeviceDiskSN"
	ch_RecordedSource = "RecSourceID"

	def __str__(self):
		return self.value


def get_channel_metadata_int_from_str(str_value):
	"""
	Get the channel metadata int from the C enum given the metadata string value

	:param str_value: The string value of the metadata, from ChannelMetadataStr
	"""
	for member in ChannelMetadata:
		if ChannelMetadataStr[member.name].value == str_value:
			return int(member)
	return None


def get_channel_metadata_str_from_int(int_value):
	"""
	Get the channel metadata string from the C enum given the metadata int value

	:param int_value: The int value of the metadata, from ChannelMetadata
	"""
	for member in ChannelMetadata:
		if int(member) == int_value:
			return str(ChannelMetadataStr[member.name].value)
	return None


class ChannelMetadataStr_Predef(Enum):
	# As defined in predef_metadata_channel.h
	CHANNEL_NAME = "Name"
	CHANNEL_TYPE = "Type"
	CHANNEL_NUMBER = "Track"
	CHANNEL_DATA_FORMAT = "DataFormat"
	CHANNEL_COUPLING = "Coupling"
	CHANNEL_RANGE_PEAK = "RangePeak"
	CHANNEL_RANGE_INFO = "RangeInfo"
	CHANNEL_SOURCE_ID = "SourceID"
	CHANNEL_REC_SOURCE_ID = "RecSourceID"
	CHANNEL_SOURCE_NAME = "SourceName"
	CHANNEL_SAMPLING_RATE = "SamplingRate"
	CHANNEL_SAMPLING_INDEX = "SamplingIndex"
	CHANNEL_SENSITIVITY = "Sensitivity"
	CHANNEL_OFFSET = "Offset"
	CHANNEL_PHYSICAL_QUANTITY = "PhysicalQuantity"
	CHANNEL_UNIT = "Unit"
	CHANNEL_TRANSDUCER_ID = "TransducerID"
	CHANNEL_POLARITY = "Polarity"
	CHANNEL_ABS_ACCURACY = "AbsAccuracy"
	CHANNEL_FREQUENCY_CORR = "FreqCorr"
	CHANNEL_NODE_NUMBER = "NodeNumber"
	CHANNEL_NODE_DIRECTION = "NodeDirection"
	CHANNEL_NODE_COMPONENT = "NodeComponent"
	CHANNEL_NODE_TYPE = "NodeType"
	CHANNEL_IS_TACH = "IsTach"
	CHANNEL_EXTERNAL_SYNC_MODE = "ExtSyncMode"
	CHANNEL_MISSING_TEETH = "MissingTeeth"
	CHANNEL_PULSE_PER_REV = "PulsePerRev"
	CHANNEL_PREDIVIDER = "PreDivider"

	DEVICE_NAME = "DeviceName"
	DEVICE_HARD_TYPE = "DeviceType"
	DEVICE_VERSION = "DeviceVersion"
	DEVICE_SN = "DeviceSN"
	DECICE_FMW_VERSION = "DeviceFirmWareVersion"
	DEVICE_DISK_NAME = "DeviceDiskName"
	DEVICE_DISK_SN = "DeviceDiskSN"

	CHANNEL_RANGE_INFO_PA = "RangeInfoPostAnalysis"
	CHANNEL_SENSITIVITY_PA = "SensitivityPostAnalysis"
	CHANNEL_OFFSET_PA = "OffsetPostAnalysis"
	CHANNEL_PHYSICAL_QUANTITY_PA = "PhysicalQuantityPostAnalysis"
	CHANNEL_UNIT_PA = "UnitPostAnalysis"
	CHANNEL_TRANSDUCER_ID_PA = "TransducerIDPostAnalysis"
	CHANNEL_NAME_PA = "NamePostAnalysis"

	RECORD_START_DATE_STRING = "RecordStartDateString"
	RECORD_START_DATE = "RecordStartDate"
	RECORD_DURATION = "RecordDuration"
	RECORD_CUMULATIVE_DATE = "RecordCumulativeDate"
	RECORD_RELATIVE_DATE = "RecordRelativeDate"
	RECORD_RELATIVE_DATE_END = "RecordRelativeDateEnd"
	RECORD_NUMBER = "RecordNumber"
	RECORD_SECTIONS = "RecordSections"

	SIGNAL_OFFSET = "SignalOffset"
	SIGNAL_TIME_STEP = "SignalTimeStep"
	SIGNAL_UNCOMP_COEFF = "SignalUncompactCoeff"
	SIGNAL_UNCOMP_OFFSET = "SignalUncompactOffset"
	SIGNAL_COMPRESSION_FACTOR = "CompressionFactor"
	SIGNAL_PART_LENGTH = "PartLength"
	SIGNAL_MAX_RECORD_LENGTH = "MaxRecordLength"
	SIGNAL_LAST_WRITE_POS = "LastWritePos"
	SIGNAL_1ST_STAGE_LAST_WRITE_POS = "FirstStageLastWritePos"

	CHANNEL_TYPE_DYNAMIC = "Dynamic"
	CHANNEL_TYPE_DYN_SIG_OP = "DynSigOp"
	CHANNEL_TYPE_PARAMETRIC = "Parametric"
	CHANNEL_TYPE_PARAM_SIG_OP = "ParamSigOp"
	CHANNEL_TYPE_TORSIONAL = "Torsional"
	CHANNEL_TYPE_TRIGGER = "Trigger"
	CHANNEL_TYPE_TRIGGER_ANALOG = "TriggerAnalog"
	CHANNEL_TYPE_TWIST_STATIC = "TwistStatic"
	CHANNEL_TYPE_SLOW_TWIST = "SlowTwist"
	CHANNEL_FORMAT_SI_FLOAT = "SIFloat"
	CHANNEL_FORMAT_SI_DOUBLE = "SIDouble"
	CHANNEL_FORMAT_COMPACT16 = "Compact16"
	CHANNEL_FORMAT_RAW32 = "Raw32"

	CHANNEL_COUPLING_AC = "AC"
	CHANNEL_COUPLING_DC = "DC"
	CHANNEL_COUPLING_ICP = "ICP"
	CHANNEL_COUPLING_AC_FLT = "AC-FLT"
	CHANNEL_COUPLING_DC_FLT = "DC-FLT"
	CHANNEL_COUPLING_ICP_CHECK = "ICP-CHECK"
	CHANNEL_COUPLING_GND = "GND"
	CHANNEL_COUPLING_ICP_TEDS = "ICP-TEDS"
	CHANNEL_COUPLING_ICP_TEDS_CHECK = "TEDS-CHECK"
	CHANNEL_COUPLING_DC_CAN2 = "DC-CAN2"
	CHANNEL_COUPLING_AC_FLT_ALT = "AC_Flt"
	CHANNEL_COUPLING_DC_FLT_ALT = "DC_Flt"
	CHANNEL_COUPLING_ICP_CHECK_ALT = "Check_ICP"
	CHANNEL_COUPLING_ICP_TEDS_ALT = "ICP_TEDS"
	CHANNEL_COUPLING_ICP_TEDS_CHECK_ALT = "Check_TEDS"
	CHANNEL_EXT_SYNC_TRIGGER = "Trigger"
	CHANNEL_EXT_SYNC_TACH = "Tach"
	CHANNEL_EXT_SYNC_TORSIONAL = "Torsional"
	CHANNEL_EXT_SYNC_TORSIONAL_TACH = "Torsional+Tach"
	CHANNEL_EXT_SYNC_SAMPLING = "Sampling"
	CHANNEL_EXT_SYNC_SAMPLING_TORS = "Sampling+Torsional"
	CHANNEL_EXT_SYNC_SAMPLING_TACH = "Sampling+Tach"
	CHANNEL_EXT_SYNC_SAMPLING_TACH_TORS = "Sampling+Tach+Torsional"

	def __str__(self):
		return self.value


class InputType(Enum):
	INPUT_AC = 0
	INPUT_DC = 1
	INPUT_ICP = 2
	INPUT_AC_FLT = 3
	INPUT_DC_FLT = 4
	INPUT_ICP_CHECK = 5
	INPUT_GND = 6
	INPUT_ICP_TEDS = 7
	INPUT_ICP_TEDS_CHECK = 8
	INPUT_DC_CAN2 = 9


class InputTypeStr(Enum):
	INPUT_AC = "AC"
	INPUT_DC = "DC"
	INPUT_ICP = "ICP"
	INPUT_AC_FLT = "AC-FLT"
	INPUT_DC_FLT = "DC-FLT"
	INPUT_ICP_CHECK = "ICP-CHECK"
	INPUT_GND = "GND"
	INPUT_ICP_TEDS = "ICP-TEDS"
	INPUT_ICP_TEDS_CHECK = "TEDS-CHECK"
	INPUT_DC_CAN2 = "DC-CAN2"


def get_input_type_int_from_str(str_value):
	"""
	Get the input type int from the C enum given the input type string value

	:param str_value: The string value of the input type, from InputTypeStr
	"""
	for member in InputType:
		if InputTypeStr[member.name].value == str_value:
			return int(member.value)
	return None


def get_input_type_str_from_int(int_value):
	"""
	Get the input type string from the C enum given the input type int value

	:param int_value: The int value of the input type, from InputType
	"""
	for member in InputType:
		if int(member) == int_value:
			return str(InputTypeStr[member.name].value)
	return None


class ExtSynchMode(Enum):
	EXT_SYNCH_MODE_TRIGGER = 0
	EXT_SYNCH_MODE_TACHO = 1
	EXT_SYNCH_MODE_TORSIONAL = 2
	EXT_SYNCH_MODE_TORSIONAL_TACHO = 3
	EXT_SYNCH_MODE_SAMPLING = 4
	EXT_SYNCH_MODE_SAMPLING_TORS = 5
	EXT_SYNCH_MODE_SAMPLING_TACHO = 6
	EXT_SYNCH_MODE_SAMPLING_TACHO_TORS = 7


class ExtSynchModeStr(Enum):
	EXT_SYNCH_MODE_TRIGGER = "Trigger"
	EXT_SYNCH_MODE_TACHO = "Tach"
	EXT_SYNCH_MODE_TORSIONAL = "Torsional"
	EXT_SYNCH_MODE_TORSIONAL_TACHO = "Torsional+Tach"
	EXT_SYNCH_MODE_SAMPLING = "Sampling"
	EXT_SYNCH_MODE_SAMPLING_TORS = "Sampling+Torsional"
	EXT_SYNCH_MODE_SAMPLING_TACHO = "Sampling+Tach"
	EXT_SYNCH_MODE_SAMPLING_TACHO_TORS = "Sampling+Tach+Torsional"


def get_ext_synch_mode_int_from_str(str_value):
	"""
	Get the ext synch mode int from the C enum given the ext synch mode string value

	:param str_value: The string value of the ext synch mode, from ExtSynchModeStr
	"""
	for member in ExtSynchMode:
		if ExtSynchModeStr[member.name].value == str_value:
			return int(member.value)
	return None


def get_ext_synch_mode_str_from_int(int_value):
	"""
	Get the ext synch mode string from the C enum given the ext synch mode int value

	:param int_value: The int value of the ext synch mode, from ExtSynchMode
	"""
	for member in ExtSynchMode:
		if int(member) == int_value:
			return str(ExtSynchModeStr[member.name].value)
	return None


class NvgsRecordMultiPartMode(Enum):
	NvgsSinglePartFile = 0
	NvgsShortPart = 1
	NvgsMediumPart = 2
	NvgsLongPart = 3

	def __int__(self):
		return self.value

	def get_time(self):
		if self.name == "NvgsSinglePartFile":
			return 0.0
		elif self.name == "NvgsShortPart":
			return 64.0
		elif self.name == "NvgsMediumPart":
			return 640.0
		elif self.name == "NvgsLongPart":
			return 1920.0
		else:
			return None

	@classmethod
	def get_enum_from_time(cls, time):
		if time is None or time == 0.0:
			return cls.NvgsSinglePartFile
		elif time <= 64.0:
			return cls.NvgsShortPart
		elif time <= 640.0:
			return cls.NvgsMediumPart
		else:
			return cls.NvgsLongPart


class MarkerMetadataStr_Predef(Enum):
	# As defined in predef_metadata_measurement.h
	META_MRK_ABSOLUTE_DATE = "AbsoluteDate"
	META_MRK_DATE_DAY_OF_WEEK = "DateDayOfWeek"
	META_MRK_RELATIVE_DATE = "RelativeDate"
	META_MRK_IDENTIFIER = "ID"
	META_MRK_COMMENT = "Comment"


def is_measurement_metadata_valid(key):
	"""
	Check if the given key is a valid measurement metadata key.

	:param key: The key to check
	:type key: str
	:return: True if the key is a valid measurement metadata key, False otherwise
	:rtype: bool
	"""
	return key in [str(item) for item in MeasurementMetadataStr_Predef]


def is_record_metadata_valid(key):
	"""
	Check if the given key is a valid record metadata key.

	:param key: The key to check
	:type key: str
	:return: True if the key is a valid record metadata key, False otherwise
	:rtype: bool
	"""
	return key in [str(item) for item in RecordMetadataStr]


def is_channel_metadata__valid(key):
	"""
	Check if the given key is a valid channel metadata key.

	:param key: The key to check
	:type key: str
	:return: True if the key is a valid channel metadata key, False otherwise
	:rtype: bool
	"""
	return key in [str(item) for item in ChannelMetadataStr_Predef]


class PropertyType(Enum):
	PropertyTypeUndefined = 0
	PropertyText = 1
	PropertyTextBlock = 2
	PropertyNumeric = 3
	PropertyDateTime = 4
	PropertyBoolean = 5
	PropertyEnumerated = 6

	def __int__(self):
		return self.value

	def __str__(self):
		return str(self.name)