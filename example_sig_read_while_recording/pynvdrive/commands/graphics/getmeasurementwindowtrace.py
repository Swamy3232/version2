from ... import Command


class GetMeasurementWindowTrace(Command):
    def __init__(self, layout, window, trace_index = '0'):
        super().__init__(name=None, parameters=[layout, window, str(trace_index)])
        self.value = None
        return

    def parse_response(self, response):
        self.value = self.parse_response_list_string(response)
