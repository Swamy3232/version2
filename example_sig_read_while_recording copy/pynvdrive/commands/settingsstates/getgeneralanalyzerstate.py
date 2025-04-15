from ... import Command
from enum import Enum


class GeneralAnalyzerState(Enum):
    """
    Enum for GeneralAnalyzerState, following nvdrive.doc
    """
    UNKNOWN = 0
    RUNNING = 3  # Include recording and triggering
    STOPPED = 4
    PAUSED = 6
    CALIBRATION = 9
    ARMED = 11  # Armed while waiting for a recording


class GetGeneralAnalyzerState(Command):
    def __init__(self):
        super().__init__(name=None, parameters=[])
        self.value = None
        self.state = None
        return

    def parse_response(self, response):
        temp = int.from_bytes(response.split(b'\0')[0], byteorder='little', signed=True)
        if temp == 0:
            self.value = 'Unknown'
            self.state = GeneralAnalyzerState.UNKNOWN
        elif temp == 3:
            self.value = 'Running'
            self.state = GeneralAnalyzerState.RUNNING
        elif temp == 4:
            self.value = 'Stopped'
            self.state = GeneralAnalyzerState.STOPPED
        elif temp == 6:
            self.value = 'Paused'
            self.state = GeneralAnalyzerState.PAUSED
        elif temp == 9:
            self.value = 'Calibrating'
            self.state = GeneralAnalyzerState.CALIBRATION
        elif temp == 11:
            self.value = 'Armed'
            self.state = GeneralAnalyzerState.ARMED
        else:
            self.value = 'Unknown'
            self.state = GeneralAnalyzerState.UNKNOWN

        return
