import struct
from ... import Command


class GetUnitInfo(Command):
    def __init__(self, magnitude_name, unit_name):
        super().__init__(name=None, parameters=[magnitude_name, unit_name])
        self.value = None

        self.coeffA = None
        self.coeffB = None
        self.userunit_label = None
        self.userunit_name = unit_name
        self.si_unit = None

        return

    def parse_response(self, response):
        contents = response.split(b'\0')

        self.si_unit = self.parse_response_string(contents[4])

        temp = response[:-17]
        temp = temp.split(b'\0')
        self.userunit_label = self.parse_response_string(temp[-1])

        self.coeffA = struct.unpack('f', response[-16:-12])[0]
        self.coeffB = struct.unpack('f', response[-12:-8])[0]
