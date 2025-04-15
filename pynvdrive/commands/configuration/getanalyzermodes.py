from ... import Command
import struct


class GetAnalyzerModes(Command):
	def __init__(self):
		super().__init__(name=None, parameters=[])
		self.value = None
		self.analysis_mode = None
		self.connection_mode = None
		return

	def parse_response(self, response):
		# Unpack short
		if len(response) == 4:
			self.analysis_mode = struct.unpack('h', response[:2])[0]
			self.connection_mode = struct.unpack('h', response[2:])[0]
			self.value = [self.analysis_mode, self.connection_mode]
		else:
			self.value = [None, None]
