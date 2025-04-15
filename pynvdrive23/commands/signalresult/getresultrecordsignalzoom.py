from ... import Command
from ...formats.result import Result


class GetResultRecordSignalZoom(Command):
	"""GetResultRecordSignalZoom

    :param track_number: track number
	:param t0: start time
	:param t1: end time
	:param size: size, the number of samples to read from the position
    :param details: details, requested details metadata, 0: no details, 1: details
	:param record_number: record number

	:returns: Result
	"""
	def __init__(self, track_number, t0, t1, size, details, record_number=1):
		super().__init__(name=None, parameters=[str(track_number), str(t0), str(t1), str(size), str(details),
		                                        str(record_number)])
		self.result = None

		self.track_number = track_number
		self.t0 = t0
		self.t1 = t1
		self.record_number = record_number

		return

	def parse_response(self, response):
		self.result = Result.from_binary(binary=response)

		# self.result.track_number = self.track_number
		# self.result.t0 = self.t0
		# self.result.t1 = self.t1
		# self.record_number = self.record_number

		return self.result
