import pynvdrive


def is_nvgate(client: pynvdrive.Client = None):
	"""
	is_nvgate
	:return: True if NVGate is running
	"""
	if client is None:
		client = pynvdrive.Client()
		client.socket.settimeout(1)
	return client.connect()
