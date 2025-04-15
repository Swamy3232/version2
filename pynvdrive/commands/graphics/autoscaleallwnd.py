from ... import Command


class AutoscaleAllWnd(Command):
    """
    Autoscale on Y axis or referenced axis of all windows of a layout.

    parameters:

        - layout_name: name of the layout, str

    optional parameters:

        - axis: axis to autoscale, str ("Y" or "Ref")
    """
    def __init__(self, layout_name, axis=''):
        super().__init__(name=None, parameters=[layout_name, axis])
        self.value = None
        return

    def parse_response(self, response):
        self.value = self.parse_response_string(response[:-1])
