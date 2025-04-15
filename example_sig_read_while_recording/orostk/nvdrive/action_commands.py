"""
This module defines all the action commands of NVDrive
See NVDrive documentation to get informations about these
actions parameters and return code.
"""
import logging

from orostk.nvdrive.generic_command import GenericCommand
from orostk.nvdrive.nvd_commands import run_action
from orostk.nvdrive.nvd_utils import get_cmd_last_error

nvdrive_logger = logging.getLogger('NVDriveLogger')


class ActionCommand(GenericCommand):
    """
    This class represents an action command:
    action that doesn't return anything
    Classes inherited from this class must be named as the NVDCommand
    (see run method)
    """

    def __init__(self, *args):
        """

        :param args: Arguments of the command
        :return:
        """
        nvdrive_logger.debug(
            'Creating a {} command'.format(self.__class__.__name__)
        )
        super().__init__()
        self.args = []
        for item in args:
            self.args.append(str(item))

    def run(self, socket):
        """ This method run the NVGate command. It shouldn't be called
        by a user, the use NVDManager.run(command) is preferable.

        :return: True if succeed, False if failed
        """
        action_cmd = self.__class__.__name__
        nvdrive_logger.info('Running command {}'.format(action_cmd))
        self.return_code = run_action(socket,
                                      action_cmd,
                                      self.args)
        if self.return_code < 0:
            self.error_code = get_cmd_last_error(socket)
            nvdrive_logger.error(
                'Command {} failed, error code {}'.format(action_cmd,
                                                          self.error_code)
            )
        else:
            nvdrive_logger.info('Command succeed')
        return self.return_code == 0


class Run(ActionCommand):
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


class Stop(ActionCommand):
    """
    Permanently stops the measurement in the process
    of acquisition (only one measurement is possible at a time),
    which can be in the « run » or « pause » mode.


    """
    pass


class Noop(ActionCommand):
    """
    No operation


    """
    pass


class Pause(ActionCommand):
    """
    If a measurement is in the process of acquisition:

        - If the measurement is in the « run » mode,
          interrupt the measurement. It then moves to the “pause” mode.
        - If the measurement is in the “pause” mode,
          continue the measurement which moves to the “run” mode.

    """
    pass


class RefreshPM(ActionCommand):
    """
    Refresh the project Manager
    """
    pass


class TransactionBegin(ActionCommand):
    """
    When connecting inputs to analyzer plug-ins and/or changing the settings,
    this command avoid sending the new configuration to the hardware
    after each modification.

    TransactionBegin must be called before sending the first configuration
    command and the command TransactionEnd must be called
    after the last configuration command.
    """
    pass


class TransactionEnd(ActionCommand):
    """
    When connecting inputs to analyzer plug-ins and/or changing the settings,
    this command avoid sending the new configuration to the hardware
    after each modification.

    TransactionBegin must be called before sending the first configuration
    command and the command TransactionEnd must be called
    after the last configuration command.
    """
    pass


class FormatDisk(ActionCommand):
    """
    Format OR3x internal disk.
    """
    pass


class Accept(ActionCommand):
    """
    Do accept the signal blocks in the FFT plug-in.
    """
    pass


class Reject(ActionCommand):
    """
    Do reject the signal blocks in the FFT plug-in.
    """
    pass


class Autorange(ActionCommand):
    """
    Do or stop the auto range according to the NVGate settings.

    optional parameters:

        - DoAutorange: 1(activated) or 0(stopped), default=1
        - MasterOrSlave: 1(master) or 2(slave), default=1
    """
    pass


class CheckICP(ActionCommand):
    """
    Do the check ICP on the channels whose coupling is ICP.

    optional parameters:

        - MasterOrSlave: 1(master) or 2(slave), default=1
    """
    pass


class CheckTEDS(ActionCommand):
    """
    Do the check TEDS on the channels whose coupling is ICP TEDS.

    optional parameters:

        - MasterOrSlave: 1(master) or 2(slave), default=1
        - Input: input number, default=0(all)
        - Silent: 0(unactivated) or 1(activated), default=1
    """
    pass


class EditCalibration(ActionCommand):
    """
    Edit the calibration’s dialog box,
    and wait for the user to click on “OK” or “Cancel”.

    """
    pass


class PlayByStep(ActionCommand):
    """
    Play by steps, available only in post-analysis,
    when the file is played by step.
    The command starts a new step or pauses the current step.

    """
    pass


class RefreshState(ActionCommand):
    """
    Refresh all NVGate status.
    """
    pass


class Shutdown(ActionCommand):
    """
    Allows the user to close the server application.

    optional parameters:

        - Save: 0(no save) 1(save), default=0

    """
    pass


class ConnectInput(ActionCommand):
    """
    Connects a front-end input (or player track, in post-analysis mode)
    to an analyzer channel.

    parameters:

        - Input number
        - Module number
        - Channel number

    """
    pass


class DisconnectInput(ActionCommand):
    """
    Disconnect a front-end input in on-line mode,
    a player track in post-analysis mode.

    optional parameters:

        - InputNumber: The input number, if not specified disconnect all inputs

    """
    pass


class ResetEvents(ActionCommand):
    """
    Initializes all the events to « not appeared ».
    """
    pass


class ResetControlPanel(ActionCommand):
    """
    Removes part of or entire control panel

    optional parameters:

        - Application: describe which part
          of the control panel has to be reset:

            - 0(default), Complete
            - 1, Active tab
            - 2, Status are
            - 3, tab defined by TabName
        - TabName: The name of the tab to reset.

    """
    pass


class SetSaveOption(ActionCommand):
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
    pass


class AddRecordMarker(ActionCommand):
    """
    Allows the user to add a record marker (during recording).
    """
    pass


class EnableOrosDrive(ActionCommand):
    pass


class ReloadCurrentWorkbook(ActionCommand):
    """
    Allows the user to reload the saved workbook of the current project.
    """
    pass


class RemoveMeasurement(ActionCommand):
    """
    Allows the user to remove project’s measurements.

    optional parameters:

        - ProjectName, if not specified: current project
        - MeasurementName, if not specified, all measurements

    """
    pass


class ResetWorkbook(ActionCommand):
    """
    Reset everything in NVGate:

        - Settings of the analyzer are set to their default value
        - Windows are destroyed
        - Control panel and Save setup are emptied

    """
    pass


class SaveProject(ActionCommand):
    """
    Allows the user to save the current project.

    optional parameters:

        - AskQuestion, 0(no interruption), 1(choices), default=0
        - AccessAllowed, 0(Administrator only), 1(All users), default=0

    """
    pass


class SaveWorkbook(ActionCommand):
    """
    Allows the user to save the current workbook.
    """
    pass


class UnloadCurrentMeasurement(ActionCommand):
    """
    Allows the user to unload the current measurement.

    optional parameters:

        - Confirmation, 0(No), 1(Yes), default=0
        - Save, 0(No), 1(Yes), default=0

    """
    pass


class ClearSetupList(ActionCommand):
    """
    Clears the save setup result list
    """
    pass


class SaveResults(ActionCommand):
    """
    Save the results that have been selected in the Save Setup in
    a new measurement.

    optional parameters:

        - ConfirmName, 0(No) 1(Yes), default=0

    """
    pass


class SetSetupParameters(ActionCommand):
    """
    Sets the parameters [Measurement database name] and [Increment type]
    of the save setup.

    optional parameters:

        - Measurement database name
        - IncrementType, 0(by number), 1(by date)

    """
    pass


class SetSettingValue(ActionCommand):
    """
    Assigns a value to a simple type (Boolean, string, scalar),
    enumerated type (enumerated), matrix type setting,
    action type, actionbis type or multisources type.

    parameters:

        - ModuleNum
        - SubModuleNum
        - SettingNum
        - Value

    """
    pass


class AddWindowResult(ActionCommand):
    """
    Creates a result window (not 3D waterfall result).

    parameters:

        - LayoutName
        - WindowName
        - ModuleNumber
        - ProcessNumber
        - ChannelNumber

    optional parameters:

        - RefChannelNumber
        - WeightingOperator
        - TimeOperator
        - DisplayUnit
        - ArrangeWindow
        - Maximize/Minimize, 0(Normal), 1(Minimize), 2(Maximize), default=0
        - 2D_WaterFall, 0(Normal), 1(2D Waterfall), default=0
        - ExistingResultIsAnError, 0(not an error), 1(considered as error)

    """
    pass


class CreateResultEx(ActionCommand):
    """
    Prepare a result to be retrieved with the command GetResultEx.

    parameters:

        - ModuleNumber
        - ProcessNumber
        - ChannelNumber

    optional parameters:

        - ReferenceChannelNumber
        - WaterfallFlag

    """
    pass


class DeleteResultEx(ActionCommand):
    """
    Delete a result created with the command CreateResultEx.

    parameters:

        - ModuleNumber
        - ProcessNumber
        - ChannelNumber

    optional parameters:

        - ReferenceChannelNumber
        - WaterfallFlag

    """
    pass


class RemoveTCPResultChannel(ActionCommand):
    """
    Allows the user to remove a TCP channel.

    parameters:

        - TCPChannelId, if -1 all TCP Channels are destroyed
    """
    pass


class ChangeTCPResultName(ActionCommand):
    """
    Change result name of a TCP result.

    parameters:

        - TCPChannelId
        - ResultName

    """
    pass


class Autoscale(ActionCommand):
    """
    Autoscale on Y axis or referenced axis of a result window.

    parameters:

        - LayoutName
        - WindowName

    optional parameters:

        - Axis, Y or Ref, default=Y
    """
    pass


class SetScaleValues(ActionCommand):
    """
    Set the min and max values of the selected scale.

    parameters:

        - WindowName
        - Min
        - Max

    optional parameters:

        - DisplayZoneType
        - Axis, 0(X), 1(Y), 2(Z), default=0
        - Lock, 0(No), 1(Yes), default=0

    """
    pass


class AddWindowWtfResult(ActionCommand):
    """
    Creates a 3D waterfall result window.
    Warning: Not for reinjected results

    parameters:

        - LayoutName
        - WindowName
        - ModuleNumber
        - ProcessNumber
        - ChannelNumber

    optional parameters:

        - RefChannelNumber
        - WeightingOperator
        - TimeOperator
        - DisplayUnit
        - ArrangeWindow
        - Maximize/Minimize, 0(Normal), 1(Minimize), 2(Maximize), default=0

    """
    pass


class ConnectToTCPClient(ActionCommand):
    """
    Creates a TCP socket connection between NVGate and a NVDrive client
    application.

    parameters:

        - IP address
        - Port number

    """
    pass


class DisconnectFromTCPClient(ActionCommand):
    """
    Disconnect NVGate from the NVDrive client
    """
    pass


class RegisterState(ActionCommand):
    """
    Register a NVDrive client application to receive notifications
    from NVGate when a state event is generated.

    parameters:

        - Module number
        - Submodule number
        - Setting number

    """
    pass


class UnregisterState(ActionCommand):
    """
    Unregister the specified state from the notification system.

    parameters:

        - Module number
        - Submodule number
        - Setting number

    """
    pass


class RegisterSetting(ActionCommand):
    """
    Register a NVDrive client application to receive notifications
    from NVGate when a setting event is generated.

    parameters:

        - Module number
        - Submodule number
        - Setting number

    """
    pass


class UnregisterSetting(ActionCommand):
    """
    Unregister the specified setting from the notification system.

    parameters:

        - Module number
        - Submodule number
        - Setting number

    """
    pass


class RegisterUINotification(ActionCommand):
    """
    Register a NVDrive client application to receive notifications
    from NVGate when a UI event is generated.

    parameters:

        - UI notification number

    optional parameter:

        - Mode

    """
    pass


class UnregisterUINotification(ActionCommand):
    """
    Unregister the specified UI from the notification system.

    parameters:

        - UI notification number

    """
    pass


class RegisterCommand(ActionCommand):
    """
    Register a NVDrive client application to receive notifications
    from NVGate when a state event is generated.

    parameters:

        - Command number

    """
    pass


class UnregisterCommand(ActionCommand):
    """
    Unregister the specified state from the notification system.

    parameters:

        - Command number

    """
    pass


class RegisterNewResult(ActionCommand):
    """
    Register a NVDrive client application to receive notifications
    from NVGate when a new result event is generated.

    parameters:

        - Module id

    """
    pass


class UnregisterNewResult(ActionCommand):
    """
    Unregister the specified new result event from the notification system.

    parameters:

        - Module id

    """
    pass


class UnblockNewResult(ActionCommand):
    """
    Unblock the specified new result transfer.

    parameters:

        - Module id

    """
    pass


class RegisterNewMeasurement(ActionCommand):
    """
    Register a NVDrive client application to receive notifications
    from NVGate when a new measurement event is generated.

    """
    pass


class UnregisterNewMeasurement(ActionCommand):
    """
    Unregister the new measurement event from the notification system.

    """
    pass


class ChangeMode(ActionCommand):
    """
    Switch between post analysis mode and normal mode

    parameters:
        - Mode: 0 normal, 1 post-analyses

    """
    pass


class LoadWorkbookModel(ActionCommand):
    """
    Allows the user to load a workbook of the workbook library.

    parameters:

        - Workbook name

    opional parameters:

        - Path
        - Save
        - Settings
        - ControlPanel
        - Layouts
        - Setup
        - Print setup


    """
    pass


class SetSignalFileSettingValue(ActionCommand):
    """
    Assigns a value to a signal file type setting.

    parameters:

        - Module
        - SubModuleNum
        - SettingNum

    optional parameters:

        - Project name
        - Measurement name
        - Perform check

    """
    pass


class AddResultToSetup(ActionCommand):
    """
    Adds a result to the save setup list

    parameters:

        - Module
        - Process number
        - Channel number

    optional parameters:

        - Reference channel number
        - Weighting operator
        - Time operator
        - Display unit
        - IsWaterfall

    """
    pass


class NewProject(ActionCommand):
    """
    Allows the user to create a new current project with a new name.

    parameters:

        - Project Name

    optional parameters:

        - Access allowed: 0(default) Administrator, 1 All users
        - Workbook
            - 0(default), empty workbook
            - 1, current workbook
            - 2, workbook model
        - Workbook model, name of the workbook momdel

    """
    pass


class LoadProject(ActionCommand):
    """
    Allows the user to load a project

    parameters:

        - Project name

    output parameters:

        - Project database name
        - Save
            - 0 load without saveing current
            - 1(default) open confirmation dialogue box

    """
    pass


class LogWarning(ActionCommand):
    """
    Allows the user to log a warning in the NVGate log window

    parameters:

        - user message to display

    """
pass

