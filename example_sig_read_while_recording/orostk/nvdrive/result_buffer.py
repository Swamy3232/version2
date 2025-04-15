import logging


nvdrive_logger = logging.getLogger('NVDriveLogger')


class ResultBuffer(object):
    """
    This class creates a buffer from a result.
    This buffer will be sent to NVGate
    """

    def __init__(self, result=None):
        """

        :param result:
        :type result: Result
        :return:
        """
        self.result = None
        self.fields = None
        self.byte_size = None
        if result:
            self.affect(result)
        else:
            self.clear()

    def affect(self, result):
        """ Clear the buffer and affect a new
        result to it.

        :param result:
        :type result: Result
        :return:
        """
        self.result = result
        self.fields = self.result.serialize_fields()
        self.byte_size = self.result.total_size

    def clear(self):
        """ Clear the buffer

        :return:
        """
        self.byte_size = 0
        self.fields = []
        self.result = None

    @property
    def blocks_fields(self):
        """
        :return: Fields of the buffer without the result informations
        """
        return self.fields[len(self.result.serialized_result_info):]

    @property
    def blocks_size(self):
        return self.byte_size - self.result.res_size
