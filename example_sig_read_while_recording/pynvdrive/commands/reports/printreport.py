from ... import Command


class PrintReport(Command):
    def __init__(self, template_name, return_filename = '', auto_close_query = ''):
        super().__init__(name=None, parameters=[template_name, str(return_filename), str(auto_close_query)])
        self.value = None
        return

    def parse_response(self, response):
        return None