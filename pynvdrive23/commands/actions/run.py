from ... import CommandAction

class Run(CommandAction):
    """
    If no measurement is in the process of acquisition,
    start a new measurement. The new measurement is in the “run” mode.

    If a measurement is in the process of acquisition:

        - If it is in the « pause » mode,
          reinitialize then restart the measurement.
        - If it is in the « run » mode,
          reinitialize then restart the measurement.

    """
    pass