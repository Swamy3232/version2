from ... import Command


class IsSignalFileCompatible(Command):
	def __init__(self, project_name, measurement_name):
		super().__init__(name=None, parameters=[str(project_name), str(measurement_name)])
		self.value = None
		return

	def parse_response(self, response):
		print(response)
