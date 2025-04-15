from ... import Command
from ...formats.result_format_and_description import ResultFormatAndDescription


class GetSavedResultList(Command):
    def __init__(self, measurement_name, project_name=''):
        super().__init__(name=None, parameters=[measurement_name, project_name])
        self.value = []
        return

    def parse_response(self, response):
        try:
            _, _ = response.split(b'\0', 1)
        except Exception:
            raise NotImplementedError('No saved results inside choosen measurement')

        # print(response)
        temp = self.parse_response_list_string(response)
        for i in range(0, len(temp)):
            myTrace = ResultFormatAndDescription()
            myTrace.module_id = int.from_bytes(temp[i][0:2], byteorder='little', signed=False)
            myTrace.process_id = int.from_bytes(temp[i][2:6], byteorder='little', signed=False)
            myTrace.channel_number = int.from_bytes(temp[i][6:10], byteorder='little', signed=False)
            myTrace.input_name = self.parse_response_string(temp[i][14:].split(b'\0')[0])
            self.value.append(myTrace)

    @staticmethod
    def parse_response_list_string(contents):
        contents = contents.split(b'-')
        return contents
