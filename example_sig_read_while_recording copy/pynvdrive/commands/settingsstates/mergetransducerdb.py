from ... import Command


class MergeTransducerDB(Command):
    """
    Merges a transducer database file (CDB or TXT) into NVGate’s transducer database

    :param file: full path to the file to import (including “.cdb” or “.txt” extension), from the NVGate’s computer point of view. This file corresponds to the “theirs” column in the NVGate’s merge dialog.
    :type file: string
    :param operation: instructs the operation to perform when a conflict occurs (0:do nothing, 1: use mine, 2: use theirs)
    :type operation: int
    :return: no return

    """
    def __init__(self, file, operation):

        super().__init__(name=None, parameters=[file, str(operation)])
        self.value = None
        return

    def parse_response(self, response):
        pass
