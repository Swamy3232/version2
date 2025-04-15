"""
This package provides features about manipulating
NVGate thanks to NVDrive commands.
"""
import logging
import locale

nvdrive_logger = logging.getLogger('NVDriveLogger')
nvdrive_handler = logging.StreamHandler()
nvdrive_formatter = logging.Formatter(
    '%(asctime)s %(name)-12s %(levelname)-8s %(message)s'
)
nvdrive_handler.setFormatter(nvdrive_formatter)
nvdrive_logger.addHandler(nvdrive_handler)
nvdrive_logger.setLevel(logging.WARNING)


read_encoding = locale.getpreferredencoding()
write_encoding = locale.getpreferredencoding()
