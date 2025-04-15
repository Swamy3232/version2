from ... import Command


class RemoveTCPResultChannel(Command):
    """
    Allows the user to remove a TCP channel.

    parameters:

        - TCPChannelId, if -1 all TCP Channels are destroyed
    """
    def __init__(self, tcp_channel_id):
        super().__init__(name=None, parameters=[str(tcp_channel_id)])
        self.value = None
        return

    def parse_response(self, response):
        self.value = self.parse_response_string(response[:-1])
