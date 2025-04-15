from ... import Command
from ... import NVDriveCommandParsing


class GetSettingValues(Command):
    def __init__(self, idn):
        super().__init__(name=None, parameters=[idn, '', ''])
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
            self.value = self.parse_enumerated(self.parse_response_list_string(contents))
        elif value_type == b'Scalar':
            self.value = self.parse_response_scalar(contents)
            # self.value = self.parse_response_string(contents)
        else:
            raise NotImplementedError('GetSettingValue not yet implemented setting type: ' + str(value_type))
        return

    @staticmethod
    def parse_response_scalar(contents):
        try:
            import struct
            return struct.unpack('f', contents)[0]
        except (Exception,):
            return float

    @staticmethod
    def parse_response_boolean(contents):
        if len(contents) != 2:
            raise NVDriveCommandParsing('expected 16-bits encoded bool')
        i = int.from_bytes(contents, byteorder='little', signed=True)
        return i != 0

    @staticmethod
    def parse_enumerated(contents):
        # If not % 2, then the last element has to be removed
        old = contents
        contents = []
        for i in range(0, len(old) -1, 2):
            temp = ([old[i], old[i+1]])
            contents.append(temp)

        return contents
