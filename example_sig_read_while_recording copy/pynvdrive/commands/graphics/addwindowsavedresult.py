from ... import Command


class AddWindowSavedResult(Command):
    """
    Creates a result window (not 3D waterfall result).

    parameters:

        - LayoutName
        - WindowName
        - ProjectName
        - MeasurementName
        - ModuleNumber
        - ProcessNumber
        - ChannelNumber

    optional parameters:

        - RefChannelNumber
        - WeightingOperator
        - TimeOperator
        - DisplayUnit
        - ArrangeWindow
        - Maximize/Minimize, 0(Normal), 1(Minimize), 2(Maximize), default=0
        - 2D_WaterFall, 0(Normal), 1(2D Waterfall), default=0

    """
    def __init__(self, layout_name, window_name, project_name, measurement_name, module_number, process_number, channel_number, reference_channel_number='', weighting_operator=0, time_operator='', display_unit='', arrange_window='', maximize_minimize='', waterfall=''):
        super().__init__(name=None, parameters=[layout_name, window_name, project_name, measurement_name, str(module_number), str(process_number), str(channel_number), str(reference_channel_number), str(weighting_operator), str(time_operator), str(display_unit), arrange_window, maximize_minimize, waterfall])
        self.value = None
        return

    def parse_response(self, response):
        self.value = self.parse_response_string(response[:-1])
