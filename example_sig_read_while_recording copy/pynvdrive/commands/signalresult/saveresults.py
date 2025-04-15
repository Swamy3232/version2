from ... import Command


class SaveResults(Command):
    def __init__(self, confirm_name=0, return_measurement_name=0):
        super().__init__(name=None, parameters=[str(confirm_name), str(return_measurement_name)])
        self.value = None
        return

    def parse_response(self, response):
        self.value = self.parse_response_string(response[:-1])
