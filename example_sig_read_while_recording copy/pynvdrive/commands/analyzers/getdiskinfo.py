from ... import Command
import struct


class GetDiskInfo(Command):
    """
    Return the disk information of the NVDrive.
    :param optional analyzer_index: The index of the analyzer.
    :param optional disk_index: The index of the disk.
    """
    def __init__(self, analyzer_index='', disk_index=''):
        super().__init__(name=None, parameters=[str(analyzer_index), str(disk_index)])
        self.value = None
        self.hard_size = None
        self.hard_free = None
        self.local_size = None
        self.local_free = None
        self.disk_serial_number = None
        self.disk_model_name = None
        return

    def parse_response(self, response):
        self.hard_size = struct.unpack('q', response[0:8])[0]
        self.hard_free = struct.unpack('q', response[8:16])[0]
        self.local_size = struct.unpack('q', response[16:24])[0]
        self.local_free = struct.unpack('q', response[24:32])[0]
        reste = response[32:]
        self.disk_serial_number = self.parse_response_string(reste.split(b'\0')[0])
        self.disk_model_name = self.parse_response_string(reste.split(b'\0')[1])
        self.value = [self.hard_size, self.hard_free, self.local_size, self.local_free, self.disk_serial_number, self.disk_model_name]
