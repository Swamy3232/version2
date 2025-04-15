from ... import Command


class ReportGetInteractiveDocumentList(Command):
    def __init__(self):
        super().__init__(name=None, parameters=[])
        self.value = None
        return

    def parse_response(self, response):
        # print(response)
        try:
            _, _ = response.split(b'\0', 1)
        except Exception:
            raise NotImplementedError('No window displayed into chosen layout')

        self.value = self.parse_response_list_string(response)
