from ... import Command


# frontEnd.969:1 => Get List System

class GetSubModuleList(Command):
    def __init__(self, submodule):
        super().__init__(name=None, parameters=[submodule])
        self.value = None
        return

    def parse_response(self, response):
        self.value = self.parse_response_string(response[:-1])