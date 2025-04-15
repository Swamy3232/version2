from ... import Command


class AddWindowWtfResult(Command):
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
    def __init__(self, layout, window, module, process, channel, reference_channel_number='', weighting_operator=0, time_operator=0, display_unit=0, arrange_window='', maximize_minimize=''):
        super().__init__(name=None, parameters=[layout, window, str(module), str(process), str(channel), reference_channel_number, str(weighting_operator), str(time_operator), str(display_unit), arrange_window, maximize_minimize])
        self.value = None
        return

    def parse_response(self, response):
        self.value = self.parse_response_string(response[:-1])
