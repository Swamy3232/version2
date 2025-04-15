import pynvdrive
from ..client import Client
from ..commands.configuration.setsaveoption import SetSaveOption


def set_save_option(save_mode_flag=None, keyword=None, acquisition_save_flag=None, manual_save_flag=None, client: pynvdrive.Client = None):
    """
    Sets the value of a setting
    """
    if client is None:
        client = pynvdrive.Client()
        client.connect()
    else:
        client.connect()
    try:
        cmd = SetSaveOption(save_mode_flag=save_mode_flag, keyword=keyword, acquisition_save_flag=acquisition_save_flag, manual_save_flag=manual_save_flag)
        client.send_command(cmd)
        return True
    except pynvdrive.NVDriveCommandError as e:
        print('error SetSaveOption ', e.error)
        return False
