from ... import Command
import struct


class GetNVGateInfo(Command):
    """
    Retrieve some NVGate information.
    :param optional analyzer_index: The index of the analyzer to retrieve the information from.
    If not specified, the information is retrieved from the first analyzer
    index start at 1.
    """
    def __init__(self, analyzer_index=''):
        super().__init__(name=None, parameters=[str(analyzer_index)])
        self.value = None

        self.nvgate_major_version = None
        self.nvgate_minor_version = None
        self.indice = None
        self.hard_type = None
        self.hard_serial_number = None
        self.full_build_number = None
        return

    def parse_response(self, response):
        self.nvgate_major_version = struct.unpack('I', response[0:4])[0]
        reste = response[4:]
        self.nvgate_minor_version = struct.unpack('I', reste[0:4])[0]
        reste = reste[4:]
        self.value = []
        self.value.append(self.nvgate_major_version)
        self.value.append(self.nvgate_minor_version)

        # Get the number of hardware devices*
        current_hardware = []
        self.indice = self.parse_response_string(reste.split(b'\0', 2)[0])
        if self.indice.isnumeric():
            self.indice = int(self.indice)
        self.hard_type = self.parse_response_string(reste.split(b'\0', 2)[1])
        self.value.append(self.indice)
        self.value.append(self.hard_type)
        reste = reste.split(b'\0', 2)[2]

        self.serial_number = struct.unpack('l', reste[0:4])[0]
        self.value.append(self.serial_number)
        reste = reste[4:]
        dunno_what_it_is = struct.unpack('l', reste[0:4])[0]
        reste = reste[4:]
        self.full_build_number = self.parse_response_string(reste.split(b'\0')[0])
        self.value.append(self.full_build_number)

        return
