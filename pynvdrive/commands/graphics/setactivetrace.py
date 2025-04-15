from ... import Command


class SetActiveTrace(Command):
    def __init__(self, layout_name, window_name, trace_index):
        super().__init__(name=None, parameters=[layout_name, window_name, str(trace_index)])
        self.value = None
        return

    def parse_response(self, response):
        return None
