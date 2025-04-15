import copy

from ..blocks.RESULTBLOCK import b_str_EOL
import struct
from pynvdrive import ENCODING_MBCS


class TCPRESULT:
	"""
    A TCP result

    parameters:

        - ModuleNumber
        - ProcessNumber
        - ChannelNumber
        - ReferenceChannelNumber
        - InputName
        - Result

    """

	def __init__(self, module=498, process=None, channel=0, ref_channel=0, input_name=None, result=None, tcp_channel_id=None):
		self.module = module
		self.process = process
		self.channel = channel
		self.ref_channel = ref_channel
		self.input_name = input_name
		self.result = result
		self.result_si = None

		self.tcp_channel_id = tcp_channel_id

		self.binary = b''

		return

	def to_binary(self):
		"""Generate binary block using attributes
        """

		if self.tcp_channel_id is None:
			b_tcp_channel_id = bytes()
		else:
			b_tcp_channel_id = struct.pack('l', self.tcp_channel_id)

		b_tcp_module = struct.pack('H', self.module)
		b_tcp_process = struct.pack('I', self.process)
		b_tcp_channel = struct.pack('I', self.channel)
		b_tcp_ref_channel = struct.pack('I', self.ref_channel)
		b_tcp_inputName = bytes(self.input_name, ENCODING_MBCS, errors='replace') + b_str_EOL

		if self.tcp_channel_id is None:
			b_header = b_tcp_module + b_tcp_process + b_tcp_channel + b_tcp_ref_channel + b_tcp_inputName
		else:
			b_header = b_tcp_channel_id

		b_result = self.result_si.to_binary()

		length = len(b_header) + len(b_result)

		b_length = struct.pack('l', length)

		self.binary = b_length + b_header + b_result

		return self.binary

	def check_result_consistency(self):
		"""
        Check result consistency
        """
		# Check individual blocks consistency
		# TODO : add all consistensy block
		self.result.head.check_consistency()

		# Check if head unit exists
		# TODO : Use quantity_provider

		self.user_unit = self.result.head.check_unit_exist(quantity_provider=self.result.quantity_provider,
		                                                   magnitude_key=self.result.head.magnitude_key,
		                                                   physical_quantity=self.result.head.physical_quantity,
		                                                   unit_name=self.result.head.unit_name,
		                                                   unit_label=self.result.head.unit_label)
		self.result.head.magnitude_key = self.user_unit.magnitude_key
		self.result.head.physical_quantity = self.user_unit.magnitude_name
		self.result.head.unit_label = self.user_unit.unit_label
		self.result.head.unit_name = self.user_unit.unit_name

		# Convert to SI
		self.convert_result_to_SI()

	def convert_result_to_SI(self):
		"""
        Convert result to SI unit before pushing to NVGate
        """

		self.result_si = copy.deepcopy(self.result)

		if self.result_si.head:
			self.result_si.head = self.result_si.head.convert_to_SI()

		if self.result_si.xreg:
			self.result_si.xreg = self.result_si.xreg.convert_to_SI(quantity_provider=self.result.quantity_provider)

		if self.result_si.xref:
			self.result_si.xref = self.result_si.xref.convert_to_SI(quantity_provider=self.result.quantity_provider)

		if self.result_si.cvec:
			self.result_si.cvec = self.result_si.cvec.convert_to_SI(user_unit=self.user_unit)

		if self.result_si.rvec:
			self.result_si.rvec = self.result_si.rvec.convert_to_SI(user_unit=self.user_unit)

		if self.result_si.scal:
			self.result_si.scal = self.result_si.scal.convert_to_SI(user_unit=self.user_unit)

		if self.result_si.dwtf:
			self.result_si.dwtf = self.result_si.dwtf.convert_to_SI(user_unit=self.user_unit)

		if self.result_si.rwtf:
			self.result_si.rwtf = self.result_si.rwtf.convert_to_SI(user_unit=self.user_unit)

		if self.result_si.cwtf:
			self.result_si.cwtf = self.result_si.cwtf.convert_to_SI(user_unit=self.user_unit)

		if self.result_si.info:
			self.result_si.info = self.result_si.info.convert_to_SI()

		if self.result_si.orbt:
			self.result_si.orbt = self.result_si.orbt.convert_to_SI()

		return self.result_si
