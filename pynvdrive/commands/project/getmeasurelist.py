from ... import Command


class GetMeasureList(Command):
    def __init__(self, project_name):
        super().__init__(name=None, parameters=[project_name])
        self.value = None
        return

    def parse_response(self, response):
        try:
            _, _ = response.split(b'\0', 1)
            self.value = self.parse_response_list_string(response)
        except Exception:
            self.value = ['']
