from ... import Command


class ReportSelectInteractiveDocument(Command):
    def __init__(self, index = '0'):
        super().__init__(name=None, parameters=[str(index)])
        self.value = None
        return

    def parse_response(self, response):
        return None