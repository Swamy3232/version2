import struct

from pynvdrive.command import Command
from ... import NVDriveCommandParsing


class GetSettingValue(Command):
    def __init__(self, idn, line='', column=''):
        super().__init__(name=None, parameters=[idn, '', '', str(line), str(column)])
        self.idn = idn
        self.value = None
        return

    def parse_response(self, response):
        value_type, contents = response.split(b'\0', 1)
        if value_type == b'Boolean':
            self.value = self.parse_response_boolean(contents)
        elif value_type == b'String':
            self.value = self.parse_response_string(contents)
        elif value_type == b'Enumerated':
            self.value = self.parse_response_string(contents)
        elif value_type == b'Scalar':
            self.value = self.parse_response_scalar(contents)
            # self.value = self.parse_response_string(contents)
        elif value_type == b'idn':
            self.value = self.parse_response_string(contents)
        elif value_type == b'Signal file':
            self.value = self.parse_response_string(contents)
        else:
            raise NotImplementedError('GetSettingValue not yet implemented setting type: ' + str(value_type))
        return

    @staticmethod
    def parse_response_scalar(contents):
        temp = struct.unpack('f', contents)
        return temp[0]

    @staticmethod
    def parse_response_boolean(contents):
        if len(contents) != 2:
            raise NVDriveCommandParsing('expected 16-bits encoded bool')
        i = int.from_bytes(contents, byteorder='little', signed=True)
        print(i)
        return i != 0
