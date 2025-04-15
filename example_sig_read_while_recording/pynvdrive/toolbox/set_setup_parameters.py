import pynvdrive
from ..client import Client
from ..commands.signalresult.setsetupparameters import SetSetupParameters


def set_setup_parameters(measurement_name=None, increment_type=None, client: pynvdrive.Client = None):
    """
    Sets the value of a setting
    """
    if client is None:
        client = pynvdrive.Client()
        client.connect()
    else:
        client.connect()
    try:
        cmd = SetSetupParameters(measurementName=measurement_name, incrementType=increment_type)
        client.send_command(cmd)
        return True
    except pynvdrive.NVDriveCommandError as e:
        print('error SetSetupParameters ', e)
        return False
