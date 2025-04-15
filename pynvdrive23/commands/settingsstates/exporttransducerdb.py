from ... import Command


class ExportTransducerDB(Command):
    """
    Exports a transducer database file to a text file

    :param file: full path to the file to export to (including “.txt” extension), from the NVGate’s computer point of view
    :type file: string
    :return: no return
    """
    def __init__(self, file):
        super().__init__(name=None, parameters=[file])
        self.value = None
        return

    def parse_response(self, response):
        pass