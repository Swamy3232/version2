from ..blocks.RESULTBLOCK import ResultBlock
import struct
from datetime import datetime, timedelta
from dateutil import tz

EPOCH_AS_FILETIME = 116444736000000000  # Difference between 1601-01-01 to 1970-01-01


class INFO(ResultBlock):
    """
    This class represent an INFO block
    fields:

    - id.
    - version (actual version is 1).
    - block_size.
    - info_mask.
    - global_level.
    - weighted_global_level.
    - tacho.
    - date.

    Example::

        info = INFO(version=1, info_mask=1, global_level=1,
                         weighted_global_level=0, tacho=0)

    """
    def __init__(self, version=1, info_mask=0x1, global_level=0, weighted_global_level=0, tacho=0, date=None):
        """

        :param version:
        :type version: int
        :param info_mask: An integer representing an
        InfoMask as described in NVDrive documentation
        :type info_mask: int
        :param global_level:
        :type global_level: float
        :param weighted_global_level:
        :type weighted_global_level: float
        :param tacho:
        :type tacho: float
        :param date: Date in UTC
        :type date: datetime
        :return:
        """
        super().__init__('INFO', version)

        self.version = version

        self.info_mask = info_mask
        self.global_level = global_level
        self.weighted_global_level = weighted_global_level
        self.tacho = tacho

        # The date is in UTC
        self.date = date if date is not None else datetime(2000, 1, 1)

        return

    def convert_datetime(self):
        """Convert NVGate Win32 epoch time (1601-01-01) to Python unix time (1970-01-01)
        """
        if isinstance(self.date, datetime):
            # Because NVGate is 64bit date, since 1601-01-01, have to convert from Python datetime 1970-01-01
            seconds_epoch = self.date.timestamp()
            nanoseconds_epoch = seconds_epoch * 10000000

            self.date = int(nanoseconds_epoch + EPOCH_AS_FILETIME)

    def convert_epoch_to_datetime(self):
        """
        Convert epoch NVGate date to datetime
        """
        if isinstance(self.date, int):
            # Because NVGate is 64bit date, since 1601-01-01, have to convert from Python datetime 1970-01-01
            self.date -= EPOCH_AS_FILETIME
            try:
                self.date = datetime(1970, 1, 1) + timedelta(seconds=self.date/10000000)
                # Convert to local timezone
                self.date = self.date.replace(tzinfo=tz.tzutc())  # Tell the datetime object that it's in UTC timezone
                self.date = self.date.astimezone(tz.tzlocal())  # Convert to local timezone
            except Exception:
                self.date = datetime.now(tz.tzlocal())

    def to_binary(self):
        """Generate binary block using attributes
        """
        self.binary_body = b''

        b_info_mask = struct.pack('l', self.info_mask)
        self.binary_body += b_info_mask
        b_global_level = struct.pack('f', self.global_level)
        self.binary_body += b_global_level
        b_weighted_global_level = struct.pack('f', self.weighted_global_level)
        self.binary_body += b_weighted_global_level
        b_tacho = struct.pack('f', self.tacho)
        self.binary_body += b_tacho

        self.convert_datetime()

        b_date = struct.pack('q', self.date)
        self.binary_body += b_date

        self.get_binary_header()

        return self.binary_header + self.binary_body

    def from_binary(self, contents):
        """Parse binary block
        """
        self.binary_header = contents[:6]
        self.binary_body = contents[6:]

        self.parse_header()
        self.parse_body()

        self.convert_epoch_to_datetime()

    def from_dict(self, block_dict: dict):
        """Convert a dictionary to a block
        :param block_dict: block dictionary
        :return:
        """
        self.version = block_dict.get('version', self.version)
        self.info_mask = block_dict.get('info_mask', self.info_mask)
        self.global_level = block_dict.get('global_level', self.global_level)
        self.weighted_global_level = block_dict.get('weighted_global_level', self.weighted_global_level)
        self.tacho = block_dict.get('tacho', self.tacho)
        self.date = block_dict.get('date', self.date)

        return self

    def parse_body(self):
        """Parse binary body to individuals attributes
        """
        self.info_mask = struct.unpack('l', self.binary_body[:4])[0]
        self.global_level = struct.unpack('f', self.binary_body[4:8])[0]
        self.weighted_global_level = struct.unpack('f', self.binary_body[8:12])[0]
        self.tacho = struct.unpack('f', self.binary_body[12:16])[0]
        self.date = struct.unpack('q', self.binary_body[16:24])[0]
        self.date = int(self.date)

    def convert_to_SI(self):
        """Convert result to SI if needed
        """
        return self
