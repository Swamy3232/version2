def quote_escape_str(value, quoted=True):
	"""Quote and escape characters of NVDrive commands parameters

    :param value:  String to escape
        :param quoted: Is string need to be surrounded by quote
    :type quoted: boolean
    :return: UTF-8 bytes
    """
	unquoted_escaped = value.encode('utf-8').replace(b'\\', b'\\\\')
	unquoted_escaped = unquoted_escaped.replace(b'"', b'\\"')
	if quoted:
		return b'"' + unquoted_escaped + b'"'
	else:
		return unquoted_escaped


def quote_escape_byte(byte):
	unquoted_escaped = byte.replace(b'\\', b'\\\\')
	unquoted_escaped = unquoted_escaped.replace(b'"', b'\\"')
	return unquoted_escaped


def quote_escape_list(list, quoted=True):
	"""Quote and escape characters of NVDrive commands parameters

    :param list:  List of string to escape
    :param quoted: Is string need to be surrounded by quote
    :type quoted: boolean
    :return: list UTF-8 bytes
    """
	result = []
	for value in list:
		result.append(quote_escape(value, quoted))
	return result


def quote_escape(value, quoted=True):
	"""Quote and escape characters of NVDrive commands parameters

    :param value:  String or list to escape
        :param quoted: Is string need to be surrounded by quote
    :type quoted: boolean
    :return: UTF-8 bytes
    """
	if isinstance(value, list):
		return quote_escape_list(value)
	else:
		return quote_escape_str(value, quoted)


def convert_parameters_none(list_parameters):
	new_lists = []
	for param in list_parameters:
		if param == 'None':
			new_lists.append('')
		else:
			new_lists.append(param)
	return new_lists
