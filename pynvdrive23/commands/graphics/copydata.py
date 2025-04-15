from ... import Command


class CopyData(Command):
    def __init__(self, layout_name, window_name, display_zone):
        super().__init__(name=None, parameters=[layout_name, window_name, str(display_zone)])
        self.value = None
        return

    def parse_response(self, response):
        return None
