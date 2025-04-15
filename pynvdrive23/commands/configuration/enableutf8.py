from ... import CommandAction


class EnableUTF8(CommandAction):
    def __init__(self):
        super().__init__(name=None, parameters=[])
        self.value = None
        return