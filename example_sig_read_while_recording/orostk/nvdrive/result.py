import logging

from orostk.idn import Idn
from orostk.nvdrive.nvdrive_exceptions import IncompleteResultException
from orostk.nvdrive.result_utils import FieldType
from orostk.nvdrive.nvd_utils import extract_byte_size


nvdrive_logger = logging.getLogger('NVDriveLogger')


class Result(object):
    """
    This class is a generic class for a result.
    Results are composed of ResultBlocks.
    All kinds of Result have HEAD and INFO blocks
    """

    def __init__(self, module, process_id, channel_number,
                 refchannel_number, input_channel_name,
                 input_refchannel_name, head=None, info=None):
        """

        :param module: new generation module name
        :type module: str
        :param process_id:
        :type process_id: int
        :param channel_number:
        :type channel_number: int
        :param refchannel_number:
        :type refchannel_number: int
        :param input_channel_name:
        :type input_channel_name: str
        :param input_refchannel_name:
        :type input_refchannel_name: str
        :param head:
        :type head: HeadBlock
        :param info:
        :type info: InfoBlock
        :return:
        """

        self.module = module
        self.process_id = process_id
        self.channel_number = channel_number
        self.refchannel_number = refchannel_number
        self.input_channel_name = input_channel_name
        self.input_refchannel_name = input_refchannel_name

        self.head = head
        self.info = info
        self.total_size = 0
        self.res_size = 0
        self.serialized_result_info = []

    @property
    def module_id(self):
        return Idn(self.module).module_id

    def serialize_blocks(self):
        """
        This method is specific to a kind of result.
        It puts the blocks in a list with the good order.
        :return:
        """
        raise NotImplementedError("Can't serialize a generic Result")

    def serialize_fields(self):
        """
        This method serializes all fields in blocks in a list
        It also calculate the total size of the result in bytes

        :return: A list of fields
        """
        field_list = []
        self.total_size = 0
        self.res_size = 0
        self.serialized_result_info = []
        # APPEND RESULT DESCRIPTION
        self.serialized_result_info.append((self.module_id, FieldType.SHORT))
        self.serialized_result_info.append((self.process_id, FieldType.UINT))
        self.serialized_result_info.append(
            (self.channel_number, FieldType.UINT))
        self.serialized_result_info.append(
            (self.refchannel_number, FieldType.UINT))
        self.serialized_result_info.append(
            (self.input_channel_name, FieldType.STRING))
        if self.refchannel_number > 0:
            self.serialized_result_info.append(
                (self.input_refchannel_name, FieldType.STRING))
        field_list += self.serialized_result_info
        self.res_size = extract_byte_size(self.serialized_result_info)
        self.total_size += self.res_size
        # APPEND BLOCKS
        for block in self.serialize_blocks():
            field_list += block.serialize()
            self.total_size += block.total_size
        nvdrive_logger.debug(
            'Total size of the result in bytes: {}'.format(self.total_size))
        return field_list

    def is_SI(self):
        """

        :return: True if the result is in SI, else False
        """
        if self.head is None:
            raise IncompleteResultException(
                "No HEAD block in the result, can't check if it's SI"
            )
        return self.head.is_SI()


class ScalarResult(Result):
    """
    This class represents a Scalar result.
    It's composed by:

    - HEAD
    - SCAL
    - INFO

    Example::

        res = ScalarResult(module='tcp', process_id=185, channel_number=0,
                           refchannel_number=0, input_channel_name='MyInput',
                           input_refchannel_name='RefInput', head=head,
                           scal=scal, info=info)

    """

    def __init__(self, module, process_id, channel_number,
                 refchannel_number, input_channel_name,
                 input_refchannel_name='', head=None, scal=None, info=None):
        """

        :param module:
        :type module: str
        :param process_id:
        :type process_id: int
        :param channel_number:
        :type channel_number: int
        :param refchannel_number:
        :type refchannel_number: int
        :param input_channel_name:
        :type input_channel_name: str
        :param input_refchannel_name:
        :type input_refchannel_name: str
        :param head:
        :type head: HeadBlock
        :param info:
        :type info: InfoBlock
        :param scal:
        :type scal: ScalBlock
        :return:
        """
        super().__init__(module, process_id, channel_number,
                         refchannel_number, input_channel_name,
                         input_refchannel_name, head, info)
        self.scal = scal

    def serialize_blocks(self):
        """
        This method is specific to a kind of result.
        It puts the blocks in a list with the right order:

        - HEAD
        - SCAL
        - INFO

        :return: A list containing the blocks
        """
        if self.head is None:
            raise IncompleteResultException('Missing HEAD block')
        elif self.scal is None:
            raise IncompleteResultException('Missing SCAL block')
        elif self.info is None:
            raise IncompleteResultException('Missing INFO block')
        block_list = list()
        block_list.append(self.head)
        block_list.append(self.scal)
        block_list.append(self.info)
        return block_list


class RegVectorResult(Result):
    """
    This class represents a Regular Vector result.
    It's composed by:

    - HEAD
    - XREG
    - CVEC/RVEC
    - INFO

    Example::

        res = RegVectorResult(module='tcp', process_id=177, channel_number=1,
                              refchannel_number=0,
                              input_channel_name='MyInput',
                              input_refchannel_name='RefInput',
                              head=head, xreg=xreg, c_r_vec=rvec, info=info)

    """

    def __init__(self, module, process_id, channel_number,
                 refchannel_number, input_channel_name,
                 input_refchannel_name='', head=None, xreg=None,
                 c_r_vec=None, info=None):
        """

        :param module:
        :type module: str
        :param process_id:
        :type process_id: int
        :param channel_number:
        :type channel_number: int
        :param refchannel_number:
        :type refchannel_number: int
        :param input_channel_name:
        :type input_channel_name: str
        :param input_refchannel_name:
        :type input_refchannel_name: str
        :param head:
        :type head: HeadBlock
        :param info:
        :type info: InfoBlock
        :param xreg:
        :type xreg: XregBlock
        :param c_r_vec:
        :type c_r_vec: CvecBlock or RvecBlock
        :return:
        """
        super().__init__(module, process_id, channel_number,
                         refchannel_number, input_channel_name,
                         input_refchannel_name, head, info)
        self.xreg = xreg
        self.c_r_vec = c_r_vec

    def serialize_blocks(self):
        """
        This method is specific to a kind of result.
        It puts the blocks in a list with the good order:

        - HEAD
        - XREG
        - CVEC/RVEC
        - INFO

        :return: A list containing the blocks
        """
        if self.head is None:
            raise IncompleteResultException('Missing HEAD block')
        elif self.xreg is None:
            raise IncompleteResultException('Missing XREG block')
        elif self.c_r_vec is None:
            raise IncompleteResultException('Missing CVEC/RVEC block')
        elif self.info is None:
            raise IncompleteResultException('Missing INFO block')

        if self.head.size != len(self.c_r_vec.data):
            raise IncompleteResultException('''The size specified in HEAD and\
            the number of data in the RVEC/CVEC block is different''')

        block_list = list()
        block_list.append(self.head)
        block_list.append(self.xreg)
        block_list.append(self.c_r_vec)
        block_list.append(self.info)
        return block_list

    def is_SI(self):
        """

        :return: True if the result is in SI, else False
        """
        if not super().is_SI():
            return False
        if self.xreg is None:
            raise IncompleteResultException(
                "No XREG block in the result, can't check if it's SI"
            )
        return self.xreg.is_SI()


class RefVectorResult(Result):
    """
    This class represents a Referenced Vector result.
    It's composed by:

    - HEAD
    - XREF
    - CVEC/RVEC
    - INFO

    Example::

        res = RefVectorResult(module='tcp', process_id=185,
                              channel_number=1, refchannel_number=0,
                              input_channel_name='MyInputRef',
                              input_refchannel_name='RefInput', head=head,
                              xref=xref, c_r_vec=rvec, info=info)
    """

    def __init__(self, module, process_id, channel_number,
                 refchannel_number, input_channel_name,
                 input_refchannel_name='', head=None, xref=None,
                 c_r_vec=None, info=None):
        """

        :param module:
        :type module: str
        :param process_id:
        :type process_id: int
        :param channel_number:
        :type channel_number: int
        :param refchannel_number:
        :type refchannel_number: int
        :param input_channel_name:
        :type input_channel_name: str
        :param input_refchannel_name:
        :type input_refchannel_name: str
        :param head:
        :type head: HeadBlock
        :param info:
        :type info: InfoBlock
        :param xref:
        :type xref: XrefBlock
        :param c_r_vec:
        :type c_r_vec: CvecBlock or RvecBlock
        :return:
        """
        super().__init__(module, process_id, channel_number,
                         refchannel_number, input_channel_name,
                         input_refchannel_name, head, info)
        self.xref = xref
        self.c_r_vec = c_r_vec

    def serialize_blocks(self):
        """
        This method is specific to a kind of result.
        It puts the blocks in a list with the good order:

        - HEAD
        - XREF
        - CVEC/RVEC
        - INFO

        :return: A list containing the blocks
        """
        if self.head is None:
            raise IncompleteResultException('Missing HEAD block')
        elif self.xref is None:
            raise IncompleteResultException('Missing XREF block')
        elif self.c_r_vec is None:
            raise IncompleteResultException('Missing CVEC/RVEC block')
        elif self.info is None:
            raise IncompleteResultException('Missing INFO block')

        if self.head.size != len(self.c_r_vec.data):
            raise IncompleteResultException('''The size specified in HEAD and\
            the number of data in the RVEC/CVEC block is different''')
        block_list = list()
        block_list.append(self.head)
        block_list.append(self.xref)
        block_list.append(self.c_r_vec)
        block_list.append(self.info)
        return block_list

    def is_SI(self):
        """

        :return: True if the result is in SI, else False
        """
        if not super().is_SI():
            return False
        if self.xref is None:
            raise IncompleteResultException(
                "No XREG block in the result, can't check if it's SI"
            )
        return self.xref.is_SI()


class WaterfallResult(Result):
    """
    This class represents a 3D Waterfall result.
    It's composed by:

    - HEAD
    - DWTF
    - XREF
    - XREG
    - CWTF/RWTF
    - INFO

    Example::

        res = WaterfallResult(module='tcp', process_id=187,
                              channel_number=1, refchannel_number=0,
                              input_channel_name='MyInput',
                              input_refchannel_name='RefInput',
                              head=head, xref=xref, dwtf=dwtf,
                              xreg=xreg, c_r_wtf=rwtf, info=info)
    """

    def __init__(self, module, process_id, channel_number,
                 refchannel_number, input_channel_name,
                 input_refchannel_name='', head=None, dwtf=None,
                 xref=None, xreg=None, c_r_wtf=None, info=None):
        """

        :param module:
        :type module: str
        :param process_id:
        :type process_id: int
        :param channel_number:
        :type channel_number: int
        :param refchannel_number:
        :type refchannel_number: int
        :param input_channel_name:
        :type input_channel_name: str
        :param input_refchannel_name:
        :type input_refchannel_name: str
        :param head:
        :type head: HeadBlock
        :param info:
        :type info: InfoBlock
        :param xref:
        :type xref: XrefBlock
        :param xreg:
        :type xreg: XregBlock
        :param c_r_wtf:
        :type c_r_wtf: CwtfBlock or RwtfBlock
        :param dwtf:
        :type dwtf: DwtfBlock
        :return:
        """
        super().__init__(module, process_id, channel_number,
                         refchannel_number, input_channel_name,
                         input_refchannel_name, head, info)
        self.dwtf = dwtf
        self.xref = xref
        self.xreg = xreg
        self.c_r_wtf = c_r_wtf

    def serialize_blocks(self):
        """
        This method is specific to a kind of result.
        It puts the blocks in a list with the good order:

        - HEAD
        - DWTF
        - XREF
        - XREG
        - CWTF/RWTF
        - INFO

        :return: A list containing the blocks
        """
        if self.head is None:
            raise IncompleteResultException('Missing HEAD block')
        elif self.dwtf is None:
            raise IncompleteResultException('Missing DWTF block')
        elif self.xref is None:
            raise IncompleteResultException('Missing XREF block')
        elif self.xreg is None:
            raise IncompleteResultException('Missing XREG block')
        elif self.c_r_wtf is None:
            raise IncompleteResultException('Missing CWTF/RWTF block')
        elif self.info is None:
            raise IncompleteResultException('Missing INFO block')

        if self.head.size != self.c_r_wtf.depth * self.c_r_wtf.vector_size:
            raise IncompleteResultException('''The size specified in HEAD and\
                the number of data in the RWTF/CWTF block is different''')
        block_list = list()
        block_list.append(self.head)
        block_list.append(self.dwtf)
        block_list.append(self.xref)
        block_list.append(self.xreg)
        block_list.append(self.c_r_wtf)
        block_list.append(self.info)
        return block_list

    def is_SI(self):
        """

        :return: True if the result is in SI, else False
        """
        if not super().is_SI():
            return False
        if self.xreg is None:
            raise IncompleteResultException(
                "No XREG block in the result, can't check if it's SI"
            )
        if self.xref is None:
            raise IncompleteResultException(
                "No XREF block in the result, can't check if it's SI"
            )
        return self.xreg.is_SI() and self.xref.is_SI()
