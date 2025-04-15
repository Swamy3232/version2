from ... import Command


class GetCurrentUnit(Command):
    def __init__(self, magnitude_name):
        super().__init__(name=None, parameters=[magnitude_name])
        self.value = None
        return

    def parse_response(self, response):
        self.value = self.parse_response_string(response[:-1])
