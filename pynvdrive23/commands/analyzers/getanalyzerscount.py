from ... import Command
import struct


class GetAnalyzersCount(Command):
    """
    Return the number of analyzers.
    """
    def __init__(self):
        super().__init__(name=None, parameters=[])
        self.value = None
        self.analyzers_count = None
        return

    def parse_response(self, response):
        self.analyzers_count = struct.unpack('h', response[0:2])[0]
        self.value = self.analyzers_count