import logging

from orostk.idn import Idn
from orostk.nvdrive.generic_command import GenericCommand
from orostk.nvdrive.nvd_commands import (
    get_setting_value, get_setting_possible_values)


nvdrive_logger = logging.getLogger('NVDriveLogger')

SETTING_TYPE = {
    0: 'boolean',
    1: 'string',
    2: 'float',
    3: 'enumerate',
    4: 'signal file'
}


class GetSettingValue(GenericCommand):
    """
    This class simulates:
        - GetSettingValue

    This class helps to retrieve the value of a setting
    """
    def __init__(self, module, submodule, setting, option=0):
        """

        :param module:
        :type module: str
        :param submodule:
        :type submodule: str
        :param setting:
        :type setting: str
        :param option:
        :type option: int
        """
        super().__init__()
        self.idn = Idn(module, submodule, setting)
        self.option = option
        self.setting_value = None
        self.setting_type = None
        print(self.idn)

    def run(self, socket):
        nvdrive_logger.info('Running command GetSettingValue')
        self.setting_value, s_type = get_setting_value(socket,
                                                       (self.idn),
                                                       self.option)
        self.setting_type = SETTING_TYPE[s_type]
        nvdrive_logger.info('Command succeed')
        print(self.idn)
        return True


class GetSettingPossibleValues(GenericCommand):
    """
    This class simulates:
        - GetSettingValues

    This class helps to retrieve the possible values of a setting.
    The type of the setting should be enumerate.
    """

    def __init__(self, module, submodule, setting):
        """

        :param module:
        :type module: str
        :param submodule:
        :type submodule: str
        :param setting:
        :type setting: str
        """
        super().__init__()
        self.idn = Idn(module, submodule, setting)
        self.possible_values = None

    def run(self, socket):
        nvdrive_logger.info('Running command GetSettingPossibleValues')
        self.possible_values = get_setting_possible_values(socket,
                                                           str(self.idn))
        nvdrive_logger.info('Command succeed')
        return True
