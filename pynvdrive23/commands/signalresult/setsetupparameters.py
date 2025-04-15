from ... import CommandAction


class SetSetupParameters(CommandAction):
    def __init__(self, measurementName, incrementType = '1'):
        super().__init__(name=None, parameters=[measurementName, str(incrementType)])
        self.value = None
        return
