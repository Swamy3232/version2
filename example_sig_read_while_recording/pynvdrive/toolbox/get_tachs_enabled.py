import pynvdrive
from pynvdrive.commands.settingsstates.getsettingvalue import GetSettingValue


def get_tachs_enabled(client: pynvdrive.Client = None):
	"""
	Return a list of ext tach enabled as defined in nvgate panel
	"""
	if client is None:
		client = pynvdrive.Client()
		client.connect()
	else:
		client.connect()

	idn_front_end = 'frontEnd'

	# Count the number of inputs
	list_tachs = []

	try:
		for i in range(1, 8):
			idn = '{}.extSync{}.state'.format(idn_front_end, i)
			cmd = GetSettingValue(idn=idn)
			client.send_command(cmd)
			if cmd.value:
				list_tachs.append(i)

	except pynvdrive.NVDriveCommandError as e:
		pass
	except pynvdrive.NVDriveConnectionError:
		print('error NVDrive is not connected (get_tachs_enabled)')
	except Exception:
		pass

	return list_tachs
