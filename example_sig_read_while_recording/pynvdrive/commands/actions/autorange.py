from ... import Command

class Autorange(Command):
    """
    Do or stop the auto range according to the NVGate settings.

    optional parameters:

        - DoAutorange: 1(activated) or 0(stopped), default=1
        - MasterOrSlave: 1(master) or 2(slave), default=1
    """
    def __init__(self, do_autorange = '', master_or_slave = ''):
        super().__init__(name=None, parameters=[str(do_autorange), str(master_or_slave)])
        self.value = None
        return

    def parse_response(self, response):
        return