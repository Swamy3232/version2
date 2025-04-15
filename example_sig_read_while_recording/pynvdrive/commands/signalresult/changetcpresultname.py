from ... import Command


class GetRCPResultChannelList(Command):
    def __init__(self, tcp_channel_id, result_name):
        super().__init__(name=None, parameters=[str(tcp_channel_id), result_name])
        self.value = None
        return

    def parse_response(self, response):
        self.value = self.parse_response_string(response[:-1])