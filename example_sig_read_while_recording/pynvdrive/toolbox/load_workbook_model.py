import pynvdrive
from ..commands.project.loadworkbookmodel import LoadWorkbookModel


def load_workbook_model(model_name, client: pynvdrive.Client = None):
    """
    Load a model in NVGate
    :param model_name: name of the model to load
    :param client: pynvdrive.Client instance
    :return: True if model is loaded, False otherwise
    """
    if client is None:
        client = pynvdrive.Client()
        client.connect()
    else:
        client.connect()

    try:
        cmd = LoadWorkbookModel(workbook_name=model_name)
        client.send_command(cmd)
    except pynvdrive.NVDriveCommandError as e:
        return None
    except pynvdrive.NVDriveConnectionError:
        return None

    return True
