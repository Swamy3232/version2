import struct

from ... import Command


class GetFreeMarkerParameters(Command):
    def __init__(self, window, marker_number, display_zone=''):
        super().__init__(name=None, parameters=[window, str(display_zone), str(marker_number)])
        self.value = None
        return

    def parse_response(self, response):
        self.value = []
        position = struct.unpack('f', response[0:4])[0]
        self.value.append(position)

        response = response[4:].split(b'\0', 1)
        label = self.parse_response_string(response[0])
        self.value.append(label)
        response = response[1]

        interpolationType = struct.unpack('I', response[0:4])[0]
        self.value.append(interpolationType)


        # contents = response.split(b'-')