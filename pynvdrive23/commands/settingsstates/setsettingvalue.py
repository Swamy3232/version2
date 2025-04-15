from ... import CommandAction


class SetSettingValue(CommandAction):
    def __init__(self, idn, value):
        super().__init__(name=None, parameters=[idn, '', '', str(value)])
        self.idn = idn
        self.value = value
        return
