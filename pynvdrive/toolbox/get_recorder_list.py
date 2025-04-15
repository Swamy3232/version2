import pynvdrive
from pynvdrive import NVDriveCommandError
from ..client import Client
from ..commands.settingsstates import GetSettingValue
from collections import OrderedDict
from pynvdrive.formats.utils.idn import is_idn


def get_recorder_list(client: pynvdrive.Client = None):
	"""
	Return a list of inputs in recorder as defined in nvgate panel
	"""
	if client is None:
		client = pynvdrive.Client()
		client.connect()
	else:
		client.connect()

	if not client.is_connected():
		return []

	idn_front_end = 'frontEnd'
	idn_recorder = 'recorder'
	recorder_dict = {'source': '100', 'Sampling rate (S/s)': '14'}

	# Get sampling value
	sampling_dict = {'fs1': 'inputSampling', 'fs2': '868', 'dc': 'dcSampling', 'fast': 'inputSampling', 'slow': 'dcSampling'}
	sampling = {}
	# Get frontend settings
	for key in sampling_dict:
		try:
			cmd = GetSettingValue(idn='{}.inputSettings.{}'.format(idn_front_end, sampling_dict[key]))
			client.send_command(cmd)
			sampling[key] = cmd.value
		except pynvdrive.NVDriveCommandError as e:
			print('error GetSettingValue bandwidth', e)
		except pynvdrive.NVDriveConnectionError:
			return []
		except Exception:
			return []

	try:
		sampling['fast'] = str(int(sampling.get('fast'))*64)
	except Exception:
		pass
	try:
		sampling['slow'] = str(12.5)
	except Exception:
		pass

	# Count the number of inputs
	list_inputs = []
	for i in range(1, 256):
		idn = '{}.track{}.state'.format(idn_recorder, i)
		cmd = GetSettingValue(idn=idn)
		try:
			client.send_command(cmd)
		except pynvdrive.NVDriveCommandError as e:
			continue
		except pynvdrive.NVDriveConnectionError:
			print('error NVDrive is not connected (get_recorder_list)')
		except Exception:
			pass

		if not cmd.value:
			continue
		else:
			current_input = OrderedDict()
			current_input['track'] = i
			for key in recorder_dict:
				try:
					cmd = GetSettingValue(
						idn='{}.track{}.{}'.format(idn_recorder, i, recorder_dict[key]))
					client.send_command(cmd)
					current_input[key] = cmd.value
				except pynvdrive.NVDriveCommandError as e:
					print('error get_recorder_list GetSettingValue input', e)

			if current_input.get('source', None) and is_idn(current_input.get('source', None)):
				source_label_idn = '{}.{}.001'.format(current_input['source'].split('.')[0], current_input['source'].split('.')[1])
				try:
					cmd = GetSettingValue(idn=source_label_idn)
					client.send_command(cmd)
					current_input['source'] = cmd.value
				except pynvdrive.NVDriveCommandError as e:
					print('error GetSettingValue label', e)
			if 'Sampling rate (S/s)' in current_input:
				current_input['Sampling rate (S/s)'] = sampling.get(current_input.get('Sampling rate (S/s)', None), None)

			list_inputs.append(current_input)

	return list_inputs
