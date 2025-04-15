from ... import Command


class DeleteResultRecordSignal(Command):
    """
    Prepare a result to be retrieved with the command GetResultRecordSignalBlock

    parameters:

        - TrackNumber

    """
    def __init__(self, track_number):
        super().__init__(name=None, parameters=[str(track_number)])
        self.value = None
        return

    def parse_response(self, response):
        return response
