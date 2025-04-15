from ... import CommandAction


class LogWarning(CommandAction):
    def __init__(self, msg):
        super().__init__(name=None, parameters=[msg])
        self.value = None
        return

    def parse_response(self, response):
        return