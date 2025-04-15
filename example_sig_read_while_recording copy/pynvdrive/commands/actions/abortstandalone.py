from ... import Command


class AbortStandAlone(Command):
	def __init__(self, project_name):
		super().__init__(name=None, parameters=[project_name])
		self.value = None
		return

	def parse_response(self, response):
		return
