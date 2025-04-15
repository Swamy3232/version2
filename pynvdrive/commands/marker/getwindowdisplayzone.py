from ... import Command
import struct
from enum import Enum


class GetWindowDisplayZone(Command):
	def __init__(self, window_name: str):
		super().__init__(name=None, parameters=[window_name])
		self.value = None
		self.list_display_zone_type = []
		return

	def parse_response(self, response):
		if not response:
			return None

		# Unpack list of short to a list of int
		self.list_display_zone_type = []
		# Iterate to read short from response byte
		while len(response) >= 2:
			# Read short
			short = struct.unpack('h', response[:2])[0]
			# Remove short from response
			response = response[2:]
			# Append short to list
			self.list_display_zone_type.append(short)

		if len(self.list_display_zone_type) > 0:
			self.value = self.list_display_zone_type[0]
		return
