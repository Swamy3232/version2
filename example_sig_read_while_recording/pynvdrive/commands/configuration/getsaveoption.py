from ... import Command
import struct


class GetSaveOption(Command):
    """
    Return savemode_flag
    """
    def __init__(self):
        super().__init__(name=None, parameters=[])
        self.value = None
        return

    def parse_response(self, response):
        response = struct.unpack('I', response)[0]
        self.value = response
