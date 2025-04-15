from ... import Command


class UnSelectWtfChannels(Command):
    def __init__(self, process, module, response_channel, reference_channel=''):
        super().__init__(name=None, parameters=[str(process), str(module), str(response_channel), str(reference_channel)])
        self.value = None
        return

    def parse_response(self, response):
        pass
