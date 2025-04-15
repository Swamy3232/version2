from ... import Command


class SaveWorkbookModel(Command):
    """
    Allows the user to save the current workbook as a model.

    parameters:

        - Workbook model name

    """
    def __init__(self, model_name):
        super().__init__(name=None, parameters=[model_name])
        self.value = None
        return

    def parse_response(self, response):
        return

