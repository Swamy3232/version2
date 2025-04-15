import socket

from orostk.nvdrive.nvdrive_exceptions import NotificationTimeoutException


class NotificationHandler(object):
    """
    This class is used to to manage the network part
    of the notification system.
    It open and manage the TCP connection.
    """
    def __init__(self, ip_address, port, timeout_on_recv=None):
        self.ip_address = ip_address
        self.port = port
        self.socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket_server.bind((self.ip_address, self.port))
        self.socket_server.listen()
        self.timeout_on_recv = timeout_on_recv
        self.connection = None

    def accept_connection(self, timeout=None):
        if timeout:
            self.socket_server.settimeout(timeout)
        try:
            self.connection = self.socket_server.accept()
        except socket.timeout:
            raise NotificationTimeoutException('Timeout during connection')

    def get_block_data(self, size):
        """ Retrieve a data block of fixed size.

        :param size: The size to read
        :return: Bytes representing the data
        """
        self.connection[0].settimeout(self.timeout_on_recv)
        total_size = 0
        total_data = b''
        while total_size < size:
            to_receive = size - total_size
            data = b''
            try:
                data = self.connection[0].recv(to_receive)
            except socket.timeout:
                raise NotificationTimeoutException
            total_data += data
            total_size += len(data)
        return total_data

    def disconnect(self):
        self.socket_server.close()
