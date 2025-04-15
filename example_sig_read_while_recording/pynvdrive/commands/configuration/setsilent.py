from ... import Command


class SetSilent(Command):
    def __init__(self, nSilent): # 1 to avoid message, 0 to get them
        super().__init__(name=None, parameters=[str(nSilent)])
        return

    def parse_response(self, response):
        return
