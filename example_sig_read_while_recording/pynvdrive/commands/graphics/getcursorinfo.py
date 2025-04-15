from ... import Command, NVDriveCommandParsing
import re


class cursor:
    def __init__(self):
        self.type = None
        self.frequency = None
        self.time = None
        self.level = None
        self.slice = None
        return


class GetCursorInfo(Command):
    def __init__(self, layout, window):
        super().__init__(name=None, parameters=[layout, window])
        self.layout = layout
        self.window = window
        self.value = None
        self.cursor1 = cursor()
        self.cursor2 = cursor()
        return

    def parse_response(self, response):
        try:
            value_type, contents = response.split(b'\n', 1)
            # print(contents)
        except (Exception,):
            self.cursor1.frequency = 0
            self.cursor1.slice = 0
            self.cursor2.frequency = 0
            self.cursor2.slice = 0
            return

        if value_type == b'Cursor1':
            self.value = self.parse_response_cursor(response)

            lines = self.value.split('\n')
            currentCursor = 0
            for i in lines:
                if 'Cursor1' in i :
                    currentCursor = 1
                elif 'Cursor2' in i:
                    currentCursor = 2

                if currentCursor == 1:
                    if 'Hz' in i and self.cursor1.frequency is None:
                        self.cursor1.frequency = re.findall(r"[-+]?\d*\.\d+|\d+", i)[0]
                    if 'Slice' in i and self.cursor1.slice is None:
                        self.cursor1.slice = re.findall(r"[-+]?\d*\.\d+|\d+", i)[0]
                elif currentCursor == 2:
                    if 'Hz' in i and self.cursor2.frequency is None:
                        self.cursor2.frequency = re.findall(r"[-+]?\d*\.\d+|\d+", i)[0]
                    if 'Slice' in i and self.cursor2.slice is None:
                        self.cursor2.slice = re.findall(r"[-+]?\d*\.\d+|\d+", i)[0]

        else:
            raise NotImplementedError('GetSettingValue not yet implemented setting type: ' + str(value_type))
        return

    def parse_response_cursor(self, contents):
        if not contents.endswith(b'\0'):
            raise NVDriveCommandParsing('expected trailing zero')
        # Note: the current NVGate implementation does not support unicode for this command
        return self.parse_response_string(contents[:-1])
