from ... import Command


class CreateResultEx(Command):
    """
    Prepare a result to be retrieved with the command GetResultEx.

    parameters:

        - ModuleNumber
        - ProcessNumber
        - ChannelNumber

    optional parameters:

        - ReferenceChannelNumber
        - WaterfallFlag

    """
    def __init__(self, module, process, channel, reference_channel_number = 1, waterfall_flag = 0):
        super().__init__(name=None, parameters=[str(module), str(process), str(channel), str(reference_channel_number), str(waterfall_flag)])
        self.value = None
        return

    def parse_response(self, response):
        return response
