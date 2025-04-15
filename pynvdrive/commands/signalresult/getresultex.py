from ... import Command
from ...formats.result import Result


class GetResultEx(Command):
    def __init__(self, module, process, channel, reference_channel_number = 0, waterfall_flag = 0, version = 5):
        super().__init__(name=None, parameters=[str(module), str(process), str(channel), str(reference_channel_number), str(waterfall_flag), 'v={}'.format(version)])
        self.value = None
        self.result = None

        self.module_id = module
        self.process_id = process
        self.channel_number = channel
        return

    def parse_response(self, response):
        self.result = Result.from_binary(binary=response)

        # Add module, process and channel number
        self.result.module_id = self.module_id
        self.result.process_id = self.process_id
        self.result.channel_number = self.channel_number

        return self.result
