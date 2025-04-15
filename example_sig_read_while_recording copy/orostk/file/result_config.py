class ResultConfig(object):
    """
    This class represents the configuration of a result,
    it contains all the information that are not result specific
    but NVGate specific
    """
    def __init__(self, process_type, process_caption, num_analysis, analysis_caption,
                 num_response, response_name, num_window, response_idn = None, reference_idn = None):
        """

        :param process_type: Process ID of the result (see documentation)
        :param process_caption:
		:param num_analysis:
        :param analysis_caption:
        :param num_response: Channel of the response [1-32]
        :param response_name:
        :param num_window:
        :param response_idn: response idn, don't fill it by hand
        :param reference_idn: reference idn, don't fill it by hand 
        """
        self.process_type = process_type
        self.num_analysis = num_analysis
        self.num_response = num_response
        self.process_caption = process_caption
        self.analysis_caption = analysis_caption
        self.response_name = response_name
        self.num_window = num_window
        self.response_idn = None
        self.reference_idn = None

class ScalarConfig(ResultConfig):
    """
    This class represents the configuration of a scalar result

    Example::

        conf = ScalarConfig(process_type=108,
                            num_analysis=10,
                            num_response=1,
                            min_val=0.0,
                            max_val=1.0)

    """
    def __init__(self, process_type, num_analysis, num_response, min_val, max_val,
                 process_caption='', analysis_caption='', response_name='',
                 num_window=316, abs_precision=1e-6, rel_precision=1e-6):
        """

        :param process_type: Process ID of the result (see documentation)
        :param num_analysis: Module number
        :param num_response: Channel of the response [1-32]
        :param min_val:
        :param max_val:
        :param process_caption:
        :param analysis_caption:
        :param response_name:
        :param num_window:
        :param abs_precision:
        :param rel_precision:
        """
        super().__init__(process_type, process_caption, num_analysis, analysis_caption,
                         num_response, response_name, num_window)
        self.min_val = min_val
        self.max_val = max_val
        self.abs_precision = abs_precision
        self.rel_precision = rel_precision


class RegVectorConfig(ResultConfig):
    """
    This class represents the configuration of a regular vector result

        Example::

            config =  RegVectorConfig(process_type=2,
                                      num_analysis = 10
                                      process_caption='AvSpc',
                                      analysis_caption='FFT1',
                                      response_name='[1]-Input 1',
                                      num_response=1)

    """
    def __init__(self, process_type, num_analysis, num_response,
                 process_caption='', analysis_caption='', response_name='',
                 num_window=316, x_abs_precision=1e-6, x_rel_precision=1e-6,
                 y_abs_precision=1e-6, y_rel_precision=1e-6):
        """

        :param process_type: Process ID of the result (see documentation)
        :param num_analysis: Module number
        :param num_response: Channel of the response [1-32]
        :param process_caption:
        :param analysis_caption:
        :param response_name:
        :param num_window:
        :param x_abs_precision:
        :param x_rel_precision:
        :param y_abs_precision:
        :param y_rel_precision:

        """
        super().__init__(process_type, process_caption, num_analysis, analysis_caption,
                         num_response, response_name, num_window)
        self.x_abs_precision = x_abs_precision
        self.x_rel_precision = x_rel_precision
        self.y_abs_precision = y_abs_precision
        self.y_rel_precision = y_rel_precision


class RefVectorConfig(ResultConfig):
    """
    This class represents the configuration of a referenced vector result

    Example::

        conf = RefVectorConfig(process_type=108,
                               num_analysis = 10
                               num_response=1,
                               reference_submodule=1)

    """
    def __init__(self, process_type, num_analysis, num_response, reference_submodule,
                 num_reference=-1, reference_name='',
                 process_caption='', analysis_caption='', response_name='',
                 num_window=316, x_abs_precision=1e-6, x_rel_precision=1e-6,
                 y_abs_precision=1e-6, y_rel_precision=1e-6):
        """

        :param process_type: Process ID of the result (see documentation)
        :param num_analysis: Module number
        :param num_response: Channel of the response [1-32]
        :param reference_submodule: reference submodule id
        :param num_reference: id of the reference channel [1-32]
        :param reference_name:
        :param process_caption:
        :param analysis_caption:
        :param response_name:
        :param num_window:
        :param x_abs_precision:
        :param x_rel_precision:
        :param y_abs_precision:
        :param y_rel_precision:
        """
        super().__init__(process_type, process_caption, num_analysis, analysis_caption,
                         num_response, response_name, num_window)
        self.reference_submodule = reference_submodule
        self.x_abs_precision = x_abs_precision
        self.x_rel_precision = x_rel_precision
        self.y_abs_precision = y_abs_precision
        self.y_rel_precision = y_rel_precision
        self.num_reference = num_reference
        self.reference_name = reference_name


class WaterfallConfig(ResultConfig):
    """
    This class represents the configuration of a waterfall result

    Example::

        conf = WaterfallConfig(process_type=187,
                               num_analysis = 10
                               process_caption='AvSpc',
                               analysis_caption='FFT1',
                               response_name='[1]-Input 1',
                               num_response=1, reference_submodule=1)

    """
    def __init__(self, process_type, num_analysis, num_response, reference_submodule,
                 num_reference=-1, reference_name='',
                 process_caption='', analysis_caption='', response_name='',
                 num_window=316, x_abs_precision=1e-6, x_rel_precision=1e-6,
                 y_abs_precision=1e-6, y_rel_precision=1e-6,
                 z_abs_precision=1e-6, z_rel_precision=1e-6):
        """

        :param process_type: Process ID of the result (see documentation)
        :param num_analysis: Module number
        :param num_response: Channel of the response [1-32]
        :param reference_submodule: reference submodule id
        :param num_reference: id of the reference channel [1-32]
        :param reference_name:
        :param process_caption:
        :param analysis_caption:
        :param response_name:
        :param num_window:
        :param x_abs_precision:
        :param x_rel_precision:
        :param y_abs_precision:
        :param y_rel_precision:
        :param z_abs_precision:
        :param z_rel_precision:
        """
        super().__init__(process_type, process_caption, num_analysis, analysis_caption,
                         num_response, response_name, num_window)
        self.reference_submodule = reference_submodule
        self.x_abs_precision = x_abs_precision
        self.x_rel_precision = x_rel_precision
        self.y_abs_precision = y_abs_precision
        self.y_rel_precision = y_rel_precision
        self.z_abs_precision = z_abs_precision
        self.z_rel_precision = z_rel_precision
        self.num_reference = num_reference
        self.reference_name = reference_name
