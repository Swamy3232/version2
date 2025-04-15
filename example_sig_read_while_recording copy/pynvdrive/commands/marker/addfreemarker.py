from ... import Command


class AddFreeMarker(Command):
    def __init__(self, window_name, position, display_zone='4', interpolation='0',  label='Marker', trace_application='1'):
        super().__init__(name=None, parameters=[window_name, position, display_zone, interpolation, label, trace_application, '', '', '', '', '1'])
        self.value = None
        return

    def parse_response(self, response):
        return None
