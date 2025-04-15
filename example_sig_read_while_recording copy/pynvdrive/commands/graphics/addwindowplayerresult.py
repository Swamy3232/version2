from ... import Command


class AddWindowPlayerResult(Command):
    """
    Creates a preview window containing signal file track(s).

    parameters:

        - LayoutName
        - WindowName
        - ProjectName
        - MeasurementName

    optional parameters:

		- Nothing
		- Track
		- ArrangeWindow
		- MaximizedMinimized

    """
    def __init__(self, layout_name, window_name, project_name, measurement_name, nothing='', track='', arrange_window='', maximized_minimized=''):
        super().__init__(name=None, parameters=[layout_name, window_name, project_name, measurement_name, nothing, track, arrange_window, maximized_minimized])
        self.value = None
        return

    def parse_response(self, response):
        self.value = self.parse_response_string(response[:-1])
