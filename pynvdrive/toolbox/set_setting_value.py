import pynvdrive
from ..client import Client
from ..commands.settingsstates import SetSettingValue


def set_setting_value(module, submodule, setting, value, client: pynvdrive.Client = None):
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
        cmd = SetSettingValue(idn=idn, value=value)
        client.send_command(cmd)
        return True
    except pynvdrive.NVDriveCommandError as e:
        print('error SetSettingValue input', e)
        return False
