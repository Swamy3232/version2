from ... import CommandAction


class SetSaveOption(CommandAction):
    """
    Sets the preferences relating to creation of a new measurement.

    optional parameters:

        - SaveMode

            - 0, not saved
            - 1, saved in default measurement
            - 2(default), save with name confirmation
            - 3, save without name confirmation
        - KeyWord, associate a measurement to a keyword
        - AcquisitionSave

            - -1, no result are saved
            - 0, only the static results are saved
            - 1, only the dynamic results are saved
            - 2, both static and dynamic are saved
        - ManualSave

            - -1, no result are saved
            - 0, only the static results are saved
            - 1, only the dynamic results are saved
            - 2, both static and dynamic are saved


    """
    def __init__(self, save_mode_flag, keyword='', acquisition_save_flag='', manual_save_flag=''):
        acquisition_save_flag = '' if acquisition_save_flag is None else acquisition_save_flag
        manual_save_flag = '' if manual_save_flag is None else manual_save_flag
        super().__init__(name=None, parameters=[str(save_mode_flag), str(keyword), str(acquisition_save_flag), str(manual_save_flag)])
        return
