from ... import Command


class GetTagReferenceList(Command):
    def __init__(self, layout_name, window_name):
        super().__init__(name=None, parameters=[layout_name, window_name])
        self.value = None
        return

    def parse_response(self, response):
        try:
            self.value = self.parse_response_list_string(response)
        except (Exception,):
            pass
