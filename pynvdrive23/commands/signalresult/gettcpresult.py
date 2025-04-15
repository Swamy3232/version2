from ... import Command


class GetRCPResult(Command):
    def __init__(self, tcp_channel_id):
        super().__init__(name=None, parameters=[tcp_channel_id])
        self.value = None
        return

    def parse_response(self, response):
        self.value = self.parse_response_string(response[:-1])
