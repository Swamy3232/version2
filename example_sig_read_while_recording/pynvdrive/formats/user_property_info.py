class UserPropertyInfo:
	"""
    Result format and description as described in NVDrive documentation

    """

	def __init__(self):
		self._id = None
		self._title = None
		self._type = None
		self._value = None

		return

	@property
	def id(self):
		return self._id

	@property
	def title(self):
		return self._title

	@property
	def type(self):
		return self._type

	@property
	def value(self):
		return self._value

	@id.setter
	def id(self, value):
		self._id = value

	@title.setter
	def title(self, value):
		self._title = value

	@type.setter
	def type(self, value):
		self._type = value

	@value.setter
	def value(self, value):
		self._value = value
