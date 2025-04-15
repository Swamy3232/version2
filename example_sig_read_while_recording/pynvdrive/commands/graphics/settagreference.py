from ... import Command


class SetTagReference(Command):
    def __init__(self, layout_name, window_name, selected_reference_name, display_zone_type=0):
        super().__init__(name=None, parameters=[layout_name, window_name, selected_reference_name, str(display_zone_type)])
        self.value = None
        return

    def parse_response(self, response):
        return None
