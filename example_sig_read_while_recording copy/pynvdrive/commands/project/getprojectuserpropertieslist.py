from ... import Command
from ...formats.user_property_info import UserPropertyInfo


class GetProjectUserPropertiesList(Command):
    def __init__(self, project_name):
        super().__init__(name=None, parameters=[project_name])
        self.value = []
        self.list_user_property_info = []
        return

    def parse_response(self, response):
        try:
            _, _ = response.split(b'\0', 1)
        except Exception:
            return None

        self.list_user_property_info = self.parse_response_list_user_property_info(response)

        for user_property in self.list_user_property_info:
            self.value.append([user_property.id, user_property.title, user_property.type, user_property.value])

    def parse_response_list_user_property_info(self, contents):
        contents = self.parse_response_list_string(contents)

        if len(contents) % 4 != 0:
            # Issue because supposed to be 4 values par property
            return None

        list_user_property_info = []
        for i in range(0, len(contents), 4):
            current_user_property = UserPropertyInfo()
            current_user_property.id = contents[i]
            current_user_property.title = contents[i + 1]
            current_user_property.type = contents[i + 2]
            current_user_property.value = contents[i + 3]
            list_user_property_info.append(current_user_property)

        return list_user_property_info
