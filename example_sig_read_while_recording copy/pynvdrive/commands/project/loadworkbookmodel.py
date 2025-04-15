from ... import Command


class LoadWorkbookModel(Command):
    """
    Allows the user to load a workbook of the workbook library.

    parameters:

        - Workbook name

    opional parameters:

        - Path
        - Save
        - Settings
        - ControlPanel
        - Layouts
        - Setup
        - Print setup


    """
    def __init__(self, workbook_name, path='User', save='0', settings='', control_panel='', layouts='', setup='', print_setup=''):
        super().__init__(name=None, parameters=[str(workbook_name), path, str(save), str(settings), str(control_panel), str(layouts), str(setup), str(print_setup)])
        self.value = None
        return

    def parse_response(self, response):
        pass
