from ... import Command


class GetWindowNameList(Command):
    def __init__(self, layout=''):
        super().__init__(name=None, parameters=[layout])
        self.layout = layout
        self.windowList = None
        self.value = None
        return

    def parse_response(self, response):
        try:
            _, _ = response.split(b'\0', 1)
        except (Exception,):
            pass
            # raise NotImplementedError('No window displayed into chosen layout')

        self.windowList = self.parse_response_list_string(response)
        self.value = self.windowList
