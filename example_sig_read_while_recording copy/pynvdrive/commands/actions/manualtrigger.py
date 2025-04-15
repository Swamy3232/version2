from ... import CommandAction

class ManualTrigger(CommandAction):
    def __init__(self):
        super().__init__(name=None, parameters=[])
        self.value = None
        return