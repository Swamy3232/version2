import os
import sys
import time

import pynvdrive
from pynvdrive.toolbox.get_inputs_list import get_inputs_list
from pynvdrive.commands.settingsstates import SetSettingValue, GetSettingValues, GetSettingValue
from pynvdrive.commands.settingsstates.getanalyzerstate import GetAnalyzerState, TriggerState
from pynvdrive.commands.configuration import SetSaveOption
from pynvdrive.commands.project import ResetWorkbook
from pynvdrive.commands.actions import Run, Stop

import orostk
from orostk.file.measurement import Measurement, Record, Channel, NvgsRecordMultiPartMode, ReadingStatus
from orostk.file.channel import ChannelType
from orostk.file.nvg_signal_typedef import RecordMetadataStr, MeasurementMetadataStr_Predef, ChannelMetadataStr_Predef


"""
The goal of this example is to read the current recording measurement, print data and metadata

"""

SAMPLING_RATE = 25600  # S/s
RECORD_DURATION = 20  # seconds

BLOCK_SIZE = 8192
SLEEP_TIME_BETWEEN_READS = 0.02


def configure_nvgate():
	# Set SamplingRate
	with pynvdrive.Client() as client:
		# Set autobandwidth
		idn_autobandwidth = 'recorder.bandwiths.871'
		cmd = SetSettingValue(idn=idn_autobandwidth, value=1)
		client.send_command(cmd)

		# Read autobandwidth
		cmd = GetSettingValue(idn=idn_autobandwidth)
		client.send_command(cmd)
		assert int(cmd.value) == 1, 'Failed to set autobandwidth, GetSettingValue: {}'.format(cmd.value)

		idn_SAMPLING_RATE = 'frontEnd.inputSettings.inputSampling'
		cmd = SetSettingValue(idn=idn_SAMPLING_RATE, value=SAMPLING_RATE)
		client.send_command(cmd)

		# Get sampling rate
		cmd = GetSettingValue(idn=idn_SAMPLING_RATE)
		client.send_command(cmd)
		assert int(cmd.value) == SAMPLING_RATE, 'Failed to set sampling rate, GetSettingValue: {}'.format(cmd.value)

		# Enable input 1
		idn_input = 'frontEnd.input1.state'
		cmd = SetSettingValue(idn=idn_input, value=1)
		client.send_command(cmd)

		# Check if input 1 enabled
		idn_input = 'frontEnd.input1.state'
		cmd = GetSettingValue(idn=idn_input)
		client.send_command(cmd)
		assert cmd.value == 1, 'Failed to enable input 1, GetSettingValue: {}'.format(cmd.value)

		# Enable track 1
		idn_track = 'recorder.track1.state'
		cmd = SetSettingValue(idn=idn_track, value=1)
		client.send_command(cmd)

		# Check if track 1 enabled
		idn_track = 'recorder.track1.state'
		cmd = GetSettingValue(idn=idn_track)
		client.send_command(cmd)

		# # Connect input 1 to track 1
		idn_track_source = 'recorder.track1.100'
		idn_input_channel = '001.001.000'
		cmd = SetSettingValue(idn=idn_track_source, value=idn_input_channel)
		client.send_command(cmd)

		# Check if input 1 connected to track 1
		cmd = GetSettingValue(idn=idn_track_source)
		client.send_command(cmd)
		assert cmd.value == idn_input_channel, 'Failed to connect input 1 to track 1, GetSettingValue: {}'.format(cmd.value)

		# Enable record on PC
		idn_record = 'recorder.recMode.200'
		cmd = SetSettingValue(idn=idn_record, value=1)
		client.send_command(cmd)

		# Check if record on PC enabled
		cmd = GetSettingValue(idn=idn_record)
		client.send_command(cmd)
		assert int(cmd.value) == 1, 'Failed to enable record on PC, GetSettingValue: {}'.format(cmd.value)

		# Set part length
		idn_part_length = 'recorder.recMode.partLength'
		cmd = SetSettingValue(idn=idn_part_length, value=1)
		client.send_command(cmd)

		# Check if part length set
		cmd = GetSettingValue(idn=idn_part_length)
		client.send_command(cmd)
		assert int(cmd.value) == 1, 'Failed to set part length, GetSettingValue: {}'.format(cmd.value)

		# Set time to stop, 10 seconds
		idn_recMode_mode = 'recorder.recMode.17'
		cmd = SetSettingValue(idn=idn_recMode_mode, value=0)
		client.send_command(cmd)
		idn_recMode_duration = 'recorder.recMode.23'
		cmd = SetSettingValue(idn=idn_recMode_duration, value=RECORD_DURATION)
		client.send_command(cmd)

		# Check if time to stop set
		cmd = GetSettingValue(idn=idn_recMode_mode)
		client.send_command(cmd)
		assert int(cmd.value) == 0, 'Failed to set time to stop, GetSettingValue: {}'.format(cmd.value)

		# Check if time to stop set
		cmd = GetSettingValue(idn=idn_recMode_duration)
		client.send_command(cmd)
		assert int(cmd.value) == RECORD_DURATION, 'Failed to set time to stop, GetSettingValue: {}'.format(cmd.value)

		# Set SaveOption without confirmation
		cmd = SetSaveOption(3)
		client.send_command(cmd)
		
	return 


def read_signal():
	with pynvdrive.Client() as client:
		# Start recording
		cmd = Run()
		client.send_command(cmd)

		# Wait until recording starts
		cmd = GetAnalyzerState(module='recorder')
		client.send_command(cmd)
		while cmd.state != TriggerState.RECORDING:
			print('Waiting for recording to start, GetAnalyzerState: {}'.format(cmd.state))
			time.sleep(1)
			client.send_command(cmd)
	time.sleep(1)

	# NVGate is recording now
	measurement_while_recording = Measurement.read_measurement_recording()
	print('measurement: {}'.format(measurement_while_recording))

	# Ensure orostk knows it is recording
	assert measurement_while_recording.is_recording(), 'Orostk is not aware of recording'

	# Update metadata
	# Update all metadata once NVGate is running
	measurement_while_recording.read_metadata()

	channel_idx = 1
	read_data = []
	while measurement_while_recording.get_reading_status(channel_idx=channel_idx) != ReadingStatus.MeasurementRead:
		try:
			if not measurement_while_recording.read_metadata():
				time.sleep(0.5)
				continue
		except:
			time.sleep(0.5)
			continue

		current_record = measurement_while_recording.get_opened_record()
		current_record_idx = current_record.get_record_idx()

		channel = current_record.get_channel(index=channel_idx)
		data = channel.read_data_block(block_size=BLOCK_SIZE)
		read_data.extend(data)

		print('Read {} samples'.format(len(data)))

		# Do whatever you want with data here
		#
		#

		# Flag to check if the measurement is fully read or still being read
		reading_status = measurement_while_recording.get_reading_status(channel_idx=channel_idx)

		if reading_status == ReadingStatus.MeasurementRead:
			break
		time.sleep(SLEEP_TIME_BETWEEN_READS)

	print('Recording is finished')
	print('Total samples read: {}'.format(len(read_data)))
	print('Expected samples: {}'.format(SAMPLING_RATE*RECORD_DURATION))
	assert len(read_data) == SAMPLING_RATE*RECORD_DURATION, 'Failed to read all samples, len(read_data): {}'.format(len(read_data))


def main():
	configure_nvgate()
	read_signal()


if __name__ == '__main__':
	main()
	print('Done!')
	sys.exit(0)
