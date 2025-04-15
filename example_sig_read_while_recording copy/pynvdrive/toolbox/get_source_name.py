import pynvdrive
from pynvdrive import NVDriveCommandError
from ..client import Client
from pynvdrive.commands.settingsstates.getsettingvalue import GetSettingValue
from pynvdrive.formats.modules import modules as nvg_modules


def get_source_name(module, channel, process=None):
    """
    Return input_nb and input_label string name linked to a module channel number
    """
    try:
        with Client():
            pass
    except (Exception,):
        return None, None

    if isinstance(module, int):  # Convert old idn to new
        module = nvg_modules[module]
    elif module.isnumeric():
        module = nvg_modules[int(module)]

    idn_source = None

    input_nb = None
    label = None

    with Client() as client:
        if module.lower() == 'frontend':
            if process == 311: # DC SIMULATED, process_id=311
                idn_source = '{}.simulatedDCInput{}.000'.format(module, channel)
            elif process == 9: # DC Input
                idn_source = '{}.dcinput{}.000'.format(module, channel)
            else:
                idn_source = '{}.input{}.000'.format(module, channel)
        else:
            try:
                idn = '{}.channel{}.100'.format(module, channel)
                cmd = GetSettingValue(idn=idn)
                client.send_command(cmd)
                idn_source = cmd.value
            except NVDriveCommandError as e:
                print('error get_source_name:GetSettingValue idn source', e)

        if idn_source.split('.')[0] == '015':  # TORSIONAL_INPUT, need to retrieve the tach frontend associated
            try:
                module = idn_source.split('.')[0]
                input_nb = idn_source.split('.')[1]
                idn_source = '{}.{}.100'.format(module, input_nb) # 100 is the src from 015 module
                cmd = GetSettingValue(idn=idn_source)
                client.send_command(cmd)
                idn_source = cmd.value
            except pynvdrive.NVDriveCommandError as e:
                print('error get_source_name for 015 module:GetSettingValue label ', e)

        try:
            module = idn_source.split('.')[0]
            input_nb = idn_source.split('.')[1]
            idn_source = '{}.{}.001'.format(module, input_nb)
            cmd = GetSettingValue(idn=idn_source)

            client.send_command(cmd)
            label = cmd.value
        except pynvdrive.NVDriveCommandError as e:
            print('error get_source_name:GetSettingValue label ', e)

    return input_nb, label, idn_source