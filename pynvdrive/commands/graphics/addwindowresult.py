from ... import Command


class AddWindowResult(Command):
    """
    Creates a result window (not 3D waterfall result).

    parameters:

        - LayoutName
        - WindowName
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
        - ExistingResultIsAnError, 0(not an error), 1(considered as error)

    """
    def __init__(self, layout, window, module, process, channel, reference_channel_number='', weighting_operator=0, time_operator='', display_unit='', arrange_window='', maximize_minimize='', waterfall='', existing_result_is_an_error=''):
        super().__init__(name=None, parameters=[layout, window, str(module), str(process), str(channel), str(reference_channel_number), str(weighting_operator), str(time_operator), str(display_unit), arrange_window, maximize_minimize, waterfall, existing_result_is_an_error])
        self.value = None
        return

    def parse_response(self, response):
        self.value = self.parse_response_string(response[:-1])
