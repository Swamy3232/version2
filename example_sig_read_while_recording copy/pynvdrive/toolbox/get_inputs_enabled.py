import pynvdrive
from pynvdrive.commands.settingsstates.getsettingvalue import GetSettingValue


def get_inputs_enabled(client: pynvdrive.Client = None):
	"""
	Return a list of inputs enabled as defined in nvgate panel
	"""
	if client is None:
		client = pynvdrive.Client()
		client.connect()
	else:
		client.connect()

	idn_front_end = 'frontEnd'

	# Count the number of inputs
	list_inputs = []
	try:
		for i in range(1, 256):
			idn = '{}.input{}.state'.format(idn_front_end, i)
			cmd = GetSettingValue(idn=idn)
			client.send_command(cmd)
			if cmd.value:
				list_inputs.append(i)

	except pynvdrive.NVDriveCommandError as e:
		pass
	except pynvdrive.NVDriveConnectionError:
		print('error NVDrive is not connected (get_inputs_enabled)')
	except Exception:
		pass
	return list_inputs


def get_inputs_dc_enabled(client: pynvdrive.Client = None):
	"""
	Return a list of inputs enabled as defined in nvgate panel
	"""
	if client is None:
		client = pynvdrive.Client()
		client.connect()
	else:
		client.connect()

	idn_front_end = 'frontEnd'

	# Count the number of inputs
	list_inputs = []
	try:
		for i in range(1, 256):
			idn = '{}.dcinput{}.state'.format(idn_front_end, i)
			cmd = GetSettingValue(idn=idn)
			client.send_command(cmd)
			if cmd.value:
				list_inputs.append(i)

	except pynvdrive.NVDriveCommandError as e:
		pass
	except pynvdrive.NVDriveConnectionError:
		print('error NVDrive is not connected (get_inputs_dc_enabled)')
	except Exception:
		pass
	return list_inputs
