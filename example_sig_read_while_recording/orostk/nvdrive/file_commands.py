import logging
from enum import Enum

from orostk.nvdrive.generic_command import GenericCommand
from orostk.nvdrive.nvd_commands import import_file
from orostk.nvdrive.nvd_utils import get_cmd_last_error


nvdrive_logger = logging.getLogger('NVDriveLogger')


class FileType(Enum):
    OR2X_RES = 0
    OR2X_SIG = 1
    OR3X_RES = 2
    OR3X_SIG = 3
    UFF_SIG = 4
    TXT_SIG = 5


class ImportFile(GenericCommand):
    """
    This class simulates:
        - ImportFile

    """
    def __init__(self, file_type: FileType, file_name, directory, project=''):
        """

        :param file_type:
        :param file_name:
        :param directory:
        :param project:
        """
        super().__init__()
        self.file_type = file_type
        self.file_name = file_name
        self.directory = directory
        self.project = project

    def run(self, socket):
        nvdrive_logger.info('Running command ImportFile')
        self.return_code = import_file(socket,
                                       self.file_type.value,
                                       self.file_name,
                                       self.directory,
                                       self.project)
        if self.return_code < 0:
            self.error_code = get_cmd_last_error(socket)
            nvdrive_logger.error(
                'Command ImportFile failed, error code {}'.format(
                    self.error_code
                )
            )

        else:
            nvdrive_logger.info('Command succeed')
        return self.return_code == 0
