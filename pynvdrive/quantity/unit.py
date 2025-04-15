class Unit(object):
	"""
	This class represent a NVGate unit
	"""
	ROUND_COEFF = 5

	def __init__(self, magnitude_name=None, magnitude_key=None, unit_name=None, unit_label=None, si_unit_label=None,
	             coeff_A=None, coeff_B=None):
		self.magnitude_name = magnitude_name  # magnitude_name and physical_quantity is same thing
		self.magnitude_key = magnitude_key
		self.unit_name = unit_name
		self.unit_label = unit_label
		self.si_unit_label = si_unit_label
		self.coeff_A = coeff_A
		self.coeff_B = coeff_B

	def is_filled(self):
		"""
		Return True if the unit is empty/not filled
		"""
		if self.unit_label is None or self.magnitude_name is None or self.coeff_A is None or self.coeff_B is None:
			return False
		else:
			return True

	def to_dict(self):
		"""
		Return a dictionary representation of the unit
		"""
		return {
			'magnitude_name': self.magnitude_name,
			'magnitude_key': self.magnitude_key,
			'unit_name': self.unit_name,
			'unit_label': self.unit_label,
			'si_unit_label': self.si_unit_label,
			'coeff_A': self.coeff_A,
			'coeff_B': self.coeff_B
		}

	@classmethod
	def from_dict(cls, data):
		"""
		Create a Unit object from a dictionary
		"""
		return cls(magnitude_name=data.get('magnitude_name', None), magnitude_key=data.get('magnitude_key', None),
		           unit_name=data.get('unit_name', None), unit_label=data.get('unit_label', None),
		           si_unit_label=data.get('si_unit_label', None), coeff_A=data.get('coeff_A', None),
		           coeff_B=data.get('coeff_B', None))

	def get_si_value_from_user_value(self, user_value):
		"""
		Convert a user value to SI value
		"""
		# print("get_si_value_from_user_value : ", user_value)
		if (self.coeff_A is not None) and (self.coeff_B is not None):
			if isinstance(user_value, list):
				return [(user_value[i] - self.coeff_B) / round(self.coeff_A, self.ROUND_COEFF) for i in range(len(user_value))]
			else:
				return (user_value - self.coeff_B) / round(self.coeff_A, self.ROUND_COEFF)
		else:
			return user_value

	def get_user_value_from_si_value(self, si_value):
		"""
		Convert a SI value to user value
		"""
		# print("get_user_value_from_si_value : ", si_value)
		if (self.coeff_A is not None) and (self.coeff_B is not None):
			if isinstance(si_value, list):
				return [si_value[i] * round(self.coeff_A, self.ROUND_COEFF) + self.coeff_B for i in range(len(si_value))]
			else:
				return si_value * round(self.coeff_A, self.ROUND_COEFF) + self.coeff_B
		else:
			return si_value


if __name__ == '__main__':
	unit = Unit(magnitude_name='Acceleration', magnitude_key='Acceleration', unit_name='Gravity', unit_label='g',
	            si_unit_label='Meter /second²', coeff_A=0.10193680226802826, coeff_B=0.0)
	values = [3000, 300, 30, 3, 0.3, 0.03, 0.003, 0.0003, 0.00003, 0.000003, 0.0000003, 0.00000003, 0.000000003, 0.0000000003, 0.00000000003]
	for v in values:
		si_value = unit.get_si_value_from_user_value(v)
		back_value = unit.get_user_value_from_si_value(si_value)
		print('Original : {}, SI : {}, Back : {}'.format(v, si_value, back_value))