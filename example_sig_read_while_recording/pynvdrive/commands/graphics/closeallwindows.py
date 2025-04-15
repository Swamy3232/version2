from ... import Command


class CloseAllWindows(Command):
    def __init__(self, layout_name):
        super().__init__(name=None, parameters=[layout_name])
        self.value = None
        return

    def parse_response(self, response):
        return None
