from ... import Command

class PlayByStep(Command):
    """
    Play by steps, available only in post-analysis,
    when the file is played by step.
    The command starts a new step or pauses the current step.

    """
    def __init__(self, action):
        super().__init__(name=None, parameters=[str(action)])
        self.value = None
        return

    def parse_response(self, response):
        return