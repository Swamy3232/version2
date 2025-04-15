from ... import Command


class GetMagnitudeInfo(Command):
    def __init__(self, magnitude_key):
        super().__init__(name=None, parameters=[magnitude_key])
        self.value = None
        self.magnitude_name = None
        self.unit_name = None
        self.unit_label = None
        return

    def parse_response(self, response):
        try:
            _, _ = response.split(b'\0', 1)
        except Exception:
            raise NotImplementedError('No window displayed into chosen layout')

        self.value = self.parse_response_list_string(response)
        self.magnitude_name = self.value[0]
        self.unit_name = self.value[1]
        self.unit_label = self.value[2]
