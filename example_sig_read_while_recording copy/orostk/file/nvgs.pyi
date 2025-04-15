import datetime

def get_filetime(dt):
  ...
# ------------------------------------ Overall ------------------------------------
def NVG_NVGateResultFileInitialize():
    pass

# ------------------------------------ Measurements ------------------------------------
# Create a new measurement
# @param recordPath Path to the record
# @param recordName Name of the record
# @param samplingRateBase Base sampling rate of the measurement
# @return The id of the opened measurement
#         -1 : unsupported sampling rate
#         -2 : unable to create measurement
def NVGS_CreateNewMeasurement(const char* recordPath, const char* recordName, float samplingRateBase):
    pass

# Open a measurement (measurement) and load the metadata.
# This function prepares for the data reading and position itself on the first sample of each channel and on the first record.
#
# The first record becomes the current record.
#
# @param[in] measurementPath   Full measurement path (e.g., C:\OROS\NVGate data\Projects\Default Project\Measurement1\)
# @return > 0 if successful, this is the record id used as first parameters for all other functions
#        -1 : invalid path
#        -2 : measurementPath is not a valid measurement path
#        -3 : unable to open measurement
#        -4 : unable to get records list
#        -5 : unable to open first record
#        -6 : unable to get channels list
def NVGS_OpenMeasurement(const char * measurementPath):
    pass

# Opens the current recording in NvGate
# This function prepares for the data reading and position itself on the first sample of each channel and on the first record.
# @param[in] NvDrivePort		The NvDrive socket port number (3000 by default)
# @param[in] NotificationPort	The notification socket port number (4300 by default)
# @param[in] ipAddr			The IP address to access NvGate (127.0.0.1 by default)
# @return > 0 if successful, this is the record id used as first parameters for all other functions
#        -1 : unable to connect to NvGate (NvGate not started or invalid NvDrive port and/or IP address)
# Warning : Until a recording has started (in NvGate) all calls to the metadata or sample reading functions will return 0
def NVGS_OpenNvGateRecord(int NvDrivePort, int NotificationPort, const char * ipAddr):
    pass

# Same as NVGS_OpenNvGateRecord but with default parameters
def NVGS_OpenNvGateRecordDefault():
    pass

# Test if all the signal of channel @p channelIndex has been read
# @param[in]  openedMeasurementId	The value returned by NVGS_OpenMeasurement or NVGS_OpenNvGateRecord
# @param[in]  channelIndex	If in the [1..number of channels] range: the channel index, if 0 then all the recorded channels are tested
# @return :	    2	: NvGate mode : recorder is stopped, nothing more to read, Normal mode : the last record was read completely
#				1	: the end of the current recording has been reached, call NVGS_CloseRecord, NVGS_GetRecordsVect and NVGS_OpenRecord to read next record
#				0	: NvGate mode : record in progress, Normal mode : end of record not reached
#			   -1	: invalid openedMeasurementId
#			   -2	: the measurement is not open
#			   -3	: invalid channel index
def NVGS_IsEndOfReading(OpenedMeasurementId_t openedMeasurementId, int channelIndex):
    pass

# Close the record opened with NVGS_OpenMeasurement
# @param[in]  openedMeasurementId		The value returned by NVGS_OpenMeasurement
# @return 0 if successful
#        -1 : invalid openedMeasurementId
#        -2 : the measurement is not open
def NVGS_CloseMeasurement(OpenedMeasurementId_t openedMeasurementId):
    pass

# Close all the records opened with NVGS_CreateNewMeasurement or NVGS_OpenMeasurement
# @return 0 if successful
def NVGS_CloseAllMeasurements():
    pass

# Returns the list of all the records found in the subdirectories of the directory @p searchPath passed as parameter.
# @param[in]	searchPath	The path in which to search for records
# @param[out]	recordsList	Returns all the records found in the directory @p searchPath
#             The function allocates a new NvgsMeasurementPathArray_t structure.
#             You're responsible for deallocating the data with NVGS_FreeMeasurementPathArray.
# @return the number of records found if >= 0,
#        -1 if search error
def NVGS_SearchMeasurements(const char* searchPath, NvgsMeasurementPathArray_t** recordsList):
    pass

# Read the full measurement path
# @return nullptr in case of error or the full path of the measurement (UTF8).
# The function allocates a NvgsString_t structure, you're responsible for deallocating this using NVGS_FreeString.
# @return the measurementPath
def NVGS_GetMeasurementPath(OpenedMeasurementId_t openedMeasurementId):
    pass

# ------------------------------------ Record ------------------------------------
# Start the record
# @param[in]  openedMeasurementId	The value returned by NVGS_CreateNewMeasurement
# @param[in]  utcDate               The UTC date of the first sample (UTC date in number of step of 100 ns since 01/01/1601, Windows format),
# @returns 0 if successful
#			-1 : invalid openedMeasurementId
#			-2 : measurement deleted or not ready
#			-3 : channel list is empty
#			-4 : unable to save record metadata
#			-5 : unable to update channel metadata
#			-6 : unable to start record
def NVGS_StartRecord(OpenedMeasurementId_t openedMeasurementId, uint64_t utcDate):
    pass

# Stop and close the record
# @param[in]  openedMeasurementId		The value returned by NVGS_CreateNewMeasurement
# @returns 0 if successful
#			-1 : invalid openedMeasurementId
#			-2 : unable to update metadata
def NVGS_StopRecord(OpenedMeasurementId_t openedMeasurementId):
    pass

# Returns the list of records of the current measurement
# @param[in]  openedMeasurementId		The value returned by NVGS_OpenMeasurement
# @param[out] records			The list of records (for each records the MetadataRecord object contains : the record id, the absolute start date of the record,
#                             the relative start date from the begining of the fist record and the legnth of the record)
#                             The function allocates a new NvgsMetadataRecordArray_t structure.
#                             You're responsible for deallocating the data with NVGS_FreeMetadataRecordArray.
# @return >= 0 if successful, this is the number of records
#         0: for NvGate record: recorder not started
#        -1 : invalid openedMeasurementId
#        -2 : the measurement is not open
#        -3 : measurement is empty
def NVGS_GetRecordsVect(OpenedMeasurementId_t openedMeasurementId, NvgsMetadataRecordArray_t** records):
    pass

# Lists all records of a measurement
# @param[in]  openedMeasurementId The value returned by NVGS_OpenMeasurement
# @param[out] list                int64_t array
# @return 1 if successful,
#         0 : for NvGate record : recorder not started
#        -1 : invalid openedMeasurementId
#        -2 : the measurement is not open
#        -3 : cannot list records
# The function allocates a new NvgsFloatArray_t structure.
# You're responsible for deallocating the data with NVGS_FreeFloatArray.
def NVGS_ListRecords(OpenedMeasurementId_t openedMeasurementId, NvgsUInt64Array_t** list):
    pass

# Change the current record
# @param[in]  openedMeasurementId		The value returned by NVGS_OpenMeasurement
# @param[in]  The record id
# @return 1 if successful,
#         0 : for NvGate record : recorder not started or renaming
#        -1 : invalid openedMeasurementId
#        -2 : the measurement is not open
#		 -3 : record already opened
#		 -4 : unable to open record
def NVGS_OpenRecord(OpenedMeasurementId_t openedMeasurementId, uint64_t recordId):
    pass

# Close the current record
# @param[in]  openedMeasurementId		The value returned by NVGS_OpenMeasurement
# @return 1 if successful,
#         0 : for NvGate record : recorder not started
#        -1 : invalid openedMeasurementId
#        -2 : the measurement is not open
#        -3 : invalid record index
def NVGS_CloseRecord(OpenedMeasurementId_t openedMeasurementId):
    pass

# Returns the index of the opened record.
# @param[in]  openedMeasurementId		The value returned by NVGS_OpenMeasurement
# @return >= 1 if successful,
#         0 : For NvGate record : recorder not started or renaming
#        -1 : invalid openedMeasurementId
#        -2 : the measurement is not open
def NVGS_OpenedRecordIndex(OpenedMeasurementId_t openedMeasurementId):
    pass

# Returns the record length in seconds
# @param[in]  openedMeasurementId	The value returned by NVGS_OpenMeasurement
# @returns part length in seconds
#          0: multi-part disabled
#         -1: record not found
#         -2: no channel(s)
def NVGS_GetRecordLength(OpenedMeasurementId_t openedMeasurementId):
    pass

# ------------------------------------ Channel ------------------------------------
# Add a channel to the record
#
# The type of the channels can be  "osff_Dynamic", "osff_Parametric" or "osff_Trigger".
#
# By default, all the channels have 1 and 0 as values for the parameters A and B used to convert samples from user unit to SI unit.
# Use the NVGS_SetChannelCoeffToSI function to initialize these coefficients if unit conversion is required.
#
# Their type is  "Potential_Difference" with unit Volt.
#
# The coupling is "AC" and their name is constructed as "Input X".
#
# @param[in]  openedMeasurementId		The value returned by NVGS_CreateNewMeasurement
# @param[in]  type			The channel type
# @param[in]  samplingRate	The sampling rate of the channel (in samples/s).
#								For osff_Dynamic channel type the sampling rate should be a sub multiple of the base sampling rate.
#								For osff_Parametric channel type the sampling rate should be 12.5 or 15 spl/s.
#								For osff_Trigger channel type the sampling rate should be the base sampling rate.
# @return > 0 : returns the new channel index (value to use as parameter in other functions)
#			-1 : invalid openedMeasurementId
#			-2 : measurement deleted or not ready
#			-3 : invalid sampling rate
#			-4 : unable to create a new record
#			-5 : unable to add a new channel
def NVGS_AddChannel(OpenedMeasurementId_t openedMeasurementId, OSFFChannelType_t typeChannel, float samplingRate):
    pass

# Returns the list of channels name
# @param[in]  openedMeasurementId		The value returned by NVGS_OpenMeasurement
# @param[out] channelList		The list of channels name (string UTF8)
#                             The function allocates a new NvgsStringArray_t structure.
#                             You're responsible for deallocating the data with NVGS_FreeStringArray.
# @return >= 0 if successful, this is the number of channels
#        -1 : invalid openedMeasurementId
#        -2 : the measurement is not open
def NVGS_GetChannelList(OpenedMeasurementId_t openedMeasurementId, NvgsStringArray_t** channelList):
    pass

# Initialize the unit conversion coefficient of a channel. These coefficients are used to convert the samples to SI units.
# Call this function only if the source samples are not in SI units. The conversion formula is :
# sample_si = sample_not_si * coeffToSI + offsetToSI;
# @param[in]  openedMeasurementId		The value returned by NVGS_CreateNewMeasurement
# @param[in]  channelIndex	The channel index to modify [1...number of channels]
# @param[in]  coeffToSI		Conversion multiplier
# @param[in]  offsetToSI		Offset conversion
# @returns 0 if successful
#			-1 : invalid openedMeasurementId
#			-2 : measurement deleted or not ready
#			-3 : invalid channel index
def NVGS_SetChannelCoeffToSI(OpenedMeasurementId_t openedMeasurementId, int channelIndex,float coeffToSI, float offsetToSI):
    pass

# ------------------------------------ Writing ------------------------------------
def NVGS_WriteSampleBlock(OpenedMeasurementId_t openedMeasurementId, int channelIndex, const float* data,unsigned int sampleCount):
    pass

# ------------------------------------ Reading ------------------------------------
# Returns the current read position for one channel
# @param[in]  openedMeasurementId		The value returned by NVGS_OpenMeasurement
# @param[in]  channelIndex	The channel index [1..number of channels]
# @param[out] recordId		Returns the current record id
# @param[out] sampleIndex		Returns the current samples index [0..number of samples in the current record]
# @return 1 if successful,
#         0 : for NvGate record : recorder not started or renaming
#        -1 : invalid openedMeasurementId
#        -2 : the measurement is not open
#        -3 : invalid channel index
#        -4 : invalid sampling rate for channel @p channelIndex
def NVGS_GetReadPosition(OpenedMeasurementId_t openedMeasurementId, int channelIndex, uint64_t* recordId,uint64_t* sampleIndex):
    pass

# Set read position (for all channels)
# @param[in]  openedMeasurementId		The value returned by NVGS_OpenMeasurement
# @param[in]  		The record index [1..number of records]
# @param[in]  fTime			Position relative dans l'enregistrement (en secondes)
# @return 1 if successful,
#         0 : for NvGate record : recorder not started
#        -1 : invalid openedMeasurementId
#        -2 : the measurement is not open
#        -3 : invalid record index
#		 -4 : unable to set read position
def NVGS_SetReadPosition(OpenedMeasurementId_t openedMeasurementId, float fTime):
    pass

# Read a block of samples from the channel @p channelIndex in the current record. The samples are read in, SI unit
# @param[in]  openedMeasurementId		The value returned by NVGS_OpenMeasurement
# @param[in]  channelIndex	The channel index [1..number of channels]
# @param[out] data			Pointer on the destination samples array (array size must be >= @p sampleCount)
# @param[in]  sampleCount		The number of samples to read
# @return >=0 if successful, this is the number of samples read (< sampleCount if the end of the record has been reached)
#        -1 : invalid openedMeasurementId
#        -2 : the measurement is not open
#        -3 : invalid channel index
#        -4 : read error
# Read position can be changed using NVGS_SetReadPosition
def NVGS_ReadSampleBlock(OpenedMeasurementId_t openedMeasurementId, int channelIndex, float* data,unsigned long sampleCount):
    pass

# Retrieves the compressed signal of a channel between 2 dates. The samples are read in, SI unit
# @param[in]  openedMeasurementId		The value returned by NVGS_OpenMeasurement
# @param[in]  channelIndex	The channel index [1..number of channels]
# @param[in]  start			Relative start position from the beginning of the record (in seconds).
#								If it is a multi-record, the relative date uses the cumulative durations of the records to determine the reading position
#								(without taking into account the durations between 2 records)
# @param[in]  stop			Relative stop position from the beginning of record (in secondes)
#								If it is a multi-record, the relative @p stop date may not be in the same record as the relative @p start date.
#								All records between the @p start and @p stop dates are compressed as if they were consecutive.
# @param[in]  requested		Minimum number of min/max pairs requested
# @param[out] dest			Destination vector of the compressed signal (min/max pairs, the size of the vector is set by the function)
#                             The function allocates a new NvgsFloatArray_t structure.
#                             You're responsible for deallocating the data with NVGS_FreeFloatArray.
# @return > 0 if successful, this is the number of min/max pairs in the compressed vector
#        -1 : invalid openedMeasurementId
#        -2 : the measurement is not open
#        -3 : invalid channel index
#        -4 : compress error
def NVGS_GetCompressedSignal(OpenedMeasurementId_t openedMeasurementId, int channelIndex, float start, float stop,unsigned long requested, NvgsFloatArray_t** dest):
    pass

# ------------------------------------ Measurement Metadata ------------------------------------
# Returns the list of metadata keys of the record
# @param[in]  openedMeasurementId	The value returned by NVGS_OpenMeasurement
# @param[out] metadataList	The function allocates the list of metadata keys for the record (UTF8 string)
#                             You're responsible for deallocating the data with NVGS_FreeStringArray.
# @return >= 0 if successful, this is the number of keys in the list
#        -1 : invalid openedMeasurementId
#        -2 : the measurement is not open
def NVGS_GetMeasurementMetadataKeyList(OpenedMeasurementId_t openedMeasurementId, NvgsStringArray_t** metadataList):
    pass

# Returns the type of a record metadata
# @param[in]  openedMeasurementId  The value returned by NVGS_OpenMeasurement
# @param[in]  key                 A metadata key returned by NVGS_GetMeasurementMetadataKeyList
# @return Returns the type of metadata (string, float, long , bool, unknown...)
def NVGS_GetMeasurementMetadataType(OpenedMeasurementId_t openedMeasurementId, const char * key):
    pass

# Returns the value of a record metadata
# @param[in]  openedMeasurementId		The value returned by NVGS_OpenMeasurement
# @param[in]  key				The key of the metadata (one of the keys returned by NVGS_GetMeasurementMetadataKeyList)
# @param[out] value			The value of the metadate (UTF8 string, float, double, long or long long)
#                             For strings, the function allocates a new NvgsString_t structure.
#                             You're responsible for deallocating the data with NVGS_FreeString.
# @return 1 if successful,
#         0 : for NvGate record : recorder not started
#        -1 : invalid openedMeasurementId
#        -2 : the measurement is not open
#        -3 : metadata key not valid / not found
def NVGS_GetMeasurementMetadataString(OpenedMeasurementId_t openedMeasurementId, const char* key, NvgsString_t** value):
    pass

def NVGS_GetMeasurementMetadataFloat(OpenedMeasurementId_t openedMeasurementId, const char* key, float* value):
    pass

def NVGS_GetMeasurementMetadataDouble(OpenedMeasurementId_t openedMeasurementId, const char* key, double* value):
    pass

def NVGS_GetMeasurementMetadataBool(OpenedMeasurementId_t openedMeasurementId, const char* key, int* value):
    pass

def NVGS_GetMeasurementMetadataLong(OpenedMeasurementId_t openedMeasurementId, const char* key, long* value):
    pass

def NVGS_GetMeasurementMetadataLongLong(OpenedMeasurementId_t openedMeasurementId, const char* key, long long* value):
    pass

def NVGS_GetMeasurementMetadataFloatArray(OpenedMeasurementId_t openedMeasurementId, const char* key, NvgsFloatArray_t** value):
    pass

def NVGS_GetMeasurementMetadataLongArray(OpenedMeasurementId_t openedMeasurementId, const char* key, NvgsLongArray_t** value):
    pass

def NVGS_GetMeasurementMetadataUInt64Array(OpenedMeasurementId_t openedMeasurementId, const char* key, NvgsUInt64Array_t** value):
    pass

# Change the value of a record metadata of type string
# @param[in]  openedMeasurementId		The value returned by NVGS_CreateNewMeasurement
# @param[in]  meta			The type of metadata to modify
# @param[in]  value			The new value of the metadata
# @returns 0 if successful
#			-1 : invalid openedMeasurementId
#			-2 : measurement deleted or not ready
#			-3 : invalid metadata type
#			-4 : non-editable metadata
def NVGS_SetMeasurementMetadataStringByType(OpenedMeasurementId_t openedMeasurementId, RecordMetadata_t meta,const char* value):
    pass

# Change the value of a record metadata of type string
# @param[in]  openedMeasurementId		The value returned by NVGS_CreateNewMeasurement
# @param[in]  key			The key of metadata to modify
# @param[in]  value			The new value of the metadata
# @returns 0 if successful
#			-1 : invalid openedMeasurementId
#			-2 : measurement deleted or not ready
#			-3 : invalid metadata type
#			-4 : non-editable metadata
#			-5 : if the key is not valid
def NVGS_SetMeasurementMetadataString(OpenedMeasurementId_t measurementId, const char * key, const char* value):
    pass

# Change the value of a record metadata of type float
# @param[in]  openedMeasurementId		The value returned by NVGS_CreateNewMeasurement
# @param[in]  meta			The type of metadata to modify
# @param[in]  value			The new value of the metadata
# @returns 0 if successful
#			-1 : invalid openedMeasurementId
#			-2 : measurement deleted or not ready
#			-3 : invalid metadata type
#			-4 : non-editable metadata
def NVGS_SetMeasurementMetadataFloatByType(OpenedMeasurementId_t openedMeasurementId, RecordMetadata_t meta,float value):
    pass

# Change the value of a record metadata of type float
# @param[in]  openedMeasurementId		The value returned by NVGS_CreateNewMeasurement
# @param[in]  key			The key of metadata to modify
# @param[in]  value			The new value of the metadata
# @returns 0 if successful
#			-1 : invalid openedMeasurementId
#			-2 : measurement deleted or not ready
#			-3 : invalid metadata type
#			-4 : non-editable metadata
#			-5 : if the key is not valid
def NVGS_SetMeasurementMetadataFloat(OpenedMeasurementId_t measurementId, const char * key, float value):
    pass

# ------------------------------------ Measurement Properties ------------------------------------
# Returns the list of the NvGate measurement properties
# @param[in]  openedMeasurementId		The value returned by NVGS_OpenMeasurement
# @param[out] list			The list of measurement properties
#                             The function allocates a new NvgsMeasurementPropertyValueArray_t structure.
#                             You're responsible for deallocating the data with NVGS_FreeMetadataMeasurementPropertyValueArray.
# @return >= 0 if successful, this is the number of properties
#         0: for NvGate record: recorder not started
#        -1 : invalid openedMeasurementId
#        -2 : the measurement is not open
#        -4 : malloc failed
def NVGS_GetMeasurementProperties(OpenedMeasurementId_t openedMeasurementId, NvgsMeasurementPropertyValueArray_t** list):
    pass

# Add a property to the measurement
# @param[in] openedMeasurementId		The value returned by NVGS_OpenMeasurement
# @param[in] prop					The property to add
# @return >= 0 if successful, this is the number of properties
#        -1 : invalid openedMeasurementId
#        -2 : the measurement is not open
def NVGS_AddMeasurementProperty(OpenedMeasurementId_t openedMeasurementId, const MeasurementPropertyValue* prop):
    pass

# Add a set of metadata of an analyzer used to record the channels
# @param[in]  openedMeasurementId		The value returned by NVGS_CreateNewMeasurement
# @param[in]  name			The name of the analyzer
# @param[in]  sn				The serial number of the analyzer
# @param[in]  diskName		The name of the analyzer disk
# @param[in]  diskSn			The serial number of the analyzer disk
# @returns 0 if successful
#			-1 : invalid openedMeasurementId
#			-2 : measurement deleted or not ready
def NVGS_AddAnalyzer(OpenedMeasurementId_t openedMeasurementId, const char* name, const char* sn,const char* diskName, const char* diskSn):
    pass

# Returns the list of analyzers metadata
# @param[in]  openedMeasurementId		The value returned by NVGS_OpenMeasurement
# @param[out] analyzers		The list of analyzers metadata (for each analyzer the MetadataAnalyzer object contains : the name of the analyzer, the serial number of the analyzer,
#                             the name of the disk and the serial number of the disk)
#                             The function allocates a new NvgsMetadataAnalyzerArray_t structure.
#                             You're responsible for deallocating the data with NVGS_FreeMetadataAnalyzerArray.
# @return >= 0 if successful, this is the number of analyzers
#         0: for NvGate record: recorder not started
#        -1 : invalid openedMeasurementId
#        -2 : the measurement is not open
def NVGS_GetAnalyzers(OpenedMeasurementId_t openedMeasurementId, NvgsMetadataAnalyzerArray_t** analyzers):
    pass

# ------------------------------------ Channel Metadata ------------------------------------
# Returns the list of metadata keys of a channel
# @param[in]  openedMeasurementId		The value returned by NVGS_OpenMeasurement
# @param[in]  channelIndex	The channel index [1..number of channels]
# @param[out] metadataList	Returns the list of metadata keys for the channel (UTF8 string)
#                             The function allocates a new NvgsStringArray_t structure.
#                             You're responsible for deallocating the data with NVGS_FreeStringArray.
# @return >= 0 if successful, this is the number of keys in the list
#        -1 : invalid openedMeasurementId
#        -2 : the measurement is not open
#        -3 : invalid channel index
def NVGS_GetChannelMetadataKeyList(OpenedMeasurementId_t openedMeasurementId, int channelIndex, NvgsStringArray_t** metadataList):
    pass

# Returns the type of a channel metadata
# @param[in]  openedMeasurementId		The value returned by NVGS_OpenMeasurement
# @param[in]  channelIndex	The channel index [1..number of channels]
# @param[in]  key				A metadata key returned by NVGS_GetMeasurementMetadataKeyList
# @return Returns the type of metadata (string, float, long , bool, unknown...)
def NVGS_GetChannelMetadataType(OpenedMeasurementId_t openedMeasurementId, int channelIndex, const char * key):
    pass

# Returns the value of a channel metadata
# @param[in]  openedMeasurementId		The value returned by NVGS_OpenMeasurement
# @param[in]  channelIndex	The channel index [1..number of channels]
# @param[in]  key				The key of the metadata (one of the keys returned by NVGS_GetChannelMetadataKeyList)
# @param[out] value			The value of the metadate (UTF8 string, float, double,long, long long bool or vector of float)
#                             For strings, the function allocates a new NvgsString_t structure.
#                             You're responsible for deallocating the data with NVGS_FreeString.
#                             For float array, the function allocates a new NvgsFloatArray_t structure.
#                             You're responsible for deallocating the data with NVGS_FreeFloatArray.
# @return 1 if successful,
#         0 : for NvGate record : recorder not started
#        -1 : invalid openedMeasurementId
#        -2 : the measurement is not open
#        -3 : invalid channel index
#        -4 : metadata key not valid / not found
def NVGS_GetChannelMetadataString(OpenedMeasurementId_t openedMeasurementId, int channelIndex, const char * key,NvgsString_t** value):
    pass

def NVGS_GetChannelMetadataFloat(OpenedMeasurementId_t openedMeasurementId, int channelIndex, const char * key,float * value):
    pass

def NVGS_GetChannelMetadataDouble(OpenedMeasurementId_t openedMeasurementId, int channelIndex, const char * key,double * value):
    pass

def NVGS_GetChannelMetadataLong(OpenedMeasurementId_t openedMeasurementId, int channelIndex, const char * key,long * value):
    pass

def NVGS_GetChannelMetadataLongLong(OpenedMeasurementId_t openedMeasurementId, int channelIndex, const char * key,long long * value):
    pass

def NVGS_GetChannelMetadataBool(OpenedMeasurementId_t openedMeasurementId, int channelIndex, const char * key,int * value):
    pass

def NVGS_GetChannelMetadataFloatArray(OpenedMeasurementId_t openedMeasurementId, int channelIndex, const char * key,NvgsFloatArray_t** value):
    pass

def NVGS_GetChannelMetadataLongArray(OpenedMeasurementId_t openedMeasurementId, int channelIndex, const char * key,NvgsLongArray_t** value):
    pass

def NVGS_GetChannelMetadataUInt64Array(OpenedMeasurementId_t openedMeasurementId, int channelIndex, const char * key,NvgsUInt64Array_t** value):
    pass

# Change the value of a channel metadata of type string
# @param[in]  openedMeasurementId		The value returned by NVGS_CreateNewMeasurement
# @param[in]  channelIndex	The channel index to modify [1...number of channels]
# @param[in]  meta			The type of metadata to modify
# @param[in]  value			The new value of the metadata (UTF8)
# @returns 0 if successful
#			-1 : invalid openedMeasurementId
#			-2 : measurement deleted or not ready
#			-3 : invalid channel index
#			-4 : invalid metadata type
#			-5 : invalid physical quantity
def NVGS_SetChannelMetadataStringByType(OpenedMeasurementId_t openedMeasurementId, int channelIndex,ChannelMetadata_t meta, const char * value):
    pass

# Change the value of a channel metadata of type string
# @param[in]  openedMeasurementId		The value returned by NVGS_CreateNewMeasurement
# @param[in]  channelIndex	The channel index to modify [1...number of channels]
# @param[in]  key			The key of metadata to modify
# @param[in]  value			The new value of the metadata (UTF8)
# @returns 0 if successful
#			-1 : invalid openedMeasurementId
#			-2 : measurement deleted or not ready
#			-3 : invalid channel index
#			-4 : invalid metadata type
#			-5 : invalid physical quantity
#			-6 : invalid key
def NVGS_SetChannelMetadataString(OpenedMeasurementId_t measurementId, int channelIndex, const char * key,const char * value):
    pass

# Change the value of a channel metadata of type float
# @param[in]  openedMeasurementId		The value returned by NVGS_CreateNewMeasurement
# @param[in]  channelIndex	The channel index to modify [1...number of channels]
# @param[in]  meta			The type of metadata to modify
# @param[in]  value			The new value of the metadata
# @returns 0 if successful
#			-1 : invalid openedMeasurementId
#			-2 : measurement deleted or not ready
#			-3 : invalid channel index
#			-4 : invalid metadata type
#			-5 : invalid physical quantity
def NVGS_SetChannelMetadataFloatByType(OpenedMeasurementId_t openedMeasurementId, int channelIndex,ChannelMetadata_t meta, float value):
    pass

# Change the value of a channel metadata of type float
# @param[in]  openedMeasurementId		The value returned by NVGS_CreateNewMeasurement
# @param[in]  channelIndex	The channel index to modify [1...number of channels]
# @param[in]  key			The key of metadata to modify
# @param[in]  value			The new value of the metadata
# @returns 0 if successful
#			-1 : invalid openedMeasurementId
#			-2 : measurement deleted or not ready
#			-3 : invalid channel index
#			-4 : invalid metadata type
#			-5 : invalid physical quantity
#			-6 : invalid key
def NVGS_SetChannelMetadataFloat(OpenedMeasurementId_t measurementId, int channelIndex, const char * key, float value):
    pass

# Change the value of a channel metadata of type long
# @param[in]  openedMeasurementId		The value returned by NVGS_CreateNewMeasurement
# @param[in]  channelIndex	The channel index to modify [1...number of channels]
# @param[in]  meta			The type of metadata to modify
# @param[in]  value			The new value of the metadata
# @returns 0 if successful
#			-1 : invalid openedMeasurementId
#			-2 : measurement deleted or not ready
#			-3 : invalid channel index
#			-4 : invalid metadata type
#			-5 : invalid metadata value
def NVGS_SetChannelMetadataLongByType(OpenedMeasurementId_t openedMeasurementId, int channelIndex,ChannelMetadata_t meta, long value):
    pass

# Change the value of a channel metadata of type long
# @param[in]  openedMeasurementId		The value returned by NVGS_CreateNewMeasurement
# @param[in]  channelIndex	The channel index to modify [1...number of channels]
# @param[in]  key			The key of metadata to modify
# @param[in]  value			The new value of the metadata
# @returns 0 if successful
#			-1 : invalid openedMeasurementId
#			-2 : measurement deleted or not ready
#			-3 : invalid channel index
#			-4 : invalid metadata type
#			-5 : invalid metadata value
#			-6 : invalid key
def NVGS_SetChannelMetadataLong(OpenedMeasurementId_t measurementId, int channelIndex, const char * key, long value):
    pass

# Change the value of a channel metadata of type bool
# @param[in]  openedMeasurementId		The value returned by NVGS_CreateNewMeasurement
# @param[in]  channelIndex	The channel index to modify [1...number of channels]
# @param[in]  meta			The type of metadata to modify
# @param[in]  value			The new value of the metadata (0 or 1)
# @returns 0 if successful
#			-1 : invalid openedMeasurementId
#			-2 : measurement deleted or not ready
#			-3 : invalid channel index
#			-4 : invalid metadata type
#			-5 : invalid metadata value
def NVGS_SetChannelMetadataBoolByType(OpenedMeasurementId_t openedMeasurementId, int channelIndex,ChannelMetadata_t meta, int value):
    pass

# Change the value of a channel metadata of type bool
# @param[in]  openedMeasurementId		The value returned by NVGS_CreateNewMeasurement
# @param[in]  channelIndex	The channel index to modify [1...number of channels]
# @param[in]  key			The key of metadata to modify
# @param[in]  value			The new value of the metadata (0 or 1)
# @returns 0 if successful
#			-1 : invalid openedMeasurementId
#			-2 : measurement deleted or not ready
#			-3 : invalid channel index
#			-4 : invalid metadata type
#			-5 : invalid metadata value
#			-6 : invalid key
def NVGS_SetChannelMetadataBool(OpenedMeasurementId_t measurementId, int channelIndex, const char * key, int value):
    pass

# Change the value of a channel metadata of type array of float
# The channel metadata of type array of float are:
# - ch_FreqCorr : the frequency correction coefficient of the input (only for osff_Dynamic channel type)
# @param[in]  openedMeasurementId		The value returned by NVGS_CreateNewMeasurement
# @param[in]  channelIndex	The channel index to modify [1...number of channels]
# @param[in]  meta			The type of metadata to modify
# @param[in]  value			The pointer on the array of float
# @param[in]  coeffNb			The number of float coefficients in the array
# @returns 0 if successful
#			-1 : invalid openedMeasurementId
#			-2 : measurement deleted or not ready
#			-3 : invalid channel index
#			-4 : invalid metadata type
def NVGS_SetChannelMetadataFloatArrayByType(OpenedMeasurementId_t openedMeasurementId, int channelIndex,ChannelMetadata_t meta, const float* value, unsigned int coeffNb):
    pass

# Change the value of a channel metadata of type array of float
# The channel metadata of type array of float are:
# - ch_FreqCorr : the frequency correction coefficient of the input (only for osff_Dynamic channel type)
# @param[in]  openedMeasurementId		The value returned by NVGS_CreateNewMeasurement
# @param[in]  channelIndex	The channel index to modify [1...number of channels]
# @param[in]  key			The key of metadata to modify
# @param[in]  value			The pointer on the array of float
# @param[in]  coeffNb			The number of float coefficients in the array
# @returns 0 if successful
#			-1 : invalid openedMeasurementId
#			-2 : measurement deleted or not ready
#			-3 : invalid channel index
#			-4 : invalid metadata type
#			-5 : invalid key
def NVGS_SetChannelMetadataFloatArray(OpenedMeasurementId_t measurementId, int channelIndex, const char * key,const float * value, unsigned int coeffNb):
    pass

# ------------------------------------ Markers ------------------------------------
# Returns the list of markers
# @param[in]  openedMeasurementId		The value returned by NVGS_OpenMeasurement
# @param[out] markers			The list of markers (for each markers the MetadataMarker object contains : the marker id, the absolute date of the marker,
#                             the relative date from the begining of the record, the relative date from the beginig of the first record and the comment of the marker)
#                             The function allocates a new NvgsMetadataMarkerArray_t structure.
#                             You're responsible for deallocating the data with NVGS_FreeMetadataMarkerArray.
# @return >= 0 if successful, this is the number of markers
#         0: for NvGate record: recorder not started
#        -1 : invalid openedMeasurementId
#        -2 : the measurement is not open
#        -3 : cannot read markers file
def NVGS_GetMarkers(OpenedMeasurementId_t openedMeasurementId, NvgsMetadataMarkerArray_t** markers):
    pass

# Add a new marker (must be called while recording)
# @param[in]  openedMeasurementId		The value returned by NVGS_OpenMeasurement
# @param[in]  position            Position in the record in second
# @param[in]  comment             Comment on the marker
# @return >= 0 if successful, this is the number of markers
#        -1 : invalid openedMeasurementId
#        -2 : the measurement is not open
#        -3 : cannot write markers file
def NVGS_AddMarker(OpenedMeasurementId_t openedMeasurementId, double position, const char * comment):
    pass

# ------------------------------------ MultiParts ------------------------------------
# Record signal in differents files of fixed length.
# Default value is NvgsSignalPartFile. Must be called before NVGS_StartRecord.
# @param[in]  length
#
# @returns 0 if successful
#			-1 : unknown mode
def NVGS_SetRecordMultiPart(NvgsRecordMultiPartMode length):
    pass

# ------------------------------------ Editing ------------------------------------
# Lock the measurement for editing
# Recording can continue while editing is done but no other editing can be done meantime.
# @param[in]  openedMeasurementId		The value returned by NVGS_OpenMeasurement
# @return 0 if successful
#        -1 : invalid openedMeasurementId
#		 -2 : unable to lock measurement for editing
def NVGS_StartEditing(OpenedMeasurementId_t openedMeasurementId):
    pass

# Unlock the measurement for editing
# @param[in]  openedMeasurementId		The value returned by NVGS_OpenMeasurement
# @return 0 if successful
#        -1 : invalid openedMeasurementId
#		 -2 : unable to unlock measurement for editing
def NVGS_StopEditing(OpenedMeasurementId_t openedMeasurementId):
    pass

# Split the record in two parts :
#  - First : [begin, firstPartOfNewRecord - 1],
#  - Second : [firstPartOfNewRecord, end]
# The part number can be computed with record_duration/part_length
# The opened record becomes the second part.
# The measurement must be lock for editing with start_editing().
# @param[in] openedMeasurementId		The value returned by NVGS_OpenMeasurement
# @param[in] firstPartOfNewRecord first part of the new record.
# @return 0 if successful
#        -1 : invalid openedMeasurementId
#        -3 : the signal is being recorded
#        -4 : unable to split record
def NVGS_Split(OpenedMeasurementId_t openedMeasurementId, int firstPartOfNewRecord):
    pass

# Set a part to zero to save disk space. The signal duration stay unchanged.
# The number of parts can be computed with record_duration/NVGS_GetRecordPartLength()
# The measurement must be lock for editing with NVGS_StartEditing.
# @param[in] openedMeasurementId  The value returned by NVGS_OpenMeasurement
# @param[in] channelIndex  The channel index [1..number of channels]
# @param[in] from  First part to erase (>= 0)
# @param[in] to  Last part to erase (>= 0)
# @return 0 if successful
#        -1 : invalid openedMeasurementId
#        -2 : invalid channelIndex
#        -3 : the signal is being recorded
#        -4 : the part(s) cannot be removed
def NVGS_ErasePart(OpenedMeasurementId_t openedMeasurementId, int channelIndex, int from_part, int to_part):
    pass

# Remove one channel
# This operation cannot be done when the record is opened.
# The measurement must be lock for editing with NVGS_StartEditing.
# @param[in] openedMeasurementId  The value returned by NVGS_OpenMeasurement
# @param[in] channelIndex  The channel index [1..number of channels]
# @return 0 if successful
#        -1 : invalid openedMeasurementId
#        -2 : invalid channelIndex
#        -3 : the channel cannot be removed
def NVGS_RemoveChannel(OpenedMeasurementId_t openedMeasurementId, int channelIndex):
    pass

# Remove one record
# This operation cannot be done when the record is opened.
# The measurement must be lock for editing with NVGS_StartEditing.
# @param[in] openedMeasurementId  The value returned by NVGS_OpenMeasurement
# @param[in] recordId             The record id
# @return 0 if successful
#        -1 : invalid openedMeasurementId
#        -2 : the measurement is not open
#        -3 : cannot remove record
def NVGS_RemoveRecord(OpenedMeasurementId_t openedMeasurementId, int64_t recordId):
    pass

