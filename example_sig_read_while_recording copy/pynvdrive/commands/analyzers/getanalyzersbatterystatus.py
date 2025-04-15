from ... import Command
import struct


class GetAnalyzersBatteryStatus(Command):
    """
    Return the battery status of the analyzers.
    :return: The battery status of the analyzers. list of strings
    """
    def __init__(self):
        super().__init__(name=None, parameters=[])
        self.value = None
        return

    def parse_response(self, response):
        reste = response[2:]
        self.value = []
        while len(reste) >= 4:
            self.value.append(struct.unpack('L', reste[0:4])[0])
            reste = reste[4:]
