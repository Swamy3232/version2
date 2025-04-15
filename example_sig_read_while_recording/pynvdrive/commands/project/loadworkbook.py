from ... import Command


class LoadWorkbook(Command):
    """
    Allows the user to load a workbook of the workbook library.

    parameters:

        - Project name

    opional parameters:

        - Measurement name
        - Save
        - Settings
        - ControlPanel
        - Layouts
        - Setup
        - Print setup


    """
    def __init__(self, project_name, measurement_name='', save='', settings='', control_panel='', layouts='', setup='', print_setup=''):
        super().__init__(name=None, parameters=[project_name, measurement_name, save, settings, control_panel, layouts, setup, print_setup])
        self.value = None
        return

    def parse_response(self, response):
        pass
