import struct

from ... import Command
from enum import Enum


class TriggerState(Enum):
	"""
	Enum for TriggerState, following nvdrive.doc
	"""
	RUNNING = 0
	RECORDING = 1
	TRIGGERING = 2
	BLOC_TRIGGERING = 3
	WAITING = 4
	PAUSED = 5
	STOPPED = 6


class GetAnalyzerState(Command):
	def __init__(self, module, state_name=''):
		"""
		Get analyzer state
		:param module: module name
		:param state_name: state name
		state_name : 'Trigger state', 'Count', 'Real-time', 'Block overload', 'Analysis overload', \
		Record counter', 'Time to stabilization'
		"""
		super().__init__(name=None, parameters=[str(module), state_name])
		self.value = None
		self.state: TriggerState = None
		return

	def parse_response(self, response):
		# Check if string b'Stopped\x00'
		contents = response.split(b'\0', 1)
		try:
			result = self.parse_response_string(contents[0])
		except (Exception,):
			result = None

		if result:
			self.value = result
			if result == 'Running':
				self.state = TriggerState.RUNNING
			elif result == 'Recording':
				self.state = TriggerState.RECORDING
			elif result == 'Triggering':
				self.state = TriggerState.TRIGGERING
			elif result == 'Block triggering':
				self.state = TriggerState.BLOC_TRIGGERING
			elif result == 'Waiting':
				self.state = TriggerState.WAITING
			elif result == 'Paused':
				self.state = TriggerState.PAUSED
			elif result == 'Stopped':
				self.state = TriggerState.STOPPED
			return

		if not result:
			try:
				contents = response
				float_number = struct.unpack('f', contents[0:4])[0]
				self.value = float_number
				return
			except (Exception,):
				return False
