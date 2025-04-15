from datetime import datetime, timedelta

# Windows EPOCH: timestamp from 1601-1-1 in 100-nanoseconds
W_EPOCH = datetime(1601, 1, 1)


def datetime_to_windows_time(date):
    if date is None:
        return 0, 0
    time_sec = (date - W_EPOCH).total_seconds()
    # convert to 100-nanoseconds
    t = int(time_sec * 10e6)
    # extract higher part
    high = t >> 32
    # extract lower_part
    low = t & 0xFFFFFFFF
    return high, low


def datetime_to_windows_time_int(date):
    h, l = datetime_to_windows_time(date)
    date = (h << 32) + l
    return date


def windows_time_to_datetime(low, high):
    # We receive in 100-nano and we convert to miliseconds
    w_time = (high << 32) + low
    delta = timedelta(microseconds=w_time/10)
    return W_EPOCH + delta


def windows_time_to_datetime_int(w_time):
    delta = timedelta(microseconds=w_time / 10)
    return W_EPOCH + delta


def date_string_to_datetime(date_str):
    """
    Return datetime from a given date in the str format: 2018-01-01T00:00:00.000Z from OSFF format

    :param date_str: the date string
    :type date_str: str
    :return: the datetime
    """
    return datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S.%fZ")
