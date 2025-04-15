from ..blocks.RESULTBLOCK import ResultBlock
import struct


class DWTF(ResultBlock):
    """
    This class represent a DWTF block
    fields:

    - id.
    - version (actual version is 0).
    - block_size.
    - process_id.
    - first_index.
    - last_index.
    - request_status.


    Example::

        dwtf = DWTF(process_id=187, first_index=0, last_index=100,
                         request_status=0)

    """
    def __init__(self, version=0, process_id=None, first_index=None,
                 last_index=None, request_status=None):
        """

        :param version:
        :param process_id:
        :param first_index:
        :param last_index:
        :param request_status:
        :return:
        """
        super().__init__('DWTF', version)

        self.version = version

        self.process_id = process_id
        self.first_index = first_index
        self.last_index = last_index
        self.request_status = request_status

        return

    def to_binary(self):
        """Generate binary block using attributes
        """
        self.binary_body = b''

        b_process_id = struct.pack('h', self.process_id)
        self.binary_body += b_process_id
        b_first_index = struct.pack('l', self.first_index)
        self.binary_body += b_first_index
        b_last_index = struct.pack('l', self.last_index)
        self.binary_body += b_last_index
        b_request_status = struct.pack('h', self.request_status)
        self.binary_body += b_request_status

        self.get_binary_header()

        return self.binary_header + self.binary_body


    def from_binary(self, contents):
        """Parse binary block
        """
        self.binary_header = contents[:6]
        self.binary_body = contents[6:]

        self.parse_header()
        self.parse_body()

    def parse_body(self):
        """Parse binary body to individuals attributes
        """
        self.process_id = struct.unpack('h', self.binary_body[:2])[0]
        self.first_index = struct.unpack('l', self.binary_body[2:6])[0]
        self.last_index = struct.unpack('l', self.binary_body[6:10])[0]
        self.request_status = struct.unpack('h', self.binary_body[10:12])[0]

    def from_dict(self, block_dict: dict):
        """Convert a dictionary to a block
        :param block_dict: block dictionary
        :return:
        """
        self.version = block_dict.get('version', self.version)
        # TODO : finish from_dict parsing
        return self

    def convert_to_SI(self):
        """Convert result to SI if needed
        """
        return self