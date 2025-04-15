"""
This package provides features about manipulating
NVGate result and signal files.
"""
import logging
import locale

file_logger = logging.getLogger('NVGateFileLogger')
file_handler = logging.StreamHandler()
file_formatter = logging.Formatter(
    '%(asctime)s %(name)-12s %(levelname)-8s %(message)s'
)
file_handler.setFormatter(file_formatter)
file_logger.addHandler(file_handler)
file_logger.setLevel(logging.WARNING)

