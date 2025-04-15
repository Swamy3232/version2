from ... import Command


class GetLicenseKeyValue(Command):
    def __init__(self, mode, key, algorithm=''):
        super().__init__(name=None, parameters=[mode, key, algorithm])
        self.value = None
        return

    def parse_response(self, response):
        response = self.parse_response_string(response.split(b'\0', 1)[0])
        self.value = response