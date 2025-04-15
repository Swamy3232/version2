from ... import Command
from pynvdrive import ENCODING


class GetTransducerList(Command):
    def __init__(self, transducer_type = ''):
        super().__init__(name=None, parameters=[transducer_type])
        self.value = None
        self.list = None
        return

    def parse_response(self, response):
        try:
            _, _ = response.split(b'\0', 1)
        except Exception:
            raise NotImplementedError('No window displayed into chosen layout')

        self.value = self.parse_response_list_string(response)

        # List them by pairs
        self.list = []
        for i in range(0, len(self.value), 2):
            self.list.append(self.value[i:i+2])
        return
