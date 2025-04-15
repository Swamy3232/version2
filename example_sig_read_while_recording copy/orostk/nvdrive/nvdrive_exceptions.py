"""
this module defines custom exception class for nvdrive package
"""


class CommandFailException(BaseException):
    """
    This exception should be raised when a command fail
    """
    pass


class IncompleteResultException(BaseException):
    """
    This exception should be raised when we serialize an
    incomplete Result
    """
    pass


class IncompleteBlockException(BaseException):
    """
    This exception should be raised when we serialize an
    incomplete block
    """
    pass


class TCPResultChannelException(BaseException):
    """
    This exception should be raised when we fail to retrieve
    an information from a TCPResultChannel
    """
    pass


class BlockReadException(BaseException):
    """
    This exception should be raised when we fail to read an information
    from a block
    """
    pass


class BadResultException(BaseException):
    """
    This exception should be raised when a value is not valid in a result.
    """
    pass


class NotificationBlockException(BaseException):
    """
    This exception should be raise when a notification block is not consistent
    """
    pass


class NotificationTimeoutException(BaseException):
    """
    This exception should be raised when a timeout on notification
    retrieving occurs.
    """
    pass


class NotificationTypeException(BaseException):
    """
    This exception should be raise when a bad notification type is passed
    to a function
    """
    pass


class NotificationException(BaseException):
    """
    This exception is a generic exception for a notification error
    """
    pass
