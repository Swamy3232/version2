from ... import Command


class AddMeasurementUserProperty(Command):
    def __init__(self, project_name, measurement_name, property_title, property_value):
        super().__init__(name=None, parameters=[project_name, measurement_name, property_title, property_value])
        self.value = None
        return

    def parse_response(self, response):
        pass
