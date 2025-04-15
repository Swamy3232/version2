from ... import Command

class ShutDown(Command):
    """
    Allows the user to close the server application.

    optional parameters:

        - Save: 0(no save) 1(save), default=0

    """
    def __init__(self, save):
        super().__init__(name=None, parameters=[str(save)])
        self.value = None
        return

    def parse_response(self, response):
        return