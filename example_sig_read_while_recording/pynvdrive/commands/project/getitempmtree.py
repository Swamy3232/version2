from ... import Command


class GetItemPMTree(Command):
    def __init__(self, project_name='', measurement_name=''):
        super().__init__(name=None, parameters=[project_name, measurement_name])
        self.value = None
        return

    def parse_response(self, response):
        try:
            _, _ = response.split(b'\0', 1)
        except Exception:
            raise NotImplementedError('No tree')

        self.value = self.parse_response_list_string(response)
