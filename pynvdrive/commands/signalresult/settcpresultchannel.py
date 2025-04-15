from ... import Command


class SetTCPResultChannel(Command):
    def __init__(self, binary_param):
        super().__init__(name=None, parameters=[binary_param])
        self.value = None
        return

    def parse_response(self, response):
        self.value = self.parse_response_string(response[:-1])
