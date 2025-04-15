import os
import logging

from orostk.utils.orostk_utils import methdispatch
from orostk.utils.singleton import Singleton
from orostk.file.nvg_signal_legacy import (
    load_signal_file, close_current_signal_file,
    get_current_signal_file_idx, set_current_signal_file,
    get_current_signal_nb_tracks, get_current_signal_nb_records,
    get_current_signal_length, read_track_data_fixed,
    get_track, new_signal_file, save_signal_file, write_track
)
from orostk.file.signal_legacy import Signal
from orostk.file.nvg_result import (
    load_result_file, number_of_results, initialize_dll, number_of_systems,
    set_system_number, get_result_list, get_result_type, get_vector_type,
    create_result_file, append_result_file, save_result_file, create_scalar_result,
    fill_scalar_result, create_regvector_result, fill_regvector_result,
    create_refvector_result, extract_scalar_result, extract_regvector_result,
    extract_refvector_result, extract_waterfall_result,
    create_waterfall_result, fill_waterfall_result,
    fill_refvector_result, fill_reference_value, create_reference, set_result_range,
    get_response_idn, get_reference_idn, get_result_source_idn, get_result_setting_value,
    set_result_visibility, get_noctave
)

from orostk.file.result import (
    ScalarResult, RegVectorResult, RefVectorResult, WaterfallResult, Result
)

from orostk.file.file_exceptions import NVGateFileException
from orostk.file.file_utils import result_types
from orostk.file.file_utils import REFERENCED_VECTOR, REGULAR_VECTOR

file_logger = logging.getLogger('NVGateFileLogger')

"""
This class manages the creation of signals and results from NVGate signals and results files.
It's the Legacy version of NVGateFileManager, it uses the old NVGate DLL, it's not used anymore and will not be updated.
It's kept here for compatibility with old code. Not recommended to use it anymore.
Still valid for NVGate < 17.00, using new signal format (OSFF instead of OXF).
However, it can read OSFF files and write them, without using new capabilities of OSFF format.
"""


class NVGateFileManager(object, metaclass=Singleton):
    """
    This class manages the creation of signals and results
    from NVGate signals and results files
    It also handle how to write these files
    """

    def __init__(self):
        self.opened_signal_files = set()
        self.opened_result_files = set()
        self.read_result_in_progress = False
        file_logger.debug('Initializing DLL')
        initialize_dll()

    def read_signal(self, path, read_data=False):
        """

        :param path: The path (absolute or relative) to the .oxf file or OSFF directory
        :param read_data: If True, it will read all data of the signal file
        :return: A Signal object, None if failed
        """
        abs_path = os.path.abspath(path)
        file_logger.info('Loading file {}'.format(abs_path))
        load_signal_file(abs_path)
        current_idx = get_current_signal_file_idx()
        try:
            nb_tracks = get_current_signal_nb_tracks()
            nb_records = get_current_signal_nb_records()
            length = get_current_signal_length()
            tracks = []
            for track_idx in range(1, nb_tracks + 1):
                track = get_track(track_idx, read_data)
                tracks.append(track)

            sig = Signal(nb_records=nb_records, tracks=tracks, length=length)
            sig.file_idx = current_idx
        except NVGateFileException:
            close_current_signal_file()
            sig = None
        else:
            if read_data:
                close_current_signal_file()
                sig.file_idx = None
            else:
                self.opened_signal_files.add(current_idx)
        return sig

    def read_signal_track_data(self, signal, record_number,
                               track_idx, begin, end):
        """ Read only a fixed number of samples of a signal track
         in a signal file.

        :param signal: The signal containing the track
        :param record_number: id of the record (starting at 0)
        :param track_idx: The index of the track in the signal
        :param begin: First sample to read
        :param end: Last sample to read
        :return: An array of samples (floating values)
        """
        file_logger.debug('Reading data from sample'
                          ' {} to sample {}'.format(begin, end))
        if signal.file_idx is None:
            raise NVGateFileException('This Signal is not attached to a file'
                                      ', unable to read its data.\n'
                                      'Did you read the whole signal ?')
        elif begin >= end:
            raise IndexError('Begin sample has to be smaller than end sample')
        elif track_idx >= len(signal.tracks):
            raise IndexError("Track index doesn't exist in this Signal")
        elif begin >= signal.tracks[track_idx].nb_samples:
            raise IndexError('Begin sample is higher than the number'
                             ' of samples')

        if end > signal.tracks[track_idx].nb_samples:
            end = signal.tracks[track_idx].nb_samples
        current_idx = get_current_signal_file_idx()
        set_current_signal_file(signal.file_idx)
        data = read_track_data_fixed(track_idx + 1, record_number,
                                     begin, end)
        set_current_signal_file(current_idx)
        return data

    def write_signal(self, signal, path):
        """

        :param signal: The signal to write
        :param path:  The path to the file to create
        :return: True if succeed, else false
        """
        if signal.file_idx is not None:
            self.close_signal_file(signal.file_idx)
        abs_path = os.path.abspath(path)
        file_logger.info('Writing file {}'.format(abs_path))
        if signal.nb_frequencies != 1:
            raise NVGateFileException("""Can't create a signal file\
                with tracks of different frequencies""")
        elif len(signal.tracks_type) != 1:
            raise NVGateFileException(
                "Can't create a signal file with tracks of different type")
        if not os.path.exists(os.path.dirname(abs_path)):
            os.makedirs(os.path.dirname(abs_path))
        new_signal_file(abs_path, signal, signal.tracks[0].frequency,
                        signal.tracks[0].track_type[0])
        file_logger.debug('Writing tracks')
        for track_idx in range(len(signal.tracks)):
            write_track(track_idx + 1, signal.tracks[track_idx])
        save_signal_file()
        file_logger.info('File {} saved'.format(abs_path))
        return True

    def close_signal_file(self, file_idx):
        """

        :param file_idx: The index of the file to close
        """
        file_logger.debug('Closing file index {}'.format(file_idx))
        current_idx = None
        if len(self.opened_signal_files) >= 1:
            current_idx = get_current_signal_file_idx()
        else:
            current_idx = -1
        set_current_signal_file(file_idx)
        close_current_signal_file()
        self.opened_signal_files.remove(file_idx)
        if current_idx != file_idx:
            set_current_signal_file(current_idx)

    def close_all_signal_files(self):
        file_logger.debug('Closing all files')
        for file_idx in list(self.opened_signal_files):
            self.close_signal_file(file_idx)

    def read_results(self, path, callback_post=None):
        """

        :param path: The path (absolute or relative) to the .res file
        :param callback_post: callback called after every read result with self and read_result parameter
        :return: A list of results
        """       
        
        self.read_result_in_progress = True
        
        abs_path = os.path.abspath(path)
        file_logger.info('Loading file {}'.format(abs_path))
        load_result_file(abs_path)
        result_list = []
        for sys_id in range(number_of_systems()):
            set_system_number(sys_id)
            size = number_of_results()
            result_dict_list = get_result_list(sys_id, size)
            for res in result_dict_list:
                extracted_result = self._extract_result(res)
                result_list.append(extracted_result)
                
                if callback_post != None:
                    callback_post(self, extracted_result)
        
        self.read_result_in_progress = False
        return result_list

    def _extract_result(self, res_dict):
        """ Create a Result object from a result file

        :param res_dict: A dictionary describing a result
        :return: a Result
        """
        file_logger.debug('Extracting result number {}'.format(
            res_dict['res_id'])
        )
        res_type = get_result_type(res_dict['res_id'])
        res = None

        process_id = res_dict['res_type']

        if result_types[res_type] == 'Scalar':
            file_logger.debug('Extracting a scalar result')
            res = extract_scalar_result(res_dict)
        elif result_types[res_type] == 'RealVector' or (
                    result_types[res_type] == 'ComplexVector'):
            type = get_vector_type(res_dict['res_id'])

            if type == REGULAR_VECTOR:
                file_logger.debug('Extracting a regular vector')
                res = extract_regvector_result(
                    res_dict,
                    result_types[res_type] == 'ComplexVector'
                )
            elif type == REFERENCED_VECTOR:
                if process_id in [18, 24, 132, 133, 183]:
                    file_logger.debug('Extracting an octave regular vector')
                    res = extract_regvector_result(
                        res_dict,
                        result_types[res_type] == 'ComplexVector'
                    )
                else:
                    file_logger.debug('Extracting a referenced vector')
                    res = extract_refvector_result(
                        res_dict,
                        result_types[res_type] == 'ComplexVector'
                    )
            else:
                raise NVGateFileException('Unknown Vector type')

        elif result_types[res_type] == 'RealWaterfall' or (
                    result_types[res_type] == 'ComplexWaterfall'):
            res = extract_waterfall_result(
                res_dict,
                result_types[res_type] == 'ComplexWaterfall'
            )
            
        res.result_id = res_dict['res_id']
        res.config.response_idn = get_response_idn(res.result_id)
        res.config.reference_idn = get_reference_idn(res.result_id)
        
        return res

    def write_results(self, results, path):
        """ Write a list of result in a file

        :param results: List of results to write
        :param path: Result file path
        """
        file_id = self.create_result_file()
        for result in results:
            self.create_result(result, file_id, 0)
        self.save_result_file(file_id, path)

    def create_result_file(self):
        """ Create a result file

        :return: Result file id
        """
        return create_result_file()

    def append_result_file(self, path):
        """ Switch to append mode for a result file

        :return: Result file id
        """
        return append_result_file(path)

    def save_result_file(self, file_id, path):
        """ Save a result file on disk

        :param file_id:
        :param path:
        """
        abs_path = os.path.abspath(path)
        file_logger.info('Writing file {}'.format(abs_path))
        save_result_file(file_id, abs_path)

    def get_source_idn(self, result, submodule_idn, store=False):
        """ Returns the source idn of submodule idn

        :param result: Read result
        :param submodule_idn: submodule channel idn
        :param store: if it is True, store the returned idn in a "source_idn" dictionary of result
        :return: idn string value
        :raises: NVGateFileException exception if it is not called by a callback during NVGateFileManager::read_results
        """
        if self.read_result_in_progress:
            if isinstance(result, Result):
                set_system_number(result.system_id)
                source = get_result_source_idn(submodule_idn)
                if store:
                    result.source_idn[submodule_idn] = source
                return source
            else:
                raise NVGateFileException('Error calling get_source_idn : bad result parameter type')
        else:
            raise NVGateFileException('Error calling get_source_idn : read_results is not in progress')

    def get_setting_value(self, result_or_signal, setting_idn, store=False):
        """ Returns the value of an setting idn

        :param result: Result or signal
        :param setting_idn: setting idn
        :param store: if it is true, store the returned value in a "setting_value" dictionary of result_or_signal
        :return: setting value according to the setting type (string, float, ...)
        :raises: NVGateFileException exception if it is not called by a callback during NVGateFileManager::read_results
        """
        if self.read_result_in_progress:
            if isinstance(result_or_signal, Result):
                set_system_number(result_or_signal.system_id)
                value = get_result_setting_value(setting_idn)
                if store:
                    result_or_signal.setting_value[setting_idn] = value
                return value
            else: # isinstance(result_or_signal, Signal):
                raise NVGateFileException('Error calling get_source_idn : bad result parameter type')
        else:
            raise NVGateFileException('Error calling get_setting_value : read_results is not in progress')

    def add_wtf_reference(self, reference, date, file_id, system_id):
        """

        :param reference: Waterfall reference to write (see orostk.file.reference)
        :param date: Date of the first value
        :param file_id: Id of the file we want to write the result
        :param system_id:
        """
        if reference.quantity_key == 'Slice_Number':
            # The creation of Referenced vector
            # automatically create a slice_number reference
            return -1
        
        # reference values must be in SI unit
        reference_SI = reference.get_SI()
        
        # process_id and submoduleReference parameters are no longer used in Toolkit C
        ref_id = create_reference(file_id, system_id, date, reference_SI)
        for i, val in enumerate(reference_SI.data):
            fill_reference_value(ref_id, val, i)
        return ref_id
        
    def set_result_range(self, result, axis, min, max):
        """

        Set the result range on a specified axis direction
        :param result: Result
        :param axis: 0 for X axis, 1 for Y axis and 2 for Z axis
        """
        return set_result_range(result.result_id, axis, min, max)

    def set_result_visibility(self, result, visible):
        """

        Set the result visibility through NVGate, by default the result is visible
        :param result: Result
        :param visible: 0 for invisible, 1 for visible
        """
        return set_result_visibility(result.result_id, visible)

    @methdispatch
    def create_result(self, result, file_id, system_id):
        """

        :param result: Result to write
        :param file_id: Id of he file where we want to write the result
        :param system_id:
        """
        raise NVGateFileException('Unknown result type')

    @create_result.register(ScalarResult)
    def _(self, result: ScalarResult, file_id, system_id):
        file_logger.debug('Creating a scalar result')
        if not result.is_SI():
            raise NVGateFileException('The result quantity is not in SI')
        result_id = create_scalar_result(file_id, system_id, result)
        result.result_id = result_id
        fill_scalar_result(result)

    @create_result.register(RegVectorResult)
    def _(self, result: RegVectorResult, file_id, system_id):
        file_logger.debug('Creating a regular vector result')
        if not result.is_SI():
            raise NVGateFileException('The result quantity is not in SI')
        result_id = create_regvector_result(file_id, system_id, result)
        result.result_id = result_id
        fill_regvector_result(result)

    @create_result.register(RefVectorResult)
    def _(self, result: RefVectorResult, file_id, system_id):
        file_logger.debug('Creating a referenced vector result')
        if not result.is_SI():
            raise NVGateFileException('The result quantity or one of its'
                                      ' references is not in SI')
        result_id = create_refvector_result(file_id, system_id, result)
        result.result_id = result_id
        for ref in result.references:
            self.add_wtf_reference(ref, result.date, file_id, system_id)
            
        for i, val in enumerate(result.y_data):
            fill_refvector_result(result.result_id, val, i)

    @create_result.register(WaterfallResult)
    def _(self, result: WaterfallResult, file_id, system_id):
        file_logger.debug('Creating a waterfall result')
        if not result.is_SI():
            raise NVGateFileException('The result quantity or one of its'
                                      ' references is not in SI')
        result_id = create_waterfall_result(file_id, system_id, result)
        result.result_id = result_id
        for ref in result.references:
            self.add_wtf_reference(ref, result.date, file_id, system_id)
            
        for num_slice in range(result.depth):
            fill_waterfall_result(result, num_slice)

    def __del__(self):
        self.close_all_signal_files()
