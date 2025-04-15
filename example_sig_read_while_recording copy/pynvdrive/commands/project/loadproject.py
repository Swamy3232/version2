from ... import Command


class LoadProject(Command):
    """
    Allows the user to load a project

    parameters:

        - Project name

    optionals parameters:

        - Project database name
        - Save
            - 0 load without saving current
            - 1(default) open confirmation dialog box

    """
    def __init__(self, project_name, project_database_name='', save=''):
        super().__init__(name=None, parameters=[project_name, project_database_name, str(save)])
        self.value = None
        return

    def parse_response(self, response):
        return
