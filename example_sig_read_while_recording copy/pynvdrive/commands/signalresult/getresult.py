from ... import Command
from ...formats.result import Result
from ...formats.blocks import HEAD, XREG, RVEC, INFO
import struct


class GetResult(Command):
    def __init__(self, module, process, channel):
        super().__init__(name=None, parameters=[str(module), str(process), str(channel), '', '', '', '3'])
        self.value = None
        self.result = None
        return

    def parse_response(self, response):
        head = response.split(b'HEAD')[1].split(b'XREG')[0]
        xreg = response.split(b'XREG')[1].split(b'RVEC')[0]
        rvec = response.split(b'RVEC')[1].split(b'INFO')[0]
        info = response.split(b'INFO')[-1]

        head = self.parse_response_head(head)
        xreg = self.parse_response_xreg(xreg)
        rvec = self.parse_response_rvec(rvec, head.size)
        try:
            info = self.parse_response_info(info)
        except (Exception,):
            print('No INFO block')

        result = Result()
        result.head = head
        result.xreg = xreg
        result.rvec = rvec
        result.info = info

        self.result = result
        return result


    def parse_response_head(self, contents):
        myHEAD = HEAD()
        myHEAD.version = struct.unpack('h', contents[0:2])[0]
        myHEAD.block_size = struct.unpack('l', contents[2:6])[0]
        myHEAD.result_type = struct.unpack('h', contents[6:8])[0]
        myHEAD.size = struct.unpack('l', contents[8:12])[0]
        myHEAD.dimension = struct.unpack('h', contents[12:14])[0]
        myHEAD.complex = struct.unpack('h', contents[14:16])[0]
        myHEAD.measure_status = struct.unpack('h', contents[16:18])[0]

        reste = contents[18:]
        reste = reste.split(b'\0', 4)

        myHEAD.physical_quantity = self.parse_response_string(reste[0])
        myHEAD.unit_name = self.parse_response_string(reste[1])
        myHEAD.unit_label = self.parse_response_string(reste[2])
        myHEAD.name = self.parse_response_string(reste[3])
        if myHEAD.version == 3:
            pass
        elif myHEAD.version >= 1:
            reste = reste[4:][0]
            myHEAD.overall_level_status = struct.unpack('h', reste[0:2])[0]
            myHEAD.weighted_ol_status = struct.unpack('h', reste[2:4])[0]

            if myHEAD.version >= 4:
                myHEAD.weighting_window = struct.unpack('H', reste[4:6])[0]

            if myHEAD.version >= 5:
                reste = reste.split(b'\0')
                myHEAD.magnitude_key = self.parse_response_string(reste[-1])

        return myHEAD

    def parse_response_xreg(self, contents):
        myXREG = XREG()
        myXREG.version = struct.unpack('h', contents[0:2])[0]
        myXREG.block_size = struct.unpack('l', contents[2:6])[0]
        myXREG.start = struct.unpack('f', contents[6:10])[0]
        myXREG.stop = struct.unpack('f', contents[10:14])[0]
        myXREG.n_octave = struct.unpack('h', contents[14:16])[0]

        reste = contents[16:]
        reste = reste.split(b'\0', 3)

        myXREG.physical_quantity = self.parse_response_string(reste[0])
        myXREG.unit_name = self.parse_response_string(reste[1])
        myXREG.unit_label = self.parse_response_string(reste[2])

        if myXREG.version >= 1:
            reste = reste[-1]
            myXREG.rel_precision = struct.unpack('f', reste[0:4])[0]
            myXREG.abs_precision = struct.unpack('f', reste[4:8])[0]
        if myXREG.version >= 3:
            reste = reste.split(b'\0')
            myXREG.magnitude_key = self.parse_response_string(reste[-1])

        return myXREG

    @staticmethod
    def parse_response_rvec(contents, size):
        myRVEC = RVEC()
        myRVEC.version = struct.unpack('h', contents[0:2])[0]
        myRVEC.block_size = struct.unpack('l', contents[2:6])[0]
        myRVEC.real_min = struct.unpack('f', contents[6:10])[0]
        myRVEC.real_max = struct.unpack('f', contents[10:14])[0]

        reste = contents[14:]
        i = 0
        for i in range(0, size):
            temp = struct.unpack('f', reste[i*4:i*4+4])[0]
            myRVEC.data.append(temp)

        if myRVEC.version >= 1:
            myRVEC.real_rel_precision = struct.unpack('f', reste[i*4+4:i*4+8])[0]
            myRVEC.real_abs_precision = struct.unpack('f', reste[i*4+8:i*4+12])[0]

        return myRVEC

    @staticmethod
    def parse_response_info(contents):
        myINFO = INFO()
        myINFO.version = struct.unpack('h', contents[0:2])[0]
        myINFO.block_size = struct.unpack('l', contents[2:6])[0]
        myINFO.info_mask = struct.unpack('l', contents[6:10])[0]
        myINFO.global_level = struct.unpack('f', contents[10:14])[0]
        myINFO.weighted_global_level = struct.unpack('l', contents[14:18])[0]
        myINFO.tacho = struct.unpack('f', contents[18:22])[0]
        myINFO.date = struct.unpack('q', contents[22:30])[0]
        myINFO.date = int(myINFO.date)



        return myINFO

    @staticmethod
    def parse_response_SCAL(contents):
        # if not contents.endswith(b'\0'):
        #     raise pynvdrive.NVDriveCommandParsing('expected trailing zero')
        # Note: the current NVGate implementation does not support unicode for this command

        contents = contents.split(b'SCAL')
        return contents


    @staticmethod
    def parse_response_scalar(contents):
        temp = struct.unpack('f', contents)
        return temp[0]