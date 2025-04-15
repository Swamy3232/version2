from ... import Command


class GetLayoutList(Command):
    def __init__(self):
        super().__init__(name=None, parameters=[])
        self.value = None
        return

    def parse_response(self, response):
        try:
            self.value = self.parse_response_list_string(response)
        except (Exception,):
            pass
