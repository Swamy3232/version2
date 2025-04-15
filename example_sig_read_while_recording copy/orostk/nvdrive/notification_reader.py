import logging

from orostk.utils.orostk_utils import methdispatch
from orostk.nvdrive.notification import (
    ResultNotification, SettingNotification, StateNotification,
    MeasurementNotification, CommandNotification, UINotification
)
from orostk.nvdrive.notification_handler import NotificationHandler
from orostk.nvdrive.nvdrive_exceptions import (
    NotificationTypeException, NotificationException
)
from orostk.nvdrive.action_commands import (
    RegisterCommand, RegisterNewMeasurement, RegisterNewResult,
    RegisterSetting, RegisterState, RegisterUINotification
)
from orostk.nvdrive.action_commands import (
    UnregisterCommand, UnregisterNewMeasurement, UnregisterNewResult,
    UnregisterSetting, UnregisterState, UnregisterUINotification
)
from orostk.nvdrive.action_commands import (
    ConnectToTCPClient, DisconnectFromTCPClient
)
from orostk.nvdrive.notification_block import HeadBlock, id_to_block

from orostk.nvdrive.notification_block import (
    StateDataBlock, SettingDataBlock, CommandDataBlock,
    ResultDataBlock, MeasurementDataBlock, UIDataBlock
)
from orostk.nvdrive.setting_commands import GetSettingValue


nvdrive_logger = logging.getLogger('NVDriveLogger')


class NotificationReader(object):
    """
    This class can be used to handle NVGate notifications.
    You have to create a child class of this one if you want
    your reader to have a specific behaviour when receiving notification.

    Example::

        with NotificationReader(nvd_client=my_client)as reader:
            reader.subscribe(my_notification)
            reader.handle_notification()

    """

    def __init__(self, nvd_client, address='127.0.0.1', port=9000):
        self.nvd_client = nvd_client
        self.handler = NotificationHandler(address, port)
        self.setting_notifications = {}
        self.state_notifications = {}
        self.command_notifications = {}
        self.ui_notifications = {}
        self.result_notifications = {}
        self.measurement_notifications = {}
        self.connected = False

    def __enter__(self):
        self.nvd_client.run(ConnectToTCPClient(
            self.handler.ip_address,
            self.handler.port)
        )
        self.handler.accept_connection(timeout=5)
        self.connected = True
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.nvd_client.run(DisconnectFromTCPClient())
        self.handler.disconnect()
        self.connected = False

    @methdispatch
    def subscribe(self, notification):
        """ Subscribe the reader to a notification

        :param notification:
        :return:
        """
        raise NotificationTypeException('Unknown notification type')

    @subscribe.register(ResultNotification)
    def _(self, notification):
        nvdrive_logger.info('Subscribing to a new result notification')
        if notification.identifier in self.result_notifications:
            raise NotificationException('Already subscribed'
                                        ' to the notification')
        self.nvd_client.run(RegisterNewResult(notification.module_id))
        self.result_notifications[notification.identifier] = notification

    @subscribe.register(SettingNotification)
    def _(self, notification):
        nvdrive_logger.info('Subscribing to a setting notification')
        if notification.identifier in self.setting_notifications:
            raise NotificationException('Already subscribed'
                                        ' to the notification')
        self.nvd_client.run(RegisterSetting(
            notification.module,
            notification.submodule,
            notification.setting
        ))
        self.setting_notifications[notification.identifier] = notification

    @subscribe.register(StateNotification)
    def _(self, notification):
        nvdrive_logger.info('Subscribing to a state notification')
        if notification.identifier in self.state_notifications:
            raise NotificationException('Already subscribed'
                                        ' to the notification')
        self.state_notifications[notification.identifier] = notification
        self.nvd_client.run(RegisterState(
            notification.module_id if notification.module != '' else -1,
            notification.submodule_id if notification.submodule != '' else -1,
            notification.setting_id if notification.setting != '' else -1
        ))

    @subscribe.register(MeasurementNotification)
    def _(self, notification):
        nvdrive_logger.info('Subscribing to a new measurement notification')
        if notification.identifier in self.measurement_notifications:
            raise NotificationException('Already subscribed'
                                        ' to the notification')
        self.measurement_notifications[notification.identifier] = notification
        self.nvd_client.run(RegisterNewMeasurement())

    @subscribe.register(CommandNotification)
    def _(self, notification):
        nvdrive_logger.info('Subscribing to a command notification')
        if notification.identifier in self.command_notifications:
            raise NotificationException('Already subscribed'
                                        ' to the notification')
        self.command_notifications[notification.identifier] = notification
        self.nvd_client.run(RegisterCommand(notification.command_id))

    @subscribe.register(UINotification)
    def _(self, notification):
        nvdrive_logger.info('Subscribing to a UI notification')
        if notification.identifier in self.ui_notifications:
            raise NotificationException('Already subscribed'
                                        ' to the notification')
        self.ui_notifications[notification.identifier] = notification
        self.nvd_client.run(RegisterUINotification(notification.ui_event_id))

    @methdispatch
    def unsubscribe(self, notification):
        """ Unsubscribe the reader from a notification

        :param notification:
        :return:
        """
        raise NotificationTypeException('Unknown notification type')

    @unsubscribe.register(ResultNotification)
    def _(self, notification):
        nvdrive_logger.info('Unsubscribing from a new result notification')
        if notification.identifier not in self.result_notifications:
            raise NotificationException('Not subscribed to the notification')
        self.nvd_client.run(UnregisterNewResult(notification.module))
        self.result_notifications.pop(notification.identifier)

    @unsubscribe.register(SettingNotification)
    def _(self, notification):
        nvdrive_logger.info('Unsubscribing from a setting notification')
        if notification.identifier not in self.setting_notifications:
            raise NotificationException('Not subscribed to the notification')
        self.nvd_client.run(UnregisterSetting(
            notification.module,
            notification.submodule,
            notification.setting)
        )
        self.setting_notifications.pop(notification.identifier)

    @unsubscribe.register(StateNotification)
    def _(self, notification):
        nvdrive_logger.info('Unsubscribing from a state notification')
        if notification.identifier not in self.state_notifications:
            raise NotificationException('Not subscribed to the notification')
        self.nvd_client.run(UnregisterState(
            notification.module,
            notification.submodule,
            notification.setting)
        )
        self.state_notifications.pop(notification.identifier)

    @unsubscribe.register(MeasurementNotification)
    def _(self, notification):
        nvdrive_logger.info('Unsubscribing from a'
                            ' new measurement notification')
        if notification.identifier not in self.measurement_notifications:
            raise NotificationException('Not subscribed to the notification')
        self.nvd_client.run(UnregisterNewMeasurement())
        self.measurement_notifications.pop(notification.identifier)

    @unsubscribe.register(CommandNotification)
    def _(self, notification):
        nvdrive_logger.info('Unsubscribing from a command notification')
        if notification.identifier not in self.command_notifications:
            raise NotificationException('Not subscribed to the notification')
        self.nvd_client.run(UnregisterCommand(notification.command_id))
        self.command_notifications.pop(notification.identifier)

    @unsubscribe.register(UINotification)
    def _(self, notification):
        nvdrive_logger.info('Unsubscribing from a UI notification')
        if notification.identifier not in self.ui_notifications:
            raise NotificationException('Not subscribed to the notification')
        self.nvd_client.run(UnregisterUINotification(notification.ui_event_id))
        self.ui_notifications.pop(notification.identifier)

    def retrieve_indentifier(self, idn_dict, block):
        if block.identifier in idn_dict:
            return block.identifier
        else:
            for key in idn_dict:
                if key in block.identifier[:len(key)]:
                    return key
        return ''

    def handle_notification(self, timeout=None):
        """This function has to be called to receive and proceed\
         a notification

        :param timeout: Timeout in seconds
        :return:
        """
        self.handler.timeout_on_recv = timeout
        head = HeadBlock(self.handler)
        DataBlockType = id_to_block[head.block_id]
        data = DataBlockType(self.handler, head.block_size)
        if DataBlockType == SettingDataBlock:
            identifier = self.retrieve_indentifier(
                self.setting_notifications,
                data
            )
            if identifier != '':
                notif = self.setting_notifications[identifier]
            else:
                notif = SettingNotification(data.module,
                                            data.submodule,
                                            data.setting)
            notif.head_block = head
            notif.data_block = data
            self.setting_notification_callback(notif)
        elif DataBlockType == StateDataBlock:
            identifier = self.retrieve_indentifier(
                self.state_notifications,
                data
            )
            if identifier != '':
                notif = self.state_notifications[identifier]
            else:
                notif = StateNotification(data.module,
                                          data.submodule,
                                          data.setting)

            notif.head_block = head
            notif.data_block = data
            self.state_notification_callback(notif)
        elif DataBlockType == ResultDataBlock:
            self.result_notifications[data.identifier].head_block = head
            self.result_notifications[data.identifier].data_block = data
            self.result_notification_callback(
                self.result_notifications[data.identifier]
            )
        elif DataBlockType == CommandDataBlock:
            self.command_notifications[data.identifier].head_block = head
            self.command_notifications[data.identifier].data_block = data
            self.command_notification_callback(
                self.command_notifications[data.identifier]
            )
        elif DataBlockType == MeasurementDataBlock:
            self.measurement_notifications[data.identifier].head_block = head
            self.measurement_notifications[data.identifier].data_block = data
            self.measurement_notification_callback(
                self.measurement_notifications[data.identifier]
            )
        elif DataBlockType == UIDataBlock:
            self.ui_notifications[data.identifier].head_block = head
            self.ui_notifications[data.identifier].data_block = data
            self.ui_notification_callback(
                self.ui_notifications[data.identifier]
            )
        else:
            raise NotificationTypeException('Unknown notification type')

    def setting_notification_callback(self, notification: SettingNotification):
        """This method is called when a setting notification is read

        :param notification:
        :return:
        """
        print('Setting notification received !')
        print('The setting {}.{}.{}'.format(
            notification.data_block.module,
            notification.data_block.submodule,
            notification.data_block.setting))
        gsv_command = GetSettingValue(notification.data_block.module,
                                      notification.data_block.submodule,
                                      notification.data_block.setting)
        self.nvd_client.run(gsv_command)
        print('Changed its value to "{}"'.format(gsv_command.setting_value))

    def state_notification_callback(self, notification: StateNotification):
        """This method is called when a state notification is read

        :param notification:
        :return:
        """
        print('State notification received !')
        print('On IDN {}.{}.{}'.format(
            notification.data_block.module,
            notification.data_block.submodule,
            notification.data_block.setting))

    def result_notification_callback(self, notification: ResultNotification):
        """This method is called when a new result notification is read

        :param notification:
        :return:
        """
        print('Result notification received !')
        print('New result on module {}'.format(notification.module))

    def command_notification_callback(self, notification: CommandNotification):
        """This method is called when a command notification is read

        :param notification:
        :return:
        """
        print('Command notification received !')
        print('Received the command "{}"'.format(notification.command))

    def measurement_notification_callback(
            self,
            notification: MeasurementNotification):
        """This method is called when a new measurement notification is read

        :param notification:
        :return:
        """
        print('Measurement notification received !')

    def ui_notification_callback(self, notification: UINotification):
        """This method is called when a UI notification is read

        :param notification:
        :return:
        """
        print('UI notification received !')
        print('On UI element with ID: {}'.format(
            notification.data_block.command_id))
