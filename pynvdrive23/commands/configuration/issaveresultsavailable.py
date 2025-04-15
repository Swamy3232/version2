import struct

from ... import Command


class IsSaveResultsAvailable(Command):
    def __init__(self):
        super().__init__(name=None, parameters=[])
        self.value = None
        return

    def parse_response(self, response):
        try:
            self.value = struct.unpack('?', response)[0]
        except (Exception,):
            self.value = False
