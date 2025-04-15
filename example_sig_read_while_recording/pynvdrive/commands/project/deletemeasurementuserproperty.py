from ... import Command


class DeleteMeasurementUserProperty(Command):
    def __init__(self, project_name, measurement_name, property_identifier):
        super().__init__(name=None, parameters=[project_name, measurement_name, property_identifier])
        self.value = None
        return

    def parse_response(self, response):
        pass
