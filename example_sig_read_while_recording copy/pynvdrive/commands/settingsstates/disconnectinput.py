from ... import Command


class DisconnectInput(Command):
    def __init__(self, input):
        super().__init__(name=None, parameters=[str(input)])
        self.value = None
        return

    def parse_response(self, response):
        return None
