from ... import Command


class GetResultCaption(Command):
    def __init__(self, module, process, channel, reference_channel_number=''):
        super().__init__(name=None, parameters=[str(module), str(process), str(channel), str(reference_channel_number)])
        self.value = None
        return

    def parse_response(self, response):
        self.value = self.parse_response_string(response)

