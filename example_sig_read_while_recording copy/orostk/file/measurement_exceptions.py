"""
This module contains exceptions that are raised when a measurement method fails.
"""


class NVGateMeasurementException(Exception):
	"""
	Base class for NVGate measurement exceptions.
	"""
	pass


class NVGateRecordException(NVGateMeasurementException):
	"""
	Exception raised when a record method fails.
	"""
	pass


class NVGateChannelsException(NVGateMeasurementException):
	"""
	Exception raised when a channel method fails.
	"""
	pass


class NVGSException(Exception):
	"""
	Base class for NVGate measurement exceptions.
	"""
	def __init__(self, message, error_code=None):
		super().__init__('{} err {} : {}'.format(self.__class__.__name__, error_code, message))
		self.message = message
		self.error_code = error_code
		print('{} err {} : {}'.format(self.__class__.__name__, error_code, message))


class NVGSRecordException(NVGSException):
	"""
	Exception raised when a record method fails.
	Same as NVGateRecordException, but used for methods while recording and thus NVGate running.
	"""
	pass


class NVGSTreeException(NVGSException):
	"""
	Exception raised when a tree method fail, like invalid measurement id.
	"""
	pass