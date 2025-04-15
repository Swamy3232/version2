from ..blocks.RESULTBLOCK import ResultBlock
import struct
from datetime import datetime, timedelta
from dateutil import tz

EPOCH_AS_FILETIME = 116444736000000000  # Difference between 1601-01-01 to 1970-01-01


class RNFO(ResultBlock):
    """
    This class represent an RNFO block
    fields:

    - id.
    - version (actual version is 1).
    - block_size.
    - duration
    - rec_nb
    - state

    Example::

        rnfo = RNFO(version=1, duration=60, rec_nb=1, state=0)

    """
    def __init__(self, version=1, samples=0, duration=0, state=0):
        """

        :param version:
        :type version: int
        :param sample: Number of read samples
        :type sample: int
        :param duration: Duration of the signal read
        :type duration: float
        :param state: 0 if all the requested samples have been read
			1 if not enough data was available in the record and the recording is running
			2 if not enough data was available in the record and the recording is stopped
        :type state: short


        :return:
        """
        super().__init__('RNFO', version)

        self.version = version
        self.samples = samples
        self.duration = duration

        self.state = state

        return

    def to_binary(self):
        """Generate binary block using attributes
        """
        self.binary_body = b''
        b_samples = struct.pack('i', self.samples)
        self.binary_body += b_samples
        b_duration = struct.pack('f', self.duration)
        self.binary_body += b_duration
        b_state = struct.pack('h', self.state)
        self.binary_body += b_state

        self.get_binary_header()

        return self.binary_header + self.binary_body

    def from_binary(self, contents):
        """Parse binary block
        """
        self.binary_header = contents[:6]
        self.binary_body = contents[6:]

        self.parse_header()
        self.parse_body()

    def from_dict(self, block_dict: dict):
        """Convert a dictionary to a block
        :param block_dict: block dictionary
        :return:
        """
        self.version = block_dict.get('version', self.version)
        self.samples = block_dict.get('samples', self.samples)
        self.duration = block_dict.get('duration', self.duration)
        self.state = block_dict.get('state', self.state)

        return self

    def parse_body(self):
        """Parse binary body to individuals attributes
        """
        self.samples = struct.unpack('i', self.binary_body[0:4])[0]
        self.duration = struct.unpack('f', self.binary_body[4:8])[0]
        self.state = struct.unpack('h', self.binary_body[8:10])[0]

    def convert_to_SI(self):
        """Convert result to SI if needed
        """
        return self
