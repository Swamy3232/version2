import pynvdrive
from ..client import Client
from ..commands.settingsstates import GetSettingValue


def get_setting_value(module, submodule, setting, client: pynvdrive.Client = None):
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
        cmd = GetSettingValue(idn=idn)
        client.send_command(cmd)
        return cmd.value
    except pynvdrive.NVDriveCommandError as e:
        print('error SetSettingValue input', e)
        return False
    except pynvdrive.NVDriveConnectionError:
        print('error NVDrive is not connected (GetSettingValue)')
        return False

