from ..quantity.quantity_provider import QuantityProvider
import json
from datetime import datetime
from pynvdrive.formats.blocks import HEAD, XREG, XREF, CVEC, RVEC, SCAL, DWTF, RWTF, CWTF, INFO, ORBT, RNFO, TCPRESULT
from .result_format_and_description import ResultFormatAndDescription
from .process import processes_to_tcp
from pynvdrive.formats.utils.octave import OCTAVE_BAND_VALUES

from copy import copy


class Result:
    """
    This class is a generic class for a result.
    Results are composed of ResultBlocks.
    All kinds of Result have HEAD and INFO blocks
    """
    def __init__(self, head=None, xreg=None, xref=None, cvec=None, rvec=None, scal=None, dwtf=None, rwtf=None,
                 cwtf=None, info=None, orbt=None, rnfo=None, quantity_provider:QuantityProvider=None):
        self.head = head
        self.xreg = xreg
        self.xref = xref
        self.cvec = cvec
        self.rvec = rvec
        self.scal = scal
        self.dwtf = dwtf
        self.rwtf = rwtf
        self.cwtf = cwtf
        self.info = info
        self.orbt = orbt
        self.rnfo = rnfo

        self.binary = None

        self.list_block = []

        if quantity_provider:
            self.quantity_provider = quantity_provider
        else:
            self.quantity_provider = QuantityProvider()

        self.meta_results = ResultFormatAndDescription()

    @property
    def input_name(self):
        return self.meta_results.input_name

    @input_name.setter
    def input_name(self, input_name):
        self.meta_results.input_name = input_name

    @property
    def module_id(self):
        return self.meta_results.module_id

    @module_id.setter
    def module_id(self, module_id):
        self.meta_results.module_id = module_id

    @property
    def process_id(self):
        return self.meta_results.process_id

    @process_id.setter
    def process_id(self, process_id):
        self.meta_results.process_id = process_id

    @property
    def channel_number(self):
        return self.meta_results.channel_number

    @channel_number.setter
    def channel_number(self, channel_number):
        self.meta_results.channel_number = channel_number

    @property
    def reference_channel_number(self):
        return self.meta_results.reference_channel_number

    @reference_channel_number.setter
    def reference_channel_number(self, reference_channel_number):
        self.meta_results.reference_channel_number = reference_channel_number

    @property
    def input_name_reference_channel_number(self):
        return self.meta_results.input_name_reference_channel_number

    @input_name_reference_channel_number.setter
    def input_name_reference_channel_number(self, input_name_reference_channel_number):
        self.meta_results.input_name_reference_channel_number = input_name_reference_channel_number

    def json_default(self, value):
        if hasattr(value, '__dict__'):
            return value.__dict__
        if isinstance(value, datetime):
            return dict(year=value.year, month=value.month, day=value.day)
        else:
            return value.__dict__

    def to_json(self):
        return json.dumps(self, default=self.json_default, sort_keys=True, indent=4, ensure_ascii=False)

    def to_dict(self):
        dict = {}
        if self.head:
            dict['head'] = self.head.to_dict()
        if self.xreg:
            dict['xreg'] = self.xreg.to_dict()
        if self.xref:
            dict['xref'] = self.xref.to_dict()
        if self.cvec:
            dict['cvec'] = self.cvec.to_dict()
        if self.rvec:
            dict['rvec'] = self.rvec.to_dict()
        if self.scal:
            dict['scal'] = self.scal.to_dict()
        if self.dwtf:
            dict['dwtf'] = self.dwtf.to_dict()
        if self.rwtf:
            dict['rwtf'] = self.rwtf.to_dict()
        if self.cwtf:
            dict['cwtf'] = self.cwtf.to_dict()
        if self.info:
            dict['info'] = self.info.to_dict()
        if self.orbt:
            dict['orbt'] = self.orbt.to_dict()
        if self.rnfo:
            dict['rnfo'] = self.rnfo.to_dict()

        dict['input_name'] = self.input_name
        dict['module_id'] = self.module_id
        dict['process_id'] = self.process_id
        dict['channel_number'] = self.channel_number
        dict['input_name_reference_channel_number'] = self.input_name_reference_channel_number
        dict['reference_channel_number'] = self.reference_channel_number

        return dict

    def from_dict(self, result_dict):
        """
        Convert a result from a dict to a result

        """
        self.head = None
        self.xreg = None
        self.xref = None
        self.cvec = None
        self.rvec = None
        self.scal = None
        self.dwtf = None
        self.rwtf = None
        self.cwtf = None
        self.info = None
        self.orbt = None
        self.rnfo = None

        self.input_name = result_dict.get('input_name', '')
        self.module_id = result_dict.get('module_id', '')
        self.process_id = result_dict.get('process_id', '')
        self.channel_number = result_dict.get('channel_number', '')
        self.input_name_reference_channel_number = result_dict.get('input_name_reference_channel_number', None)
        self.reference_channel_number = result_dict.get('reference_channel_number', None)

        if 'head' in result_dict:
            self.head = HEAD()
            self.head.from_dict(result_dict['head'])
        if 'xreg' in result_dict:
            self.xreg = XREG()
            self.xreg.from_dict(result_dict['xreg'])
        if 'xref' in result_dict:
            self.xref = XREF()
            self.xref.from_dict(result_dict['xref'])
        if 'cvec' in result_dict:
            self.cvec = CVEC()
            self.cvec.from_dict(result_dict['cvec'])
        if 'rvec' in result_dict:
            self.rvec = RVEC()
            self.rvec.from_dict(result_dict['rvec'])
        if 'scal' in result_dict:
            self.scal = SCAL()
            self.scal.from_dict(result_dict['scal'])
        if 'dwtf' in result_dict:
            self.dwtf = DWTF()
            self.dwtf.from_dict(result_dict['dwtf'])
        if 'rwtf' in result_dict:
            self.rwtf = RWTF()
            self.rwtf.from_dict(result_dict['rwtf'])
        if 'cwtf' in result_dict:
            self.cwtf = CWTF()
            self.cwtf.from_dict(result_dict['cwtf'])
        if 'info' in result_dict:
            self.info = INFO()
            self.info.from_dict(result_dict['info'])
        if 'orbt' in result_dict:
            self.orbt = ORBT()
            self.orbt.from_dict(result_dict['orbt'])
        if 'rnfo' in result_dict:
            self.rnfo = RNFO()
            self.rnfo.from_dict(result_dict['rnfo'])

        return self

    def to_binary(self):
        """
        Convert a result to binary format

        """
        self.construct_list()

        self.binary = b''

        try:
            for block in self.list_block:
                self.binary += block.to_binary()
        except Exception as e:
            raise ResultToBinaryError('error converting result to binary format: {}'.format(e))

        return self.binary

    @classmethod
    def from_binary(cls, binary):
        """
        Create a result from a binary format
        :param binary: binary result NVG format
        :return: Result
        """
        result = cls()

        delimiters = [b'HEAD', b'DWTF', b'XREG', b'XREF', b'CVEC', b'RVEC', b'SCAL', b'RWTF', b'CWTF', b'INFO', b'RNFO', b'ORBT']
        # print(binary)
        results = {}
        for delimiter in delimiters:
            test = binary.split(delimiter)
            if len(test) > 1: # If delimiters found
                reste = test[1]
                # Check all others delimiters, take shorter one
                for second_delimiter in delimiters:
                    test2 = reste.split(second_delimiter)
                    if len(test2)>1: # If can be split again, then split it
                        reste = test2[0]
                    else:
                        pass
                results[delimiter] = reste

        head = None
        xreg = None
        xref = None
        cvec = None
        rvec = None
        scal = None
        dwtf = None
        rwtf = None
        cwtf = None
        orbt = None
        info = None
        rnfo = None

        if b'HEAD' in results:
            # print(results[b'HEAD'])
            head = HEAD()
            head.from_binary(results[b'HEAD'])
        if b'XREG' in results:
            # print(results[b'XREG'])
            xreg = XREG()
            xreg.from_binary(results[b'XREG'])
        if b'XREF' in results:
            # print(results[b'XREF'])
            xref = XREF()
            xref.from_binary(results[b'XREF'], size=head.size)
        if b'CVEC' in results:
            # print(results[b'CVEC'])
            cvec = CVEC()
            cvec.from_binary(results[b'CVEC'], size=head.size)
        if b'RVEC' in results:
            # print(results[b'RVEC'])
            rvec = RVEC()
            rvec.from_binary(results[b'RVEC'])
        if b'SCAL' in results:
            # print(results[b'SCAL'])
            scal = SCAL()
            scal.from_binary(results[b'SCAL'])
        if b'DWTF' in results:
            # print(results[b'DWTF'])
            dwtf = DWTF()
            dwtf.from_binary(results[b'DWTF'])
        if b'RWTF' in results:
            # print(results[b'RWTF'])
            rwtf = RWTF()
            rwtf.from_binary(results[b'RWTF'])
        if b'CWTF' in results:
            # print(results[b'CWTF'])
            cwtf = CWTF()
            cwtf.from_binary(results[b'CWTF'])
        if b'ORBT' in results:
            # print(results[b'ORBT'])
            orbt = ORBT()
            orbt.from_binary(results[b'ORBT'])
        if b'INFO' in results:
            # print(results[b'INFO'])
            info = INFO()
            info.from_binary(results[b'INFO'])
        if b'RNFO' in results:
            # print(results[b'RNFO'])
            rnfo = RNFO()
            rnfo.from_binary(results[b'RNFO'])

        # print(results)
        result = Result()
        result.head = head
        result.xreg = xreg
        result.xref = xref
        result.cvec = cvec
        result.rvec = rvec
        result.scal = scal
        result.dwtf = dwtf
        result.rwtf = rwtf
        result.cwtf = cwtf
        result.orbt = orbt
        result.info = info
        result.rnfo = rnfo

        #result.module_id = module_id
        #result.process_id = process_id
        #result.channel_number = channel_number
        #result.channel_number = channel_number


        return result

    def construct_list(self):
        """
        Prepare the result to be converted, check if necessary blocks are present
        depending of ResultType

        """
        result_type = self.head.result_type

        self.list_block = []

        if not self.head:
            raise ResultBlockMissing('HEAD block is missing')
        self.list_block.append(self.head)

        # 1 : Scalar result, 2 : RegVector, 3 : RefVector, 8 : Waterfall
        if result_type == 1:
            if not self.scal:
                raise ResultBlockMissing('SCAL block is missing')
            self.list_block.append(self.scal)

        elif result_type == 2 or result_type == 3:
            if result_type == 2:
                if not self.xreg:
                    raise ResultBlockMissing('XREG block is missing')
                self.list_block.append(self.xreg)
            elif result_type == 3:
                if not self.xref:
                    raise ResultBlockMissing('XREF block is missing')
                self.list_block.append(self.xref)

            if self.head.is_complex > 0:
                if not self.cvec:
                    raise ResultBlockMissing('CVEC block is missing')
                self.list_block.append(self.cvec)
            else:
                if not self.rvec:
                    raise ResultBlockMissing('RVEC block is missing')
                self.list_block.append(self.rvec)

        elif result_type == 8:
            if not self.dwtf:
                raise ResultBlockMissing('DWTF block is missing')
            self.list_block.append(self.dwtf)
            if not self.xref:
                raise ResultBlockMissing('XREF block is missing')
            self.list_block.append(self.xref)

            if self.head.dimension == 2: # Waterfall 2D
                if self.head.iscomplex > 0:
                    if not self.cvec:
                        raise ResultBlockMissing('CVEC block is missing')
                    self.list_block.append(self.cvec)
                else:
                    if not self.rvec:
                        raise ResultBlockMissing('RVEC block is missing')
                    self.list_block.append(self.rvec)

            else: # Waterfall 3D
                if not self.xreg:
                    raise ResultBlockMissing('XREG block is missing')
                self.list_block.append(self.xreg)
                if self.head.iscomplex > 0:
                    if not self.cwtf:
                        raise ResultBlockMissing('CWTF block is missing')
                    self.list_block.append(self.cwtf)
                else:
                    if not self.rwtf:
                        raise ResultBlockMissing('RWTF block is missing')
                    self.list_block.append(self.rwtf)

        # TODO : block info if head version > ?
        if self.head.version:
            pass

        if not self.info:
            raise ResultBlockMissing('INFO block is missing')

        self.list_block.append(self.info)

        if self.orbt:
            self.list_block.append(self.orbt)

    def get_tcp_result(self):
        """
        Convert the current result to a TCP result for injection
        """
        # module_id mapping
        module_id_tcp = 498  # TCP module id

        # process_id mapping
        process_id_tcp = processes_to_tcp.get(self.process_id, None)

        if process_id_tcp is None:
            raise TCPProcessIDError('process_id not found in mapping : {}'.format(self.process_id))

        # channel_number mapping
        channel_number = self.channel_number

        # input_name mapping
        input_name = self.head.name

        reference_channel_number = 0

        tcp_result = TCPRESULT(module=module_id_tcp, process=process_id_tcp, channel=channel_number, ref_channel=reference_channel_number, input_name=input_name,
                               result=self)
        return tcp_result

    def get_value(self, position=None):
        """
        Get the value of a 2D result at a given position

        """
        # Result type
        if self.head.result_type == 1:  # Scalar
            return self.scal.value
        if not position:
            return None
        if self.head.result_type == 2:  # RegVector
            if self.module_id == 12:  # Octave
                octave_band_list = OCTAVE_BAND_VALUES[self.xreg.n_octave]
                start_difference = len(octave_band_list) - self.head.size
                octave_band_list = octave_band_list[start_difference:]
                # Find the idx of the position value
                try:
                    idx = octave_band_list.index(position)
                except ValueError:
                    return None
                # Find value at idx inside rvec
                # Check if idx is in rvec
                if idx < len(self.rvec.data):
                    return self.rvec.data[idx]
            elif self.module_id in (10, 11, 18, 19, 14, 17):  # FFT1, FFT2, FFT3, FFT4, SOA1, SOA2
                if self.xreg:  # If xreg is present
                    # Create the array between start, stop and head.size
                    start = self.xreg.start
                    stop = self.xreg.stop
                    step = (stop - start) / (self.head.size - 1)
                    freq_array = [start + step * i for i in range(self.head.size)]
                    # Find the idx of the position value, if not found return None
                    try:
                        # Find closest value
                        idx = min(range(len(freq_array)), key=lambda i: abs(freq_array[i] - position))
                    except ValueError:
                        return None
                    # Find value at idx inside rvec
                    # Check if idx is in rvec
                    if self.head.is_complex:
                        if idx < len(self.cvec.data):
                            imag = self.cvec.data[idx][1]
                            real = self.cvec.data[idx][0]
                            # Return modulus
                            return (real ** 2 + imag ** 2) ** 0.5
                    else:
                        if idx < len(self.rvec.data):
                            return self.rvec.data[idx]

        elif self.head.result_type == 3:  # RefVector
            raise NotImplementedError('Not implemented for RefVector')
        elif self.head.result_type == 8:  # Waterfall
            raise NotImplementedError('Waterfall result not implemented yet')
        else:
            raise NotImplementedError('Result type not implemented yet : {}'.format(self.head.result_type))

        return 0

    def get_unit(self, client=None, raise_errors=True):
        if not self.head:
            return None

        magnitude_key = self.head.magnitude_key
        unit = self.quantity_provider.get_unit_user(magnitude_key=magnitude_key, raise_errors=raise_errors)

        if unit.magnitude_name is None:
            # Unit unknown, create a unit with info from the result
            unit.magnitude_name = self.head.physical_quantity
            unit.magnitude_key = self.head.magnitude_key
            unit.unit_name = self.head.unit_name
            unit.unit_label = self.head.unit_label
            unit.coeff_A = 1.0
            unit.coeff_B = 0.0

        return unit

    def copy(self):
        """
        Copy the result
        """
        return copy(self)


class ResultException(Exception):
    pass


class ResultTypeError(ResultException):
    """
    Result type error
    """
    pass


class ResultToBinaryError(ResultException):
    """
    Error while converting to binary
    """
    pass


class ResultBlockMissing(ResultException):
    """
    Error if a block is missing into result
    """
    pass


class TCPProcessIDError(ResultException):
    """
    Error if process_id is not found in mapping
    """
    pass
