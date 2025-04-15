from ... import Command


class SetTransducerAppliedSensitivity(Command):
    def __init__(self, transducer_ID, factory_current = '0'): #0 : LastCalibration, 1 : Factory Calibration
        super().__init__(name=None, parameters=[transducer_ID, factory_current])
        self.value = None
        return
