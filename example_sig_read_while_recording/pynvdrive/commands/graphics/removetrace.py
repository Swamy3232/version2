from ... import Command


class RemoveTrace(Command):
    def __init__(self, window_name, trace_number):
        super().__init__(name=None, parameters=[window_name, str(trace_number)])
        self.value = None
        return

    def parse_response(self, response):
        return None
