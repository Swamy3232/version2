from ... import Command


class ImportFile(Command):
    def __init__(self, import_type, file, directory, project = '', delete = ''):
        super().__init__(name=None, parameters=[str(import_type), file, directory, project, delete])
        self.value = None
        return

    def parse_response(self, response):
        self.value = self.parse_response_string(response[:-1])
