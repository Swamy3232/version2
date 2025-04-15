from ... import Command


class AddAutoOperator(Command):
    def __init__(self, layout, window, module, process, channel, reference_channel_number=0, weighting_operator=0,
                 time_operator=0, display_unit=0, waterfall=0, average_type=0, automatic_selection_type='',
                 operator_name='', frequency_domain=1, step=''):
        super().__init__(name=None, parameters=[layout, window, str(module), str(process), str(channel),
                                                str(reference_channel_number), str(weighting_operator),
                                                str(time_operator), str(display_unit), str(waterfall),
                                                str(average_type), str(automatic_selection_type), operator_name,
                                                str(frequency_domain), str(step)])
        self.value = None
        return

    def parse_response(self, response):
        self.value = self.parse_response_string(response[:-1])
