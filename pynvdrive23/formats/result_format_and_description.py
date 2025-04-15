from copy import copy

from .modules import modules as nvg_modules, modules_alternative_names as nvg_modules_alternative_names
from .process import processes as nvg_processes, processes_without_unit
from ..quantity.unit import Unit
from ..quantity.quantity_provider import QuantityProvider
from pynvdrive import ENCODING


class ResultFormatAndDescription:
	"""
	Result format and description as described in NVDrive documentation

	"""

	def __init__(self, module_id=None, process_id=None, channel_number=None, reference_channel_number=None,
	             input_name=None, input_name_reference_channel_number=None, data=None, unit: Unit = None):
		self._module_id = module_id
		self._process_id = process_id
		self._channel_number = channel_number
		self._reference_channel_number = reference_channel_number
		self._input_name = input_name
		self._input_name_reference_channel_number = input_name_reference_channel_number

		if not unit:
			self.unit = Unit()
		else:
			self.unit = unit

		self._data = data

		# USED FOR MONITORING
		self._is_multiple_channel = False  # Flag if the result is associated to different channel of same module/process

		# Marker information if the result is from a marker
		self._marker_name = None
		self._marker_position = None
		return

	def update_unit(self, client=None, quantity_provider: QuantityProvider = QuantityProvider(), use_result_ex=False):
		if use_result_ex:
			self.unit = quantity_provider.get_unit_from_result_ex(client=client, result_format_and_description=self)
		else:
			if self.process_id in processes_without_unit:
				self.unit = Unit(magnitude_name='No Magnitude', magnitude_key='None', unit_name='No Units', unit_label='', coeff_A=1.0, coeff_B=0.0)
				return

			elif self.is_tach:  # Tach
				self.unit = quantity_provider.get_unit_user(magnitude_key='Angular_Velocity')
				return
			else:
				# self.unit = quantity_provider.get_unit_input_name(client=client, input_name=self.input_name)
				self.unit = quantity_provider.get_unit_from_module_channel(module_id=self.module_id,
				                                                           channel_number=self._channel_number,
				                                                           process_id=self._process_id,
				                                                           client=client)
				if '[Tors]' in self.input_name:
					self.unit = quantity_provider.get_unit_user(magnitude_key='Torsional_Acceleration')

	@property
	def module_id(self):
		return self._module_id

	@property
	def process_id(self):
		return self._process_id

	@property
	def channel_number(self):
		return self._channel_number

	@property
	def input_name(self):
		return self._input_name

	def get_input_name(self, include_marker=False):
		if self.is_marker() and include_marker:
			return '{}_{}'.format(self.input_name, self._marker_name)
		else:
			return self.input_name

	@property
	def reference_channel_number(self):
		return self._reference_channel_number

	@property
	def input_name_reference_channel_number(self):
		return self._input_name_reference_channel_number

	@property
	def data(self):
		return self._data

	@module_id.setter
	def module_id(self, value):
		self._module_id = value

	@process_id.setter
	def process_id(self, value):
		self._process_id = value

	@channel_number.setter
	def channel_number(self, value):
		self._channel_number = value

	@input_name.setter
	def input_name(self, value):
		self._input_name = value

	@reference_channel_number.setter
	def reference_channel_number(self, value):
		self._reference_channel_number = value

	@input_name_reference_channel_number.setter
	def input_name_reference_channel_number(self, value):
		self._input_name_reference_channel_number = value

	@data.setter
	def data(self, value):
		self._data = value

	# Alias
	channelNumber = channel_number
	inputName = input_name

	def set_marker(self, marker_name, marker_position):
		self._marker_name = marker_name
		self._marker_position = marker_position

	def get_marker_position(self):
		return self._marker_position

	def remove_marker(self):
		self._marker_name = None
		self._marker_position = None

	def is_marker(self):
		return self._marker_name is not None

	def to_list(self):
		return [self.module_id, self.process_id, self.channel_number, self.reference_channel_number, self.input_name,
		        self.input_name_reference_channel_number]

	def to_dict(self):
		my_dict = {'input_name': self.input_name, 'module_id': self.module_id, 'process_id': self.process_id,
		           'channel_number': self.channel_number, 'reference_channel_number': self.reference_channel_number,
		           'input_name_reference_channel_number': self.input_name_reference_channel_number}
		if self._is_multiple_channel:
			my_dict['is_multiple_channel'] = True
		if self.unit is not None:
			my_dict['unit'] = self.unit.to_dict()
		if self.is_marker():
			my_dict['marker_name'] = self._marker_name
			my_dict['marker_position'] = self._marker_position
		return copy(my_dict)

	@classmethod
	def from_dict(cls, data) -> 'ResultFormatAndDescription':
		result = cls(input_name=data.get('input_name', None), module_id=data.get('module_id', None),
		           process_id=data.get('process_id', None), channel_number=data.get('channel_number', None),
		           reference_channel_number=data.get('reference_channel_number', None),
		           input_name_reference_channel_number=data.get('input_name_reference_channel_number', None))

		if data.get('is_multiple_channel', None) is not None:
			setattr(result, '_is_multiple_channel', data.get('is_multiple_channel'))
		if data.get('unit', None) is not None:
			setattr(result, 'unit', Unit.from_dict(data.get('unit')))
		if data.get('marker_name', None) is not None:
			setattr(result, '_marker_name', data.get('marker_name'))
		if data.get('marker_position', None) is not None:
			setattr(result, '_marker_position', data.get('marker_position'))
		return result

	@staticmethod
	def from_bytes(contents):
		current_trace = ResultFormatAndDescription()
		current_trace.module_id = int.from_bytes(contents[0:2], byteorder='little', signed=False)
		current_trace.process_id = int.from_bytes(contents[2:6], byteorder='little', signed=False)
		current_trace.channel_number = int.from_bytes(contents[6:10], byteorder='little', signed=False)
		current_trace.reference_channel_number = int.from_bytes(contents[10:14], byteorder='little', signed=False)
		current_trace.input_name = str(contents[14:].split(b'\0')[0].decode(ENCODING))

		if len(contents[14:].split(b'\0')) > 1 and current_trace.reference_channel_number != 0:
			current_trace.input_name_reference_channel_number = str(contents[14:].split(b'\0')[1].decode(ENCODING))
		else:
			current_trace.input_name_reference_channel_number = ''

		return current_trace

	@property
	def analysis_fullname(self):
		"""
		Return the fullname of the analysis
		eg: FFT1: AvgSpc (from module = 10 and process = 2)
		"""
		# return '{}: {}'.format(nvg_modules.get(self.module_id, self.module_id),
		# 					   nvg_processes.get(self.process_id, self.process_id))
		nvg_module_name = nvg_modules.get(self.module_id, self.module_id)
		fullname = '{}: {}'.format(nvg_modules_alternative_names.get(nvg_module_name, nvg_module_name),
		                           nvg_processes.get(self.process_id, self.process_id))
		if self._is_multiple_channel:
			fullname += ' [{}]'.format(self.channel_number)
		# fullname = '{}'.format(nvg_processes.get(self.process_id, self.process_id))
		# if self._is_multiple_channel:
		# 	fullname += ' [{}]'.format(self.channel_number)
		# fullname += ': {}'.format(nvg_processes.get(self.process_id, self.process_id))
		# print('Fullname from result format and description: {}'.format(fullname))
		return fullname

	@property
	def user_unit_label(self):
		return self.unit.unit_label

	def get_si_value_from_user_value(self, user_value):
		if self.unit:
			return self.unit.get_si_value_from_user_value(user_value)
		else:
			return user_value

	def get_user_value_from_si_value(self, si_value):
		if si_value is None:
			return None
		if self.unit:
			return self.unit.get_user_value_from_si_value(si_value)
		else:
			return si_value

	@property
	def is_tach(self):
		"""
		Return True if the result is a tachometer
		"""
		if self.module_id == 6:
			return True
		else:
			return False

	# USED FOR MONITORING
	@property
	def is_multiple_channel(self):
		return self._is_multiple_channel

	@is_multiple_channel.setter
	def is_multiple_channel(self, value):
		self._is_multiple_channel = value
