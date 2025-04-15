import struct

from ... import Command
from ...formats.blocks.TCPRESULT import TCPRESULT


class CreateTCPResultChannel(Command):
    """
    CreateTCPResultChannel implementation

    parameters:

        - TCPResult (see doc)

    """
    def __init__(self, tcp_result: TCPRESULT):

        if isinstance(tcp_result, TCPRESULT):
            tcp_result.check_result_consistency()
            tcp_result_binary = tcp_result.to_binary()

        super().__init__(name=None, parameters=[tcp_result_binary])
        self.value = None
        return

    def parse_response(self, response):
        self.value = struct.unpack('l', response)[0]
