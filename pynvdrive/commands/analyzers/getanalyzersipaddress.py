from ... import Command


class GetAnalyzersIpAddress(Command):
    """
    Return the IP address of the analyzer.
    :return: The IP address of the analyzer. list of strings
    """
    def __init__(self):
        super().__init__(name=None, parameters=[])
        self.value = None
        self.analyzers_ip_address = None
        return

    def parse_response(self, response):
        try:
            self.analyzers_ip_address = self.parse_response_list_string(response)
            self.value = self.analyzers_ip_address
        except (Exception,):
            pass
