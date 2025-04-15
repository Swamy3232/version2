from ... import Command


class DeleteModel(Command):
    """
    Allows the user to load a workbook of the workbook library.

    parameters:

        - Workbook name

    optional parameters:

        - Path


    """
    def __init__(self, workbook_name, relative_path='User'):
        super().__init__(name=None, parameters=[str(relative_path), str(workbook_name)])
        self.value = None
        return

    def parse_response(self, response):
        pass
