"""
This module defines all the commands of NVDrive concerning the reinjection
"""

import logging

from orostk.nvdrive.generic_command import GenericCommand
from orostk.nvdrive.nvdrive_exceptions import (
    CommandFailException,
    TCPResultChannelException,
    BadResultException
)
from orostk.nvdrive.result_buffer import ResultBuffer
from orostk.nvdrive.nvd_result import (
    create_tcp_result_channel, set_tcp_result_channel,
    get_tcp_result_channels,
    add_data_to_tcp_result_channel,
    new_data_for_tcp_result_channel
)
from orostk.nvdrive.nvd_utils import get_cmd_last_error


nvdrive_logger = logging.getLogger('NVDriveLogger')


class CreateTCPResultChannel(GenericCommand):
    """
    This class simulates:

        - CreateNewTCPChannel

    """

    def __init__(self, result=None):
        nvdrive_logger.debug(
            'Creating a {} command'.format(self.__class__.__name__)
        )
        super().__init__()
        self.tcp_channel = None
        self.result = result

    def run(self, socket):
        if self.result is None:
            raise CommandFailException(
                'You have to affect a Result to the command')
        elif self.result.module_id != 498:
            raise CommandFailException(
                "You can't send a TCP result with module_id" +
                " other than 498 (reinjected result), you sent a " +
                str(self.result.module_id)
            )
        elif not self.result.is_SI():
            raise BadResultException(
                "You can't inject a result with non-SI unit,"
                " check your HEAD, XREG/XREF blocks"
            )
        result_buffer = ResultBuffer(self.result)
        nvdrive_logger.info('Running command CreateNewTCPChannel')
        self.return_code = create_tcp_result_channel(socket, result_buffer)
        if self.return_code >= 0:
            # if the command succeed, we update the tcp_channel
            self.tcp_channel = self.return_code
            nvdrive_logger.info('Command succeed')
        else:
            self.error_code = get_cmd_last_error(socket)
            nvdrive_logger.error(
                'Command failed, error code {}'.format(self.error_code)
            )
        return self.return_code >= 0


class SetTCPResultChannel(GenericCommand):
    """
    This class simulates:

        - SetTCPResultChannel

    """
    def __init__(self, result=None, tcp_channel=None):
        nvdrive_logger.debug(
            'Creating a {} command'.format(self.__class__.__name__)
        )
        super().__init__()
        self.tcp_channel = tcp_channel
        self.result = result

    def run(self, socket):
        if self.result is None:
            raise CommandFailException(
                'You have to affect a Result to the command')
        elif self.result.module_id != 498:
            raise CommandFailException(
                "You can't send a TCP result with module_id" +
                " other than 498 (reinjected result), you sent a " +
                str(self.result.module_id)
            )
        elif not self.result.is_SI():
            raise BadResultException(
                "You can't inject a result with non-SI unit,"
                " check your HEAD, XREG/XREF blocks"
            )
        elif self.tcp_channel is None:
            raise CommandFailException(' You have to affect a TCP Channel')
        result_buffer = ResultBuffer(self.result)
        self.return_code = set_tcp_result_channel(
            socket,
            result_buffer,
            self.tcp_channel
        )
        if self.return_code >= 0:
            nvdrive_logger.info('Command succeed')
        else:
            self.error_code = get_cmd_last_error(socket)
            nvdrive_logger.error(
                'Command failed, error code {}'.format(self.error_code)
            )
        return self.return_code >= 0


class GetTCPResultChannelList(GenericCommand):
    """
    This class simulates:

        - GetTCPResultChannelList

    This command returns a list of TCP result channel represented
    as dictionaries
    """

    def __init__(self):
        nvdrive_logger.debug(
            'Creating a {} command'.format(self.__class__.__name__)
        )
        super().__init__()
        self.tcp_result_channels = None

    def run(self, socket):

        nvdrive_logger.info('Running command GetTCPResultChannelList')
        try:
            self.tcp_result_channels = get_tcp_result_channels(socket)
        except TCPResultChannelException as e:
            nvdrive_logger.error(e)
            self.tcp_result_channels = None

        if self.tcp_result_channels is None:
            self.return_code = -1
            self.error_code = get_cmd_last_error(socket)
            nvdrive_logger.error(
                'Command failed, error code {}'.format(self.error_code)
            )
        else:
            self.return_code = 1
            nvdrive_logger.info('Command succeed')
        return self.return_code >= 0


class AddDataToTCPResultChannel(GenericCommand):
    """
    This class simulates:

        - AddDataToTCPResultChannel

    It allows you to add data at the end of a profile (result_type=3)
    """

    def __init__(self, result=None, tcp_channel=None):
        nvdrive_logger.debug(
            'Creating a {} command'.format(self.__class__.__name__)
        )
        super().__init__()
        self.tcp_channel = tcp_channel
        self.result = result

    def run(self, socket):
        if self.result is None:
            raise CommandFailException(
                'You have to affect a Result to the command')
        elif self.result.module_id != 498:
            raise CommandFailException(
                "You can't send a TCP result with module_id" +
                " other than 498 (reinjected result), you sent a " +
                str(self.result.module_id)
            )
        elif self.result.head.result_type != 3:
            raise CommandFailException(
                'You can only add results to a Profile (RefVector)'
            )
        elif self.tcp_channel is None:
            raise CommandFailException(
                'You have to select a tcp_channel'
            )
        result_buffer = ResultBuffer(self.result)
        nvdrive_logger.info('Running command AddDataToTCPResult')
        self.return_code = add_data_to_tcp_result_channel(
            socket,
            result_buffer,
            self.tcp_channel
        )

        if self.return_code < 0:
            self.error_code = get_cmd_last_error(socket)
            nvdrive_logger.error(
                'Command failed, error code {}'.format(self.error_code)
            )
        else:
            nvdrive_logger.info('Command succeed')
        return self.return_code >= 0


class NewDataForTCPResultChannel(GenericCommand):
    """
    This class simulates:

        - NewDataForTCPResultChannel

    It allows you to modify data of a profile (result_type=3)
    """

    def __init__(self, result=None, tcp_channel=None):
        nvdrive_logger.debug(
            'Creating a {} command'.format(self.__class__.__name__)
        )
        super().__init__()
        self.tcp_channel = tcp_channel
        self.result = result

    def run(self, socket):
        if self.result is None:
            raise CommandFailException(
                'You have to affect a Result to the command')
        elif self.result.module_id != 498:
            raise CommandFailException(
                "You can't send a TCP result with module_id" +
                " other than 498 (reinjected result), you sent a " +
                str(self.result.module_id)
            )
        elif self.tcp_channel is None:
            raise CommandFailException(
                'You have to select a tcp_channel'
            )
        result_buffer = ResultBuffer(self.result)
        nvdrive_logger.info('Running command NewDataToTCPResultChannel')
        self.return_code = new_data_for_tcp_result_channel(
            socket,
            result_buffer,
            self.tcp_channel
        )

        if self.return_code < 0:
            self.error_code = get_cmd_last_error(socket)
            nvdrive_logger.error(
                'Command failed, error code {}'.format(self.error_code)
            )
        else:
            nvdrive_logger.info('Command succeed')
        return self.return_code >= 0
