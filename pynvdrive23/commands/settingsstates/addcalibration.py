from ... import Command
from enum import Enum


class TransducerType(Enum):
	MICROPHONE = 0
	ACCELEROMETER = 1
	VOLTMETER = 3
	AMMETER = 4
	VELOCITY_SENSOR = 5
	TACHOMETER = 6
	DISPLACEMENT_SENSOR = 7
	PRESSURE_SENSOR = 8
	FORCE_SENSOR = 9


class AddCalibration(Command):
	"""
    Add a calibration to the database
    # The <Calibration type> is an integer corresponding to the following cases:
    # •	Manual calibration		0
    # •	Acoustic calibration		1
    # •	Accelerometer calibration	2
    # •	A * x + B calibration		3
    # •	Frequency calibration		4
    # •	Initial factory calibration	5
    # •	Update factory calibration	6
    """

	def __init__(self, transducer_ID, sensitivity, offset, calibration_type, input_name, user_name='',
	             calibrator_name=''):
		super().__init__(name=None,
		                 parameters=[str(transducer_ID), str(sensitivity), str(offset), str(calibration_type),
		                             str(input_name), str(user_name), str(calibrator_name)])
		self.value = None

		return

	def parse_response(self, response):
		pass
