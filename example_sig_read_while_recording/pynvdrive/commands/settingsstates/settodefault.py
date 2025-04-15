from ... import CommandAction


class SetToDefault(CommandAction):
    def __init__(self, module, sub_module, setting):
        super().__init__(name=None, parameters=[str(module), str(sub_module), str(setting)])
        self.value = None
        return
