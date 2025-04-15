from ... import Command
from ...formats.result_format_and_description import ResultFormatAndDescription


class GetAvailableResultList(Command):
    def __init__(self, module_id, result_type=0): # Result type : 0 DISPLAY, 1 WATERFALL_CONNECTION, 2 SAVE_SETUP
        super().__init__(name=None, parameters=[str(module_id), str(result_type)])
        self.value = None
        self.list = []
        return

    def parse_response(self, response):
        if not response:
            return None

        try:
            _, _ = response.split(b'\0', 1)
        except Exception:
            raise NotImplementedError('Error using GetAvailableResultList')

        # print(response)
        self.value = self.parse_response_list_string(response)
        for i in range(0, len(self.value)):
            myTrace = ResultFormatAndDescription()
            myTrace.module_id = int.from_bytes(self.value[i][0:2], byteorder='little', signed=False)
            myTrace.process_id = int.from_bytes(self.value[i][2:6], byteorder='little', signed=False)
            myTrace.channelNumber = int.from_bytes(self.value[i][6:10], byteorder='little', signed=False)
            myTrace.inputName = self.parse_response_string(self.value[i][14:].split(b'\0')[0])

            self.list.append(myTrace)

    @staticmethod
    def parse_response_list_string(contents):
        contents = contents.split(b'-')
        return contents
