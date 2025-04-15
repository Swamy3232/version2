from ... import Command


class GetCurrentTagReference(Command):
    def __init__(self, layout_name, window_name, display_zone_type=0):
        super().__init__(name=None, parameters=[layout_name, window_name, str(display_zone_type)])
        self.value = None
        return

    def parse_response(self, response):
        self.value = self.parse_response_string(response[:-1])