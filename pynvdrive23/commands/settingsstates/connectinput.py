from ... import Command


class ConnectInput(Command):
    def __init__(self, input, module, channel):
        super().__init__(name=None, parameters=[str(input), str(module), str(channel)])
        self.value = None
        return

    def parse_response(self, response):
        return None
