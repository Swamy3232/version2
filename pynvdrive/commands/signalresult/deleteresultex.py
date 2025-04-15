from ... import Command


class DeleteResultEx(Command):
    """
    Delete a result created with the command CreateResultEx.

    parameters:

        - ModuleNumber
        - ProcessNumber
        - ChannelNumber

    optional parameters:

        - ReferenceChannelNumber
        - WaterfallFlag

    """
    def __init__(self, module, process, channel):
        super().__init__(name=None, parameters=[module, process, channel])
        self.value = None
        return

    def parse_response(self, response):
        return response
