from ... import Command


class RemoveSetupResult(Command):
    def __init__(self, module_number, process_number, channel_number, reference_channel_number='', weighting_operator='', time_operator='', display_unit='', is_waterfall=''):
        super().__init__(name=None, parameters=[str(module_number), str(process_number), str(channel_number), str(reference_channel_number), weighting_operator, time_operator, display_unit, is_waterfall])
        self.value = None
        return

    def parse_response(self, response):
        self.value = self.parse_response_string(response[:-1])
