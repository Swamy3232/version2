from ... import Command
from ...formats.result_format_and_description import ResultFormatAndDescription


class GetWindowTraces(Command):
    def __init__(self, window_name):
        super().__init__(name=None, parameters=[window_name])
        self.list_result_format_and_description = []
        self.value = None
        self.traces = []
        return

    def parse_response(self, response):
        if not response:
            return None

        try:
            _, _ = response.split(b'\0', 1)
        except Exception:
            raise NotImplementedError('Error using GetResultList')

        self.list_result_format_and_description = self.parse_response_result_format_and_description_list(response)
        self.traces = [i.to_list() for i in self.list_result_format_and_description]
        self.value = self.traces

    def parse_response_result_format_and_description_list(self, contents):
        list_result_format_and_description = []
        contents_splitted = contents.split(b'-')

        # Fix issue if "-" in the input name (e.g. "Input-1"), because it's used as a separator for this command
        new_contents_splitted = []
        for content in contents_splitted:
            test_pre_parse = self.pre_parse_response_result_format_and_description(content)
            # If result False, then we need to concatenate the previous content with the current content
            if test_pre_parse:
                new_contents_splitted.append(content)
            else:
                new_contents_splitted[-1] = b'-'.join([new_contents_splitted[-1], content])

        for content in new_contents_splitted:
            current = self.parse_response_result_format_and_description(content)
            list_result_format_and_description.append(current)

        return list_result_format_and_description

    @staticmethod
    def parse_response_result_format_and_description(contents):
        return ResultFormatAndDescription.from_bytes(contents)

    @staticmethod
    def pre_parse_response_result_format_and_description(contents):
        """
        Pre-parse the response to get the list of result format and description and check if error
        """
        try:
            test = ResultFormatAndDescription.from_bytes(contents)
            if test.input_name is not None and test.input_name != '':
                return True
            else:
                return False
        except Exception:
            return False
        return True
