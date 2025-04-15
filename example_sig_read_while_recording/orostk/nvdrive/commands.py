"""
This module is an interface for the user to gather all available commands
"""
# flake8: noqa
from orostk.nvdrive.action_commands import (
    Run,
    Stop,
    Noop,
    Pause,
    RefreshPM,
    TransactionBegin,
    TransactionEnd,
    FormatDisk,
    Accept,
    Reject,
    Autorange,
    CheckICP,
    CheckTEDS,
    EditCalibration,
    PlayByStep,
    RefreshState,
    Shutdown,
    DisconnectInput,
    ResetEvents,
    ResetControlPanel,
    SetSaveOption,
    AddRecordMarker,
    EnableOrosDrive,
    ReloadCurrentWorkbook,
    RemoveMeasurement,
    ResetWorkbook,
    SaveProject,
    SaveWorkbook,
    UnloadCurrentMeasurement,
    ClearSetupList,
    SaveResults,
    SetSetupParameters,
    SetSettingValue,
    AddWindowResult,
    CreateResultEx,
    DeleteResultEx,
    RemoveTCPResultChannel,
    ChangeTCPResultName,
    Autoscale,
    SetScaleValues,
    AddWindowWtfResult,
    ChangeMode,
    ConnectInput,
    LoadWorkbookModel,
    SetSignalFileSettingValue,
    AddResultToSetup,
    NewProject,
    LoadProject,
    LogWarning,
    UnblockNewResult,
    UnregisterNewResult,
    UnregisterUINotification,
    UnregisterCommand,
    UnregisterNewMeasurement,
    UnregisterState,
    UnregisterSetting,
    RegisterUINotification,
    RegisterCommand,
    RegisterNewMeasurement,
    RegisterSetting,
    RegisterNewResult,
    RegisterState,
    DisconnectFromTCPClient
)

from orostk.nvdrive.file_commands import ImportFile

from orostk.nvdrive.reinject_commands import (
    CreateTCPResultChannel, AddDataToTCPResultChannel, SetTCPResultChannel, NewDataForTCPResultChannel
)
from orostk.nvdrive.result_commands import GetResult, GetSavedResult

from orostk.nvdrive.setting_commands import(
    GetSettingValue, GetSettingPossibleValues
)
