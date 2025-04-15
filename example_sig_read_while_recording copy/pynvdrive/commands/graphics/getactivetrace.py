from ... import Command
import struct


class GetActiveTrace(Command):
    def __init__(self, layout_name, window_name):
        super().__init__(name=None, parameters=[layout_name, window_name])
        self.value = None
        return

    def parse_response(self, response):
        # Unpack integer
        if len(response) == 4:
            self.value = struct.unpack('i', response)[0]
        else:
            self.value = None
