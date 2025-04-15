from ... import CommandAction


class ChangeDisplayMode(CommandAction):
    def __init__(self, layout, window, mode):
        super().__init__(name=None, parameters=[layout, window, mode])
        return
