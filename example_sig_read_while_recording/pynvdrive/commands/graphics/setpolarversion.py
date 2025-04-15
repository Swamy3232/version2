from ... import Command


class SetPolarVersion(Command):
    def __init__(self, version):
        super().__init__(name=None, parameters=[version])
        return

    def parse_response(self, response):
        return None
