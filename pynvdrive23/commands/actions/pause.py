from ... import CommandAction

class Pause(CommandAction):
    """
    If a measurement is in the process of acquisition:

        - If the measurement is in the « run » mode,
          interrupt the measurement. It then moves to the “pause” mode.
        - If the measurement is in the “pause” mode,
          continue the measurement which moves to the “run” mode.

    """
    pass