from ... import Command

class CheckTEDS(Command):
    """
    Do the check TEDS on the channels whose coupling is ICP TEDS.

    optional parameters:

        - master_or_slave: 1(master) or 2(slave), default=1
        - input: input number, default=0(all)
        - silent: 0(unactivated) or 1(activated), default=1
    """
    def __init__(self, master_or_slave = '', input = '', silent = ''):
        super().__init__(name=None, parameters=[str(master_or_slave), str(input), str(silent)])
        self.value = None
        return

    def parse_response(self, response):
        return