"""
This module defines the NVDManager class
"""
import logging

from orostk.nvdrive.nvdrive_exceptions import CommandFailException
from orostk.nvdrive.nvd_utils import (
    connect, disconnect, init_buffers, delete_buffers
)

nvdrive_logger = logging.getLogger('NVDriveLogger')


class NVDClient(object):
    """
    This class is the entrypoint for NVDrive commands, it connects to NVGate,
    manages sent commands and keeps informations about them.

    Example::

        client = NVDClient()
        client.connect()
        cmd = Run()
        client.run(cmd)
        client.disconnect()

    """
    _socket_cpt = 0

    def __init__(self, error_policy='exception'):
        """

        :param error_policy: Error policy 'exception' or 'ignore'
        :return:
        """
        self._socket = None
        self.sent_commands = []
        self.last_command = None
        self._connected = False
        self._address = None
        self._port = None
        if error_policy == 'exception':
            self._raise_exception = True
        elif error_policy == 'ignore':
            self._raise_exception = False
        else:
            nvdrive_logger.warning('''
                Unknown error policy: {},
                put "exception" by default'''.format(error_policy))
            self._raise_exception = True

    def connect(self, address='127.0.0.1', port=3000):
        """Connect the manager to a NVGate instance

        :param address: IP address of the computer hosting NVGate
        :param port: port on the host computer where NVGate is running on
        """
        if self._connected:
            nvdrive_logger.warning(
                "Manager already connected on {} {}".format(
                    self._address,
                    self._port)
            )
            return
        nvdrive_logger.info(
            'Connecting to NVGate on address {} port {}'.format(address, port)
        )
        self._socket = NVDClient._socket_cpt
        self._address = address
        self._port = port
        nvdrive_logger.debug('NVDClient socket: {}'.format(self._socket))
        nvdrive_logger.debug('Initialization of dll buffers')
        init_buffers(1)
        nvdrive_logger.debug('Connecting to NVGate')
        connect(self._port, self._address, self._socket)
        self._connected = True
        nvdrive_logger.info('Connected')

    def run(self, command):
        """Run a NVDrive command on the connected NVGate instance

        :param command: Command to run
        :return: True if command succeed, else False
        """
        if not self._connected:
            raise ConnectionError(
                'Manager not connected, connect it before running a command'
            )
        self.sent_commands.append(command)
        self.last_command = command
        command_succeed = command.run(self._socket)
        if not command_succeed and self._raise_exception:
            raise CommandFailException(
                'Command {} failed with error code {}'.format(
                    command.__class__.__name__,
                    command.error_code)
            )
        return command_succeed

    def disconnect(self):
        """Disconnect the manager from NVGate instance

        """
        if not self._connected:
            nvdrive_logger.warning("Manager not connected, can't disconnect")
            return
        nvdrive_logger.info('Disconnecting from NVGate')
        disconnect(self._socket)
        nvdrive_logger.debug('Deletion of dll buffers')
        delete_buffers()
        self._connected = False
        nvdrive_logger.info('Disconnected')

    def __del__(self):
        if self._connected:
            self.disconnect()
