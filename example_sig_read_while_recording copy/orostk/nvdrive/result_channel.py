from orostk.nvdrive.commands import (
    CreateResultEx, DeleteResultEx, GetResult, GetSavedResult)


class ResultChannel(object):
    """
    This class represents a result channel,
    used to extract results from a measurement.

    Example::

        client = NVDClient()
        client.connect()
        with ResultChannel(nvd_client=client, module='fft1',
                           process_id=2, channel=1) as rc:
            res = rc.get_result()

    """
    def __init__(self, nvd_client, module, process_id, channel,
                 reference_channel=None, waterfall=False,
                 project_name=None, measurement_name=None):
        """

        :param nvd_client:
        :param module:
        :type module: str
        :param process_id:
        :type process_id: int
        :param channel:
        :param reference_channel:
        :param waterfall: True or False
        :param project_name:
        :param measurement_name:
        """
        self.client = nvd_client
        self.module = module
        self.process_id = process_id
        self.channel = channel
        self.reference_channel = reference_channel if reference_channel else 0
        self.waterfall_flag = 1 if waterfall else 0
        self.project_name = project_name
        self.measurement_name = measurement_name

    def __enter__(self):
        self.create()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.delete()

    def create(self):
        cmd_create = CreateResultEx(self.module, self.process_id,
                                    self.channel, self.reference_channel,
                                    self.waterfall_flag)
        self.client.run(cmd_create)

    def delete(self):
        cmd_delete = DeleteResultEx(self.module, self.process_id,
                                    self.channel, self.reference_channel,
                                    self.waterfall_flag)
        self.client.run(cmd_delete)

    def get_result(self):
        """

        :return: A result from the opened channel
        """
        if self.project_name and self.measurement_name:
            cmd_get = GetSavedResult(self.project_name, self.measurement_name,
                                     self.module, self.project_name,
                                     self.channel, self.reference_channel,
                                     self.waterfall_flag)
        else:
            cmd_get = GetResult(self.module, self.process_id, self.channel,
                                self.reference_channel, self.waterfall_flag)

        self.client.run(cmd_get)
        return cmd_get.result
