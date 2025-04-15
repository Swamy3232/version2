import struct

from ... import Command
from enum import Enum


class GetStatus(Command):
	def __init__(self):
		"""
		Get application status
		"""
		super().__init__(name=None, parameters=[])
		self.value = None
		self.measurement_in_progress = None  # 1 Measurement in progress, 0 otherwise
		self.analyzers_status = None  # 0 office, 1 analyzers, 2 frontend (OR10, O4)
		return

	def parse_response(self, response):
		# Response is a 2 x 2 bytes short
		# First short is the measurement in progress
		# Second short is the analyzers status

		if len(response) != 4:
			return

		# First short
		try:
			# Unpack short
			result = struct.unpack('<h', response[0:2])[0]
		except (Exception,):
			result = None

		if result is not None:
			self.measurement_in_progress = result

		# Second short
		try:
			result = struct.unpack('<h', response[2:4])[0]
		except (Exception,):
			result = None

		if result is not None:
			self.analyzers_status = result

		self.value = [self.measurement_in_progress, self.analyzers_status]

