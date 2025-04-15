from ... import Command


class GetUnitList(Command):
    def __init__(self, magnitude_name):
        super().__init__(name=None, parameters=[magnitude_name])
        self.value = None
        return

    def parse_response(self, response):
        try:
            _, _ = response.split(b'\0', 1)
        except Exception:
            raise NotImplementedError('No window displayed into chosen layout')

        self.value = self.parse_response_list_string(response)
