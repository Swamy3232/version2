from ... import Command


class AddWindowZoomedSignal(Command):
    """
    Creates a zoomed signal window containing zoomed track of recording signal.

    parameters:

        - LayoutName
        - WindowName
        - TrackNumber
        - Begin
        - End

    """
    def __init__(self, layout_name, window_name, track_number, begin, end, project_name='', measurement_name=''):
        super().__init__(name=None, parameters=[layout_name, window_name, str(track_number), str(begin), str(end)])
        self.value = None
        return

    def parse_response(self, response):
        self.value = self.parse_response_string(response[:-1])
