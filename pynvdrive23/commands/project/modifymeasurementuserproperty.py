from ... import Command


class ModifyMeasurementUserProperty(Command):
    def __init__(self, project_name, measurement_name, property_identifier, property_value):
        super().__init__(name=None, parameters=[project_name, measurement_name, property_identifier, property_value])
        self.value = None
        return

    def parse_response(self, response):
        pass
