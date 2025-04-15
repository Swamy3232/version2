import pynvdrive
from pynvdrive import NVDriveCommandError
from ..client import Client
from ..commands.settingsstates import GetSettingValue


def GetSourceName(module, channel):
    """
    Return input string name linked to a module channel
    """
    try:
        with Client():
            pass
    except (Exception,):
        return None, None

    idn_source = None

    input = None
    label = None

    with Client() as client:
        try:
            idn = '{}.channel{}.100'.format(module, channel)
            cmd = GetSettingValue(idn=idn)
            client.send_command(cmd)
            idn_source = cmd.value
        except NVDriveCommandError as e:
            print('error GetSourceName GetSettingValue idn source', e)

        try:
            module = idn_source.split('.')[0]
            process = idn_source.split('.')[1]
            idn_source = '{}.{}.486'.format(module, process)
            cmd = GetSettingValue(idn=idn_source)
            client.send_command(cmd)
            input = cmd.value
        except pynvdrive.NVDriveCommandError as e:
            print('error GetSourceName GetSettingValue input', e)

        try:
            module = idn_source.split('.')[0]
            process = idn_source.split('.')[1]
            idn_source = '{}.{}.001'.format(module, process)
            cmd = GetSettingValue(idn=idn_source)
            client.send_command(cmd)
            label = cmd.value
        except pynvdrive.NVDriveCommandError as e:
            print('error GetSourceName GetSettingValue label ', e)

    return input, label