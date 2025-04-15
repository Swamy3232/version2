import configparser
import os
from ..client import Client, NVDriveCommandError
from .quantity_exceptions import QuantityError
from .orosunit import orosunit_str
from .unit import Unit
from .utils.nvd_cmd import GetMagnitudeInfo
from .utils.get_all_units import get_all_units
from .utils.get_magnitude_key_from_input import get_magnitude_key_all_inputs, get_magnitude_key_from_input_number, \
	get_magnitude_key_from_input_idn, get_magnitude_key_from_input_name
from pynvdrive.toolbox.get_source_name import get_source_name
from pynvdrive.commands.settingsstates.getsettingvalue import GetSettingValue
from pynvdrive.commands.settingsstates.getsettingvalues import GetSettingValues
import pynvdrive
from pynvdrive.formats.modules import modules as nvg_modules

_OROSUNIT_PATH = 'orosunit.ini'


def get_magnitude_dict(client: Client):
	"""
	Parse orosunit.ini, retrieving a dict associating magnitude_key:magnitude_name
	"""

	if client is None:
		client = pynvdrive.Client()
		client.connect()
	else:
		client.connect()

	magnitude_key = {}
	#
	config = configparser.ConfigParser(interpolation=None)

	orosunit_path = os.path.join(os.path.dirname(__file__), '..', 'quantity', _OROSUNIT_PATH)
	if os.path.exists(orosunit_path):
		config.read(orosunit_path)
	else:
		config.read_string(orosunit_str)

	config = configparser.ConfigParser(interpolation=None)
	config.read_string(orosunit_str)

	base_quantity = int(config['BASE QUANTITY']['Number'])
	for qty_nb in range(0, base_quantity):
		current_magnitude_key = config['BASE QUANTITY']['Quantity{}'.format(qty_nb + 1)]
		try:
			cmd = GetMagnitudeInfo(magnitude_key=current_magnitude_key)
			client.send_command(cmd)
			magnitude_name = cmd.magnitude_name
			magnitude_key[current_magnitude_key] = magnitude_name
		except NVDriveCommandError as e:
			if current_magnitude_key != 'None':
				print('error GetMagnitudeInfo {}'.format(current_magnitude_key), e.error)

	return magnitude_key


def get_simplification_dict():
	"""
	Parse orosunit.ini, retrieving a dict associating combinated magnitude_key:magnitude_key for simplification
	"""
	simplification_dict = {}
	#
	config = configparser.ConfigParser(interpolation=None)

	orosunit_path = os.path.join(os.path.dirname(__file__), '..', 'quantity', _OROSUNIT_PATH)
	if os.path.exists(orosunit_path):
		config.read(orosunit_path)
	else:
		config.read_string(orosunit_str)

	config = configparser.ConfigParser(interpolation=None)
	config.read_string(orosunit_str)

	simplification_number = int(config['SIMPLIFICATION']['Number'])
	for qty_nb in range(0, simplification_number):
		current_line = config['SIMPLIFICATION']['Simplification{}'.format(qty_nb + 1)]
		# Remove spaces and tabs
		current_line = current_line.replace(' ', '')
		current_line = current_line.replace('\t', '')
		magnitude_key = current_line.split('#')[0]
		simplification = current_line.split('#')[1]
		simplification_dict[simplification] = magnitude_key

	return simplification_dict


class QuantityProvider(object):
	"""
	This abstract class helps to retrieve NVGate quantities with their
	unit name, label ...
	For naming here an example :
	magnitude key : Accoustic_Pressure, magnitude_name : Acoustic Pressure, unit_name : Pascal, unit_label : Pa
	Uses : Call get_unit() with needed arguments to retrieve an Unit object
	"""

	def __init__(self, client_pynvdrive: pynvdrive.Client=None):
		self._all_units = None

		self._magnitude_key_to_name_dict = None
		self._magnitude_name_to_key_dict = None

		self._simplification_dict = None

		self.client_pynvdrive = client_pynvdrive
		return

	def _init_variables(self):
		if not self._magnitude_key_to_name_dict:
			self._magnitude_key_to_name_dict = get_magnitude_dict(client=self.client_pynvdrive)
			self._magnitude_name_to_key_dict = {v: k for k, v in self._magnitude_key_to_name_dict.items()}

		if not self._all_units:
			self._all_units = get_all_units(client=self.client_pynvdrive)

		if not self._simplification_dict:
			self._simplification_dict = get_simplification_dict()

	def get_unit(self, magnitude_name=None, magnitude_key=None, unit_name=None, unit_label=None, raise_errors=True):
		"""
		Retrieve a Unit class using either :
		- magnitude_name or magnitude_key only : Assuming unit is SI
		- magnitude_name and (unit_name or unit_label)
		- magnitude_key and (unit_name or unit_label)
		magnitude_name = physical quantity = physicalQty (it's the same)
		:return: unit, or None if no found unit
		:rtype: Unit class
		"""
		self._init_variables()

		unit = Unit()

		if magnitude_name and not magnitude_key and not unit_name and not unit_label:
			# magnitude_name only : Assuming unit is SI
			unit.magnitude_name = magnitude_name
			unit.magnitude_key = self._magnitude_name_to_key_dict.get(unit.magnitude_name, None)

			if not unit.magnitude_key:
				if raise_errors:
					raise QuantityError('{} magnitude name does not exist'.format(unit.magnitude_name))
				else:
					print('{} magnitude name does not exist'.format(unit.magnitude_name))
					return None

			# Get SI unit (O index)
			unit.unit_name = list(self._all_units[unit.magnitude_name].values())[0]['unit_name']
			unit.unit_label = list(self._all_units[unit.magnitude_name].values())[0]['unit_label']
			unit.si_unit_label = list(self._all_units[unit.magnitude_name].values())[0]['si_unit_label']
			unit.coeff_A = list(self._all_units[unit.magnitude_name].values())[0]['coeff_A']
			unit.coeff_B = list(self._all_units[unit.magnitude_name].values())[0]['coeff_B']
			return unit

		elif magnitude_key and not magnitude_name and not unit_name and not unit_label:
			# magnitude_key only : Assuming unit is SI
			unit.magnitude_key = magnitude_key
			unit.magnitude_name = self._magnitude_key_to_name_dict.get(unit.magnitude_key, None)

			if not unit.magnitude_name:
				if raise_errors:
					raise QuantityError('{} magnitude key does not exist'.format(unit.magnitude_key))
				else:
					print('{} magnitude key does not exist'.format(unit.magnitude_key))
					return None

			# Get SI unit (O index)
			unit.unit_name = list(self._all_units[unit.magnitude_name].values())[0]['unit_name']
			unit.unit_label = list(self._all_units[unit.magnitude_name].values())[0]['unit_label']
			unit.si_unit_label = list(self._all_units[unit.magnitude_name].values())[0]['si_unit_label']
			unit.coeff_A = list(self._all_units[unit.magnitude_name].values())[0]['coeff_A']
			unit.coeff_B = list(self._all_units[unit.magnitude_name].values())[0]['coeff_B']
			return unit

		elif (magnitude_name or magnitude_key) and (unit_name or unit_label):
			if magnitude_name:
				# magnitude_name and (unit_name or unit_label)
				unit.magnitude_name = magnitude_name
				unit.magnitude_key = self._magnitude_name_to_key_dict.get(unit.magnitude_name, None)

				if not unit.magnitude_key:
					if raise_errors:
						raise QuantityError('{} magnitude name does not exist'.format(unit.magnitude_name))
					else:
						print('{} magnitude name does not exist'.format(unit.magnitude_name))
						return None

			if magnitude_key:
				# magnitude_key and (unit_name or unit_label)
				unit.magnitude_key = magnitude_key
				unit.magnitude_name = self._magnitude_key_to_name_dict.get(unit.magnitude_key, None)

				if not unit.magnitude_name:
					if raise_errors:
						raise QuantityError('{} magnitude key does not exist'.format(unit.magnitude_key))
					else:
						print('{} magnitude key does not exist'.format(unit.magnitude_key))
						return None

			if unit_name:
				unit.unit_name = unit_name
				# Find good one
				for key in self._all_units[unit.magnitude_name]:
					if self._all_units[unit.magnitude_name][key].get('unit_name', None) == unit.unit_name:
						unit.unit_label = self._all_units[unit.magnitude_name][key]['unit_label']
						unit.si_unit_label = self._all_units[unit.magnitude_name][key]['si_unit_label']
						unit.coeff_A = self._all_units[unit.magnitude_name][key]['coeff_A']
						unit.coeff_B = self._all_units[unit.magnitude_name][key]['coeff_B']
						return unit

				if not unit.coeff_B:
					if raise_errors:
						raise QuantityError('{} unit name does not exist'.format(unit.unit_name))
					else:
						print('{} unit name does not exist'.format(unit.unit_name))
						return None

			elif unit_label:
				unit.unit_label = unit_label
				# Find good one
				for key in self._all_units[unit.magnitude_name]:
					if self._all_units[unit.magnitude_name][key].get('unit_label', None) == unit.unit_label:
						unit.unit_name = self._all_units[unit.magnitude_name][key]['unit_name']
						unit.si_unit_label = self._all_units[unit.magnitude_name][key]['si_unit_label']
						unit.coeff_A = self._all_units[unit.magnitude_name][key]['coeff_A']
						unit.coeff_B = self._all_units[unit.magnitude_name][key]['coeff_B']
						return unit

				if not unit.coeff_B:
					if raise_errors:
						raise QuantityError('{} unit unit_label does not exist'.format(unit.unit_label))
					else:
						print('{} unit unit_label does not exist'.format(unit.unit_label))
						return None
		else:
			if raise_errors:
				raise QuantityError('Not enough information to retrieve the unit')
			else:
				print('Not enough information to retrieve the unit')
				return None

		return None

	def get_unit_si(self, magnitude_name=None, magnitude_key=None):
		"""
		Get the SI unit of a unit
		:param magnitude_name:
		:param magnitude_key:
		:return:
		"""
		self._init_variables()

		return self.get_unit(magnitude_name, magnitude_key)

	def get_unit_user(self, magnitude_name=None, magnitude_key=None, raise_errors=True):
		"""
		Get the SI unit of a unit, need only the magnitude name or key
		:param magnitude_name:
		:param magnitude_key:
		:param raise_errors: If True, raise an error if the unit is not found
		:return:
		"""
		self._init_variables()

		if not magnitude_name and not magnitude_key:
			if raise_errors:
				raise QuantityError('Not enough information to retrieve the unit, at least magnitude name or magnitude key is required')
			else:
				print('Not enough information to retrieve the unit, at least magnitude name or magnitude key is required')
				return Unit()

		if not magnitude_key:
			magnitude_key = self._magnitude_name_to_key_dict.get(magnitude_name, None)

		# Retrieve user unit name
		try:
			if not self.client_pynvdrive:
				self.client_pynvdrive = Client()
			self.client_pynvdrive.connect()
		except Exception:
			if raise_errors:
				raise QuantityError('Could not connect to NVDrive')
			else:
				print('Could not connect to NVDrive')
				return Unit()
		else:
			try:
				cmd = GetMagnitudeInfo(magnitude_key=magnitude_key)
				self.client_pynvdrive.send_command(cmd)
				magnitude_name = cmd.magnitude_name
				unit_name = cmd.unit_name
				unit = self.get_unit(magnitude_name=magnitude_name, unit_name=unit_name, raise_errors=raise_errors)
				if not unit:
					unit = Unit()
			except NVDriveCommandError as e:
				if magnitude_key != 'Unknown Magnitude' and magnitude_key != 'None':
					print('error GetMagnitudeInfo {}'.format(magnitude_key), e.error)
				return Unit()

		return unit

	def get_unit_input_name(self, input_name, client=None):
		"""
		Retrieve unit for input_name
		:return: unit
		"""
		try:
			if client is None:
				if not self.client_pynvdrive:
					self.client_pynvdrive = Client()
				self.client_pynvdrive.connect()
			else:
				self.client_pynvdrive = client
				self.client_pynvdrive.connect()

			# Retrieve magnitude_key from frontend settings
			# TODO : Could be an issue if multiple frontend input have same input_name
			input_magnitude_dict = get_magnitude_key_all_inputs(client=client)
			magnitude_key = input_magnitude_dict.get(input_name, None)
			unit = self.get_unit_user(magnitude_key=magnitude_key)
		except Exception:
			raise QuantityError('Could not connect to NVDrive')
			unit = Unit()
		finally:
			return unit

	def get_unit_from_module_channel(self, module_id: int, channel_number: int, process_id: int = None, client=None):
		"""
		Retrieve unit from a module and its channel number
		:return unit
		"""
		try:
			if client is None:
				if not self.client_pynvdrive:
					self.client_pynvdrive = Client()
				self.client_pynvdrive.connect()
			else:
				self.client_pynvdrive = client
				self.client_pynvdrive.connect()

			input_nb, input_label, input_idn = get_source_name(module=module_id, channel=channel_number, process=process_id)
			magnitude_key = get_magnitude_key_from_input_idn(input_idn=input_idn, client=self.client_pynvdrive)

			if not magnitude_key:
				magnitude_key = get_magnitude_key_from_input_number(input_nb=input_nb, client=self.client_pynvdrive)
			if not magnitude_key:
				magnitude_key = get_magnitude_key_from_input_name(input_name=input_label, client=self.client_pynvdrive)

			unit = self.get_unit_user(magnitude_key=magnitude_key)
		except Exception:
			print('Unit not found for module {} and channel {}'.format(module_id, channel_number))
			unit = Unit()

		# Apply filter to this unit
		try:
			# Get filter applied to the input
			integrator_level_input, differentiator_level_input = self.get_filter_input(input_idn=input_idn, client=self.client_pynvdrive)
			integrator_level_module_channel, differentiator_level_module_channel = self.get_filter_module_channel(module_id=module_id, channel_number=channel_number, client=client)
			integrator_level = integrator_level_input + integrator_level_module_channel
			differentiator_level = differentiator_level_input + differentiator_level_module_channel
		except Exception:
			# print('Could not retrieve filter for module {} and channel {}'.format(module_id, channel_number))
			integrator_level = 0
			differentiator_level = 0
		finally:
			unit = self.get_filtered_unit(unit, integrator_level=integrator_level, differentiator_level=differentiator_level)

		# Get filter apply to this channel_number (frontend + module)
		return unit

	def get_filter_input(self, input_idn, client=None):
		"""
		Retrieve filter applied to an input
		:return: integrator_level, differentiator_level
		"""
		if client is None:
			if not self.client_pynvdrive:
				self.client_pynvdrive = Client()
			self.client_pynvdrive.connect()
		else:
			self.client_pynvdrive = client
			self.client_pynvdrive.connect()

		module = input_idn.split('.')[0]
		submodule = input_idn.split('.')[1]
		try:
			idn = '{}.{}.046'.format(module, submodule)
			cmd = GetSettingValue(idn=idn)
			self.client_pynvdrive.send_command(cmd)
			idn_filter = cmd.value
			if idn_filter == 'none':
				return 0, 0
			else:
				module = idn_filter.split('.')[0]
				submodule = idn_filter.split('.')[1]
				if submodule in ('284', '285', '286'):  # Integrator
					idn = '{}.{}.062'.format(module, submodule)
					cmd = GetSettingValue(idn=idn)
					self.client_pynvdrive.send_command(cmd)
					value = int(cmd.value)
					return value, 0
				elif submodule in ('095', '096', '097'):  # Differentiator
					return 0, 1
				else:
					return 0, 0
		except pynvdrive.NVDriveCommandError as e:
			pass
		except pynvdrive.NVDriveConnectionError:
			print('error NVDrive is not connected (get_filter_input)')
		except Exception:
			pass

	def get_filter_module_channel(self, module_id: int, channel_number: int, client=None):
		"""
		Retrieve filter applied to an channel number
		:return: integrator_level, differentiator_level
		"""
		if client is None:
			if not self.client_pynvdrive:
				self.client_pynvdrive = Client()
			self.client_pynvdrive.connect()
		else:
			self.client_pynvdrive = client
			self.client_pynvdrive.connect()

		if isinstance(module_id, int):  # Convert old idn to new
			module = nvg_modules[module_id]
		elif module_id.isnumeric():
			module = nvg_modules[int(module_id)]

		try:
			idn = '{}.channel{}.inputFilter'.format(module, channel_number)
			cmd = GetSettingValue(idn=idn)
			self.client_pynvdrive.send_command(cmd)
			idn_filter = cmd.value
			if idn_filter == 'none':
				return 0, 0
			else:
				module = idn_filter.split('.')[0]
				submodule = idn_filter.split('.')[1]
				if submodule in ('284', '285', '286'):  # Integrator
					idn = '{}.{}.062'.format(module, submodule)
					cmd = GetSettingValue(idn=idn)
					self.client_pynvdrive.send_command(cmd)
					value = int(cmd.value)
					return value, 0
				elif submodule in ('095', '096', '097'):  # Differentiator
					return 0, 1
				else:
					return 0, 0
		except NVDriveCommandError as e:
			print('error get_filter_module_channel:GetSettingValue idn filter', e)

	def get_unit_from_result_ex(self, result_format_and_description, client=None):
		"""
		Retrieve unit from a nvdrive Result containing the HEAD block
		Need the results to be already computed by NVGate, otherwise the HEAD block is not present (nor all the other blocks)
		:return unit
		"""
		from pynvdrive.toolbox.get_result_ex import get_result_ex
		from pynvdrive.toolbox.create_result_ex import create_result_ex
		try:
			if client is None:
				if not self.client_pynvdrive:
					self.client_pynvdrive = Client()
				self.client_pynvdrive.connect()
			else:
				self.client_pynvdrive = client
				self.client_pynvdrive.connect()

			create_result_ex(result_format_and_description=result_format_and_description,
			              client=self.client_pynvdrive)

			result, _ = get_result_ex(result_format_and_description=result_format_and_description,
			              client=self.client_pynvdrive)

			if not result:
				return None

			magnitude_key = result.head.magnitude_key
			unit = self.get_unit_user(magnitude_key=magnitude_key)

			if unit.magnitude_name is None:
				# Unit unknown, create a unit with info from the result
				unit.magnitude_name = result.head.physical_quantity
				unit.magnitude_key = result.head.magnitude_key
				unit.unit_name = result.head.unit_name
				unit.unit_label = result.head.unit_label
				unit.coeff_A = 1.0
				unit.coeff_B = 0.0

			return unit
		except Exception:
			# print('Unit not found for result_ex {}'.format(result_format_and_description.to_dict()))
			return Unit()

	def get_filtered_unit(self, unit: Unit, integrator_level: int, differentiator_level: int):
		"""
		Get the unit passed through a filter
		:param unit: original unit
		:param integrator_level: integrator level
		:param differentiator_level: differentiator level
		:return: filtered unit
		"""
		# print('Integrator level : {}, Differentiator level: {}'.format(integrator_level, differentiator_level))
		diff = integrator_level - differentiator_level
		if diff == 0:  # No filter
			return unit
		# Step 1 : Get the closest unit in the database using self._simplification_dict
		unit, _, found_at = self._get_closest_existing_unit(unit=unit, exposant=diff)
		exposant_remaining = diff - found_at
		# Step 2 : Apply the filter
		unit = self._apply_filter(unit=unit, exposant=exposant_remaining)
		# print('Filtered unit: {}'.format(unit.to_dict()))
		return unit

	def _get_closest_existing_unit(self, unit:Unit, exposant: int, found_at=0):
		"""
		Get the closest unit in the database using self._simplification_dict
		:param unit: original unit
		:param exposant: exposant of the filter
		:return: closest unit, exposant still to apply
		"""
		if found_at or exposant == 0:
			return unit, exposant, found_at
		original_magnitude_key = unit.magnitude_key

		str_to_find = '{}:1|Time:{}'.format(original_magnitude_key, exposant)
		# print('Looking for {}'.format(str_to_find))
		if str_to_find in self._simplification_dict:
			new_magnitude_key = self._simplification_dict[str_to_find]
			new_unit = self.get_unit_user(magnitude_key=new_magnitude_key)
			return new_unit, 0, exposant
		else:
			if exposant > 0:
				exposant -= 1
				new_unit, exposant_restant, found_at = self._get_closest_existing_unit(unit=unit, exposant=exposant)
				if (new_unit.to_dict() != unit.to_dict()) and found_at==0:
					found_at = exposant
			else:
				exposant += 1
				new_unit, exposant_restant, found_at = self._get_closest_existing_unit(unit=unit, exposant=exposant)
				if (new_unit.to_dict() != unit.to_dict()) and found_at==0:
					found_at = exposant

		return new_unit, exposant, found_at

	def _apply_filter(self, unit, exposant):
		"""
		Apply integrator/differentiator filter to magnitude_name, name, label etc...
		:param unit: unit to filter
		:param exposant: exposant of the filter
		:return: filtered unit
		"""
		if exposant == 0:
			return unit

		compared_magnitude_name = 'Time'
		compared_unit_name = 'Second'
		compared_unit_label = 's'

		new_magnitude_key = 'Unknown Magnitude'
		new_si_unit_label = None
		new_coeff_A = 1.0
		new_coeff_B = 0.0

		if exposant == -4:
			new_magnitude_name = '({})/(({})²)/(({})²)'.format(unit.magnitude_name, compared_magnitude_name, compared_magnitude_name)
			new_unit_name = '({})/(({})²)/(({})²)'.format(unit.unit_name, compared_unit_name, compared_unit_name)
			new_unit_label = '({})/(({})²)/(({})²)'.format(unit.unit_label, compared_unit_label, compared_unit_label)
		elif exposant == -3:
			new_magnitude_name = '({})/(({})²)/({})'.format(unit.magnitude_name, compared_magnitude_name, compared_magnitude_name)
			new_unit_name = '({})/(({})²)/({})'.format(unit.unit_name, compared_unit_name, compared_unit_name)
			new_unit_label = '({})/(({})²)/({})'.format(unit.unit_label, compared_unit_label, compared_unit_label)
		if exposant == -2:
			new_magnitude_name = '({})/(({})²)'.format(unit.magnitude_name, compared_magnitude_name)
			new_unit_name = '({})/(({})²)'.format(unit.unit_name, compared_unit_name)
			new_unit_label = '({})/(({})²)'.format(unit.unit_label, compared_unit_label)
		elif exposant == -1:
			new_magnitude_name = '({})/({})'.format(unit.magnitude_name, compared_magnitude_name)
			new_unit_name = '({})/({})'.format(unit.unit_name, compared_unit_name)
			new_unit_label = '({})/({})'.format(unit.unit_label, compared_unit_label)
		elif exposant == 1:
			new_magnitude_name = '({}).({})'.format(unit.magnitude_name, compared_magnitude_name)
			new_unit_name = '({}).({})'.format(unit.unit_name, compared_unit_name)
			new_unit_label = '({}).({})'.format(unit.unit_label, compared_unit_label)
		elif exposant == 2:
			new_magnitude_name = '({}).(({})²)'.format(unit.magnitude_name, compared_magnitude_name)
			new_unit_name = '({}).(({})²)'.format(unit.unit_name, compared_unit_name)
			new_unit_label = '({}).(({})²)'.format(unit.unit_label, compared_unit_label)
		elif exposant == 3:
			new_magnitude_name = '({}).(({})²).({})'.format(unit.magnitude_name, compared_magnitude_name, compared_magnitude_name)
			new_unit_name = '({}).(({})²).({})'.format(unit.unit_name, compared_unit_name, compared_unit_name)
			new_unit_label = '({}).(({})²).({})'.format(unit.unit_label, compared_unit_label, compared_unit_label)
		elif exposant == 4:
			new_magnitude_name = '({}).(({})²).(({})²)'.format(unit.magnitude_name, compared_magnitude_name, compared_magnitude_name)
			new_unit_name = '({}).(({})²).(({})²)'.format(unit.unit_name, compared_unit_name, compared_unit_name)
			new_unit_label = '({}).(({})²).(({})²)'.format(unit.unit_label, compared_unit_label, compared_unit_label)
		else:
			raise QuantityError('Exposant not supported')

		return Unit(magnitude_name=new_magnitude_name, unit_name=new_unit_name, unit_label=new_unit_label, si_unit_label=new_si_unit_label, coeff_A=new_coeff_A, coeff_B=new_coeff_B)
