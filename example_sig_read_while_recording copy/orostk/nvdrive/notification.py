from orostk.idn import Idn
from orostk.nvdrive.notification_utils import command_id


class Notification(object):
    """
    Represents a NVGate notification,
    a Notification reader can subscribe to a notification.
    """
    def __init__(self):
        self.head_block = None
        self.data_block = None

    @property
    def identifier(self):
        raise NotImplementedError('A notification needs'
                                  ' a way to be identified')

    def __eq__(self, other):
        return type(self) == type(other) and \
               self.identifier == other.identifier


class SettingNotification(Notification):
    """
    Represents a NVGate setting notification.

    Example::

        notification = SettingNotification(module='fft1')

    """
    def __init__(self, module, submodule=None, setting=None):
        """ IDN is a next generation IDN

        :param module: module identifier
        :param submodule: submodule identifier
        :param setting: setting identifier
        """
        super().__init__()
        self.idn = Idn(module=module,
                       submodule=submodule,
                       setting=setting)
        self.module = self.idn.module
        self.submodule = self.idn.submodule
        self.setting = self.idn.setting

    @property
    def identifier(self):
        identifier = ''
        identifier += self.module
        if self.submodule:
            identifier += '.'
            identifier += self.submodule
            if self.setting:
                identifier += '.'
                identifier += self.setting
        return identifier

    @property
    def module_id(self):
        return self.idn.module_id

    @property
    def submodule_id(self):
        return self.idn.submodule_id

    @property
    def setting_id(self):
        return self.idn.setting_id


class StateNotification(Notification):
    """
    Represents a NVGate state notification.

    Example::

        notification = StateNotification(module='fft1')

    """
    def __init__(self, module=None, submodule=None, setting=None):
        """ IDN is a next generation IDN

        :param module: module identifier
        :param submodule: submodule identifier
        :param setting: setting identifier
        """
        super().__init__()
        self.idn = Idn(module=module,
                       submodule=submodule,
                       setting=setting)
        self.module = self.idn.module
        self.submodule = self.idn.submodule
        self.setting = self.idn.setting

    @property
    def identifier(self):
        if self.module is None:
            return 'all'
        identifier = ''
        identifier += self.module
        if self.submodule:
            identifier += '.'
            identifier += self.submodule
            if self.setting:
                identifier += '.'
                identifier += self.setting
        return identifier

    @property
    def module_id(self):
        return self.idn.module_id

    @property
    def submodule_id(self):
        return self.idn.submodule_id

    @property
    def setting_id(self):
        return self.idn.setting_id


class CommandNotification(Notification):
    """
    Represents a NVGate command notification.
    Possible commands:

        - run
        - pause
        - stop
        - accept
        - reject
        - manual_trigger
        - player_pause

    Example::

        notification = CommandNotification(command='run')

    """
    def __init__(self, command):
        super().__init__()
        self.command = command

    @property
    def identifier(self):
        return self.command

    @property
    def command_id(self):
        return command_id[self.command]


class UINotification(Notification):
    """
    Represents a NVGate UI notification.

    Example::

        notification = UINotification(ui_event_id=3)

    """

    def __init__(self, ui_event_id):
        super().__init__()
        self.ui_event_id = ui_event_id

    @property
    def identifier(self):
        return self.ui_event_id


class ResultNotification(Notification):
    """
    Represents a NVGate new result notification.

    Example::

        notification = ResultNotification(module='soa1')

    """

    def __init__(self, module):
        """

        :param module: Module IDN next generation
        """
        super().__init__()
        self.module = module
        self.idn = Idn(module=module)

    @property
    def identifier(self):
        return self.module

    @property
    def module_id(self):
        return self.idn.module_id


class MeasurementNotification(Notification):
    """
    Represents a NVGate new measurement notification.

    Example::

        notification = MeasurementNotification()

    """

    def __init__(self):
        super().__init__()

    @property
    def identifier(self):
        return self.__class__.__name__
