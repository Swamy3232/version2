import pynvdrive
from ..client import Client
from ..commands.graphics.setlayout import SetLayout


def set_layout(layout_name: str, client: pynvdrive.Client = None):
    """
    Sets the value of a setting
    """
    if client is None:
        client = pynvdrive.Client()
        client.connect()
    else:
        client.connect()

    try:
        cmd = SetLayout(layout_name=layout_name)
        client.send_command(cmd)
        return True
    except pynvdrive.NVDriveCommandError as e:
        print('error SetLayoutName ', e)
        return False
