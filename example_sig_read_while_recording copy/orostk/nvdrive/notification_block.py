import struct

from orostk.nvdrive.notification_utils import id_to_command, uint_idn_to_idn
from orostk.idn import Idn


class NotificationBlock(object):
    """
    Notification blocks are data block sent by NVGate to report
    an event. See ui_notification_list documentation for more details.
    """
    unpacker = struct.Struct('')

    def __init__(self, notification_handler, size):
        self.size = size
        self.data = notification_handler.get_block_data(self.size)

    def unpack(self):
        return self.unpacker.unpack(self.data[:self.unpacker.size])


class HeadBlock(NotificationBlock):

    unpacker = struct.Struct('=h h l')

    def __init__(self, notification_handler):
        super().__init__(notification_handler, self.unpacker.size)
        unpacked = self.unpack()
        self.version = unpacked[0]
        self.block_id = unpacked[1]
        self.block_size = unpacked[2]


class DataBlock(NotificationBlock):
    def __init__(self, notification_handler, size):
        super().__init__(notification_handler, size)

    @property
    def identifier(self):
        raise NotImplementedError


class SettingDataBlock(DataBlock):

    unpacker = struct.Struct('h h h h i I I i')

    def __init__(self, notification_handler, size):
        super().__init__(notification_handler, size)
        unpacked = self.unpack()
        self.module = unpacked[0].module
        self.submodule = unpacked[0].submodule
        self.setting = unpacked[0].setting

    def unpack(self):
        unpacked = self.unpacker.unpack(self.data[:self.unpacker.size])
        idn = uint_idn_to_idn(unpacked[5], unpacked[6], unpacked[7])
        return (idn,)

    @property
    def identifier(self):
        return '{}.{}.{}'.format(self.module,
                                 self.submodule,
                                 self.setting)


class StateDataBlock(DataBlock):

    unpacker = struct.Struct('h h h h i I I i')

    def __init__(self, notification_handler, size):
        super().__init__(notification_handler, size)
        unpacked = self.unpack()
        self.module = unpacked[0].module
        self.submodule = unpacked[0].submodule
        self.setting = unpacked[0].setting

    def unpack(self):
        unpacked = self.unpacker.unpack(self.data[:self.unpacker.size])
        idn = uint_idn_to_idn(unpacked[5], unpacked[6], unpacked[7])
        return (idn,)

    @property
    def identifier(self):
        return '{}.{}.{}'.format(self.module,
                                 self.submodule,
                                 self.setting)


class CommandDataBlock(DataBlock):

    unpacker = struct.Struct('l ? ?')

    def __init__(self, notification_handler, size):
        super().__init__(notification_handler, self.unpacker.size)
        unpacked = self.unpack()
        self.command = id_to_command[unpacked[0]]
        self.activation = unpacked[1]
        self.authorization = unpacked[2]

    @property
    def identifier(self):
        return self.command


class ResultDataBlock(DataBlock):

    unpacker = struct.Struct('=h')

    def __init__(self, notification_handler, size):
        super().__init__(notification_handler, self.unpacker.size)
        unpacked = self.unpack()
        idn = Idn(module=unpacked[0])
        self.module = idn.module

    @property
    def identifier(self):
        return self.module


class MeasurementDataBlock(DataBlock):

    def __init__(self, notification_handler, size):
        self.unpacker = struct.Struct('={}s'.format(size))
        super().__init__(notification_handler, self.unpacker.size)
        unpacked = self.unpack()
        self.measurement_name = unpacked[0].split(b'\0')[0].decode('utf-8')

    @property
    def identifier(self):
        return 'MeasurementNotification'


class UIDataBlock(DataBlock):

    unpacker = struct.Struct('=l l ?')

    def __init__(self, notification_handler, size):
        super().__init__(notification_handler, self.unpacker.size)
        unpacked = self.unpack()
        self.command_id = unpacked[0]
        self.nb_properties = unpacked[1]
        self.executed = unpacked[2]
        self.property_blocks = []
        for i in range(self.nb_properties):
            self.read_property(notification_handler)

    @property
    def identifier(self):
        return self.command_id

    def read_property(self, notification_handler):
        head = HeadBlock(notification_handler)
        DataBlockType = id_to_block[head.block_id]
        data = DataBlockType(notification_handler, head.block_size)
        self.property_blocks.append((head, data))


class UIPropertyDataBlock(DataBlock):
    """
    This block shlouldn't be used alone, only inside a UIDataBlock
    """
    unpacker = struct.Struct('l l s s ? ?')

    def __init__(self, notification_handler, size):
        # The total size of string is:
        #  unpacker - 2 * sizeof(l) - 2*sizeof(?)
        self.unpacker = struct.Struct('=l l {}s ? ?'.format(size - 10))
        super().__init__(notification_handler, self.unpacker.size)
        unpacked = self.unpack()
        self.type = unpacked[0]
        self.name_id = unpacked[1]
        self.value = unpacked[2].split(b'\0')[0].decode('utf-8')
        self.unit = unpacked[2].split(b'\0')[1].decode('utf-8')
        self.hidden = unpacked[3]
        self.const = unpacked[4]
        self.const_block = None
        if self.const:
            self.read_const(notification_handler)

    def read_const(self, notification_handler):
        head = HeadBlock(notification_handler)
        data = UIConstDataBlock(notification_handler, head.block_size)
        self.const_block = (head, data)


class UIEnumPropertyDataBlock(DataBlock):
    """
    This block shlouldn't be used alone, only inside a UIDataBlock
    """
    unpacker = struct.Struct('l l s s ? ? l')

    def __init__(self, notification_handler, size):
        # The total size of string is:
        #  unpacker - 3 * sizeof(l) - 2*sizeof(?) = 14
        super().__init__(notification_handler, size)
        self.unpacker = struct.Struct('=l l {}s ? ? l'.format(size - 14))
        unpacked = self.unpack()
        self.type = unpacked[0]
        self.name_id = unpacked[1]
        self.value = unpacked[2].split(b'\0')[0].decode('utf-8')
        self.unit = unpacked[2].split(b'\0')[1].decode('utf-8')
        self.hidden = unpacked[3]
        self.const = unpacked[4]
        self.enum_type = unpacked[5]


class UIConstDataBlock(DataBlock):
    """
    This block shlouldn't be used alone, only inside a UIDataBlock
    """
    unpacker = struct.Struct('l s s')

    def __init__(self, notification_handler, size):
        # The total size of string is the size of the unpacker - sizeof(l)
        self.unpacker = struct.Struct('=l {}s'.format(size - 4))
        super().__init__(notification_handler, self.unpacker.size)
        unpacked = self.unpack()
        self.type = unpacked[0]
        self.name = unpacked[1].split(b'\0')[0].decode('utf-8')
        self.value = unpacked[1].split(b'\0')[1].decode('utf-8')


# Dictionnary to identify block object from id
id_to_block = {
    0: SettingDataBlock,
    1: SettingDataBlock,
    2: SettingDataBlock,
    3: SettingDataBlock,
    4: SettingDataBlock,
    5: SettingDataBlock,
    6: SettingDataBlock,
    7: SettingDataBlock,
    8: SettingDataBlock,
    9: SettingDataBlock,
    10: StateDataBlock,
    11: SettingDataBlock,
    12: StateDataBlock,
    13: CommandDataBlock,
    14: UIDataBlock,
    15: UIPropertyDataBlock,
    16: UIConstDataBlock,
    17: UIEnumPropertyDataBlock,
    18: ResultDataBlock,
    19: SettingDataBlock,
    20: SettingDataBlock,
    21: MeasurementDataBlock,
}
