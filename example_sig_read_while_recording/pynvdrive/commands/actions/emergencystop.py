from ... import CommandAction

class EmergencyStop(CommandAction):
    def __init__(self):
        super().__init__(name=None, parameters=[])
        self.value = None
        return