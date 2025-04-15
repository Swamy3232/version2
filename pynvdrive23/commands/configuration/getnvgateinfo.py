from ... import Command


class GetNVGateInfo(Command):
    def __init__(self):
        super().__init__(name=None, parameters=[])
        self.value = None
        self.hardFamily = None
        self.hardSerialNumber = None
        return

    def parse_response(self, response):
        self.value = self.parse_response_string(response[:-1])
        self.hardSerialNumber = int.from_bytes(response.split(b'\0')[8], byteorder='little', signed=True)
        self.hardFamily = self.parse_response_string(response.split(b'\0')[7])
