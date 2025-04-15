from ... import Command


class SaveWorkbook(Command):
    """
    Allows the user to save the current workbook.
    """
    def __init__(self):
        super().__init__(name=None, parameters=[])
        self.value = None
        return

    def parse_response(self, response):
        return
