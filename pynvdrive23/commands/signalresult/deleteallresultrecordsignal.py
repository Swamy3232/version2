from ... import Command


class DeleteAllResultRecordSignal(Command):
    def __init__(self):
        super().__init__(name=None, parameters=[])
        self.value = None
        return

    def parse_response(self, response):
        return response
