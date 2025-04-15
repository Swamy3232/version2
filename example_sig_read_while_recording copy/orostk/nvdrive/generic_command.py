class GenericCommand(object):
    """
    This class represents a generic command with methods that need
    to be implemented at least
    """

    def __init__(self):
        self.return_code = None
        self.error_code = None

    def run(self, socket):
        """ Abstract method to run a GenericCommand

        :return: True if succeed, else False
        """
        raise NotImplementedError
