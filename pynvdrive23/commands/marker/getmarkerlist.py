from ... import Command
from ...formats.marker_description import MarkerDescription


class GetMarkerList(Command):
	def __init__(self, window_name, display_zone_type=''):
		super().__init__(name=None, parameters=[window_name, str(display_zone_type)])
		self.window_name = window_name
		self.display_zone_type = display_zone_type

		self.value = []
		self.list_marker_description = []
		return

	def parse_response(self, response):
		if not response:
			return None

		try:
			_, _ = response.split(b'\0', 1)
		except Exception:
			raise NotImplementedError('Error using GetMarkerList')

		self.list_marker_description = self.parse_response_marker_description_list(response)
		self.value = self.list_marker_description

	def parse_response_marker_description_list(self, contents):
		list_marker_description = []
		contents_splitted = contents.split(b'-')

		# Fix issue if "-" in the input name (e.g. "Input-1"), because it's used as a separator for this command
		new_contents_splitted = []
		for content in contents_splitted:
			test_pre_parse = self.pre_parse_response_marker_description(content)
			# If result False, then we need to concatenate the previous content with the current content
			if test_pre_parse:
				new_contents_splitted.append(content)
			else:
				new_contents_splitted[-1] = b'-'.join([new_contents_splitted[-1], content])

		for content in new_contents_splitted:
			current = self.parse_response_marker_description(content)
			current.window_name = self.window_name
			current.display_zone_type = self.display_zone_type
			list_marker_description.append(current)

		return list_marker_description

	@staticmethod
	def parse_response_marker_description(contents):
		marker_description = MarkerDescription.from_bytes(contents)
		return marker_description

	@staticmethod
	def pre_parse_response_marker_description(contents):
		"""
		Pre-parse the response to get the list of result format and description and check if error
		"""
		try:
			test = MarkerDescription.from_bytes(contents)
			if test.location is not None:
				return True
			else:
				return False
		except Exception:
			return False
		return True
