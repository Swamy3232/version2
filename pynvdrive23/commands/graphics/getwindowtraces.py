from ... import Command
from ...formats.result_format_and_description import ResultFormatAndDescription


class GetWindowTraces(Command):
    def __init__(self, window_name):
        super().__init__(name=None, parameters=[window_name])
        self.value = None
        self.result_format_and_description = None
        return

    def parse_response(self, response):
        try:
            _, _ = response.split(b'\0', 1)
        except (Exception,):
            pass
            # raise NotImplementedError('No window displayed into chosen layout')

        self.result_format_and_description = self.parse_response_result_format_and_description(response)
        self.value = self.result_format_and_description.to_list()

    @staticmethod
    def parse_response_result_format_and_description(contents):
        return ResultFormatAndDescription.from_bytes(contents)
