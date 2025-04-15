

def is_idn(idn: str):
	"""
	Checks if the idn is valid
	Should be in the form of "000.111.222" or "aaa.bbb.ccc"
	"""
	if not idn:
		return False
	if len(idn.split(".")) != 3:
		return False
	return True
