from ... import Command
from ...formats.result import Result


class GetResultRecordSignalBlock(Command):
    """GetResultRecordSignalBlock
    This command reads samples from the track <Track number> of [Record number] (Record 1 by default).

    :param track_number: track number
    :param sample_number: sample number to start reading
    :param size: size, the number of samples to read from the position
    :param details: details, requested details metadata, 0: no details, 1: details
    :param record_number: record number

    :returns: Result
    """
    def __init__(self, track_number, sample_number, size, details, record_number=1):
        super().__init__(name=None, parameters=[str(track_number), str(sample_number), str(size), str(details),
                                                str(record_number)])
        self.result = None

        self.track_number = track_number
        self.sample_number = sample_number
        self.record_number = record_number

        return

    def parse_response(self, response):
        self.result = Result.from_binary(binary=response)

        # self.result.track_number = self.track_number
        # self.result.sample_number = self.sample_number
        # self.result.record_number = self.record_number

        return self.result
