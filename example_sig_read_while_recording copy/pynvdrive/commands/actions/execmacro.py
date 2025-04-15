from ... import Command

class ExecMacro(Command):
    def __init__(self, macro_name):
        super().__init__(name=None, parameters=[macro_name])
        self.value = None
        return

    def parse_response(self, response):
        return