from ... import Command


class ReportRefreshPrint(Command):
    def __init__(self, do_refresh = '0', do_print = '0'):
        super().__init__(name=None, parameters=[str(do_refresh), str(do_print)])
        self.value = None
        return

    def parse_response(self, response):
        return None
