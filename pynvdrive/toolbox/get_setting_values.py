import pynvdrive
from ..client import Client
from ..commands.settingsstates import GetSettingValues


def get_setting_values(module, submodule, setting, client: pynvdrive.Client = None):
    """
    Sets the value of a setting
    """
    if client is None:
        client = pynvdrive.Client()
        client.connect()
    else:
        client.connect()

    idn = '{}.{}.{}'.format(module, submodule, setting)

    try:
        cmd = GetSettingValues(idn=idn)
        client.send_command(cmd)
        return cmd.value
    except pynvdrive.NVDriveCommandError as e:
        print('error GetSettingValues input', e)
        return False
