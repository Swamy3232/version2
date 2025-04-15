from ... import Command


class OpenProject(Command):
    def __init__(self, project_name, workbook_type = 0, workbook_name = ''):
        super().__init__(name=None, parameters=[project_name, str(workbook_type), workbook_name])
        self.value = None
        return

    def parse_response(self, response):
        pass
