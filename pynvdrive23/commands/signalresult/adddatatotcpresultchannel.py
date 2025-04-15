from ... import Command
from ...formats.blocks import TCPRESULT


class AddDataForTCPResultChannel(Command):
    def __init__(self, tcp_result):

        if isinstance(tcp_result, TCPRESULT):
            tcp_result.check_result_consistency()
            tcp_result_binary = tcp_result.to_binary()

        super().__init__(name=None, parameters=[tcp_result_binary])
        self.value = None
        return

    def parse_response(self, response):
        self.value = self.parse_response_string(response[:-1])
