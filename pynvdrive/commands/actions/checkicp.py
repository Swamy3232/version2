from ... import Command

class CheckICP(Command):
    """
    Do the check ICP on the channels whose coupling is ICP.

    optional parameters:

        - MasterOrSlave: 1(master) or 2(slave), default=1
    """
    def __init__(self, master_or_slave = ''):
        super().__init__(name=None, parameters=[str(master_or_slave)])
        self.value = None
        return

    def parse_response(self, response):
        return