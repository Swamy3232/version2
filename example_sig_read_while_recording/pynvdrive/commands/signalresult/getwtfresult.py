from ... import Command
from ...formats.result import Result


class GetWtfResult(Command):
    def __init__(self, module, process, channel, reference_channel_number = 0, get_global_level='', get_pond_global_level_flag='', version_number='', start_index='', wanted_size=''):
        super().__init__(name=None, parameters=[str(module), str(process), str(channel), str(reference_channel_number), str(get_global_level), str(get_pond_global_level_flag), str(version_number), str(start_index), str(wanted_size)])
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

