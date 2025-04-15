"""
this module defines all the commands of NVDrive concerning the reinjection
"""

import logging

from orostk.idn import Idn
from orostk.nvdrive.generic_command import GenericCommand
from orostk.nvdrive.nvd_utils import get_cmd_last_error
from orostk.nvdrive.nvd_result import (
    load_result, load_saved_result, get_result
)


nvdrive_logger = logging.getLogger('NVDriveLogger')


class GetResult(GenericCommand):
    """
    This class simulates:
        - GetResultEx

    This command retrieves a result from NVGate.
    """

    def __init__(self, module, process_id, channel_number,
                 ref_channel=0, waterfall=0):
        nvdrive_logger.debug(
            'Creating a {} command'.format(self.__class__.__name__)
        )
        super().__init__()
        self.result = None
        idn = Idn(module)
        module_id = idn.module_id
        self.result_dict = {
            'module': module,
            'module_id': module_id,
            'process': process_id,
            'channel': channel_number,
            'ref_channel': ref_channel,
            'waterfall': waterfall
        }

    def run(self, socket):
        nvdrive_logger.info('Running command GetResult')
        return_code = load_result(socket, self.result_dict)
        if return_code >= 0:
            nvdrive_logger.debug('Retrieving result')
            self.result = get_result(socket, self.result_dict)
        if return_code < 0 or self.result is None:
            self.error_code = get_cmd_last_error(socket)
            nvdrive_logger.error(
                'Command failed, error code {}'.format(self.error_code)
            )
            return False
        nvdrive_logger.info('Command succeed')
        return True


class GetSavedResult(GenericCommand):
    """
    This class simulates:
        - GetSavedResultEx

    This command retrieves a saved result from NVGate.
    """
    def __init__(self, project_name, measurement_name,
                 module, process_id, channel_number,
                 ref_channel=0, waterfall=0, ):
        nvdrive_logger.debug(
            'Creating a {} command'.format(self.__class__.__name__)
        )
        super().__init__()
        self.result = None
        module_id = Idn(module).module_id
        self.result_dict = {
            'module': module,
            'module_id': module_id,
            'process': process_id,
            'channel': channel_number,
            'ref_channel': ref_channel,
            'waterfall': waterfall,
            'project_name': project_name,
            'measurement_name': measurement_name
        }

    def run(self, socket):
        nvdrive_logger.info('Running command GetSavedResult')
        nvdrive_logger.debug('Loading saved result')
        return_code = load_saved_result(socket, self.result_dict)
        if return_code >= 0:
            nvdrive_logger.debug('Retrieving saved result')
            self.result = get_result(socket, self.result_dict)
        if return_code < 0 or self.result is None:
            self.error_code = get_cmd_last_error(socket)
            nvdrive_logger.error(
                'Command failed, error code {}'.format(self.error_code)
            )
            return False

        nvdrive_logger.info('Command succeed')
        return True
