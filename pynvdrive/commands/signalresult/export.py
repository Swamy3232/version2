from ... import Command


class Export(Command):
    def __init__(self, ExportType, Project, Measurement, ExportDirectory):
        super().__init__(name=None, parameters=[ExportType, Project, Measurement, ExportDirectory])
        self.value = None
        return

    def parse_response(self, response):
        self.value = self.parse_response_string(response[:-1])
