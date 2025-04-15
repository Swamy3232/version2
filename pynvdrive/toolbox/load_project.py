import pynvdrive
from ..commands.project.loadproject import LoadProject


def load_project(project_name, save=0, client: pynvdrive.Client = None):
    """
    Load a project in NVGate
    :param project_name: name of the project to load
    :param client: pynvdrive.Client instance
    :param save: 0 load without saving current, 1(default) open confirmation dialog box
    :return: True if project is loaded, False otherwise
    """
    if client is None:
        client = pynvdrive.Client()
        client.connect()
    else:
        client.connect()

    try:
        cmd = LoadProject(project_name=project_name, save=save)
        client.send_command(cmd)
    except pynvdrive.NVDriveCommandError as e:
        return None
    except pynvdrive.NVDriveConnectionError:
        return None

    return True
