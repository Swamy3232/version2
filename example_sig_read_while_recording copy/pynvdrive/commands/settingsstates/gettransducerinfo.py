import struct

from ... import Command


class GetTransducerInfo(Command):
    def __init__(self, transducer_ID, version='2'):
        super().__init__(name=None, parameters=[transducer_ID, str(version)])
        self.version = int(version)
        self.value = None
        self.transducerName = None
        self.manufacturerName = None
        self.modelName = None
        self.SN = None
        self.coupling = None
        self.factorySensitivity = None
        self.abbreviationSensitivity = None
        self.factoryOffset = None
        self.abbreviationOffset = None
        self.lastCalibYear = None
        self.lastCalibMonth = None
        self.lastCalibDay = None
        self.comments = None

        # Version 1
        self.lastCalibrationSensitivity = None
        self.lastCalibrationOffset = None
        self.userLastCalibration = None
        self.analyzerLastCalibration = None
        self.inputUsedLastCalibration = None
        self.nameCalibratorLastCalibration = None

        # Version 2
        self.isFactorySensitivityApplied = None

        return

    def parse_response(self, response):
        try:
            _, _ = response.split(b'\0', 1)
        except Exception:
            raise NotImplementedError('No window displayed into chosen layout')

        self.value = self.parse_response_list_string(response)


    def parse_response_list_string(self, contents):
        # print(contents)
        # if not contents.endswith(b'\0'):
        #     raise pynvdrive.NVDriveCommandParsing('expected trailing zero')
        # Note: the current NVGate implementation does not support unicode for this command

        temp = contents.split(b'\0')

        self.transducerName = self.parse_response_string(temp[0])
        self.manufacturerName = self.parse_response_string(temp[1])
        self.modelName = self.parse_response_string(temp[2])
        self.SN = self.parse_response_string(temp[3])
        self.coupling = self.parse_response_string(temp[4])

        temp = contents.split(b'\0', 5)[-1]
        self.factorySensitivity = struct.unpack('f', temp[0:4])[0]

        temp = temp[4:]
        temp = temp.split(b'\0',1)

        self.abbreviationSensitivity = self.parse_response_string(temp[0])
        temp = temp[1]
        self.factoryOffset = struct.unpack('f', temp[0:4])[0]

        temp = temp[4:]
        temp = temp.split(b'\0', 1)
        self.abbreviationOffset = self.parse_response_string(temp[0])

        temp = temp[1]
        self.lastCalibYear = int.from_bytes(temp[0:4], byteorder='little', signed=False)
        self.lastCalibMonth = int.from_bytes(temp[4:8], byteorder='little', signed=False)
        self.lastCalibDay = int.from_bytes(temp[8:12], byteorder='little', signed=False)

        temp = temp[12:]

        temp = temp.split(b'\0', 1)
        self.comments = self.parse_response_string(temp[0])
        temp = temp[-1]

        if self.version >= 1:
            self.lastCalibrationSensitivity = struct.unpack('f', temp[0:4])[0]
            self.lastCalibrationOffset = struct.unpack('f', temp[4:8])[0]

            temp = temp[8:]
            temp = temp.split(b'\0', 4)
            self.userLastCalibration = temp[0]
            self.analyzerLastCalibration = temp[1]
            self.inputUsedLastCalibration = temp[2]
            self.nameCalibratorLastCalibration = temp[3]

            temp = temp[-1]

        if self.version >= 2:
            self.isFactorySensitivityApplied = struct.unpack('?', temp)[0]

        return [self.transducerName,self.manufacturerName, self.modelName,
                self.SN, self.coupling, self.factorySensitivity, self.abbreviationSensitivity,
                self.factoryOffset, self.abbreviationOffset, self.lastCalibYear, self.lastCalibMonth,
                self.lastCalibDay, self.comments, self.lastCalibrationSensitivity,
                self.lastCalibrationOffset, self.userLastCalibration, self.analyzerLastCalibration,
                self.inputUsedLastCalibration, self.nameCalibratorLastCalibration, self.isFactorySensitivityApplied]
