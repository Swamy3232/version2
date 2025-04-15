import math


def to_scientific_notation(x, significant_digits: int):
	"""
	Convert a number to a scientific notation with a given significant digits
	@param x: value to convert
	@type x: float
	@param significant_digits:
	@type significant_digits: int
	@return: Number in string format using scientific format with significant digits applied
	"""
	if math.isnan(x):
		return x

	x = float(x)

	if x == 0.:
		return "0." + "0"*(significant_digits-1)

	out = []

	if x < 0:
		out.append("-")
		x = -x

	e = int(math.log10(x))
	tens = math.pow(10, e - significant_digits + 1)
	n = math.floor(x/tens)

	if n < math.pow(10, significant_digits - 1):
		e = e -1
		tens = math.pow(10, e - significant_digits+1)
		n = math.floor(x / tens)

	if abs((n + 1.) * tens - x) <= abs(n * tens -x):
		n = n + 1

	if n >= math.pow(10,significant_digits):
		n = n / 10.
		e = e + 1

	m = "%.*g" % (significant_digits, n)

	if e < -2 or e >= significant_digits:
		out.append(m[0])
		if significant_digits > 1:
			out.append(".")
			out.extend(m[1:significant_digits])
		out.append('e')
		if e > 0:
			out.append("+")
		out.append(str(e))
	elif e == (significant_digits -1):
		out.append(m)
	elif e >= 0:
		out.append(m[:e+1])
		if e+1 < len(m):
			out.append(".")
			out.extend(m[e+1:])
	else:
		out.append("0.")
		out.extend(["0"]*-(e+1))
		out.append(m)

	return "".join(out)


def convert_to_significant_digits(x, digits=6):
	"""
	Convert a number using a given significant digits
	@param x: value to convert
	@type x: float
	@param digits: number of significant digits
	@type digits: int
	"""
	if x == 0 or not math.isfinite(x):
		return x
	digits -= math.ceil(math.log10(abs(x)))
	return round(x, digits)


def count_sig_figs(x):
	"""
	Count the number of significant digits in a number
	@param x: value to count
	@type x: float
	@return: number of significant digits
	"""
	str_answer = str(x).replace('.', '')
	for i in range(len(str_answer)):
		if str_answer[i] != '0':
			str_answer = str_answer[i:]
			break

	return len(str_answer)


if __name__ == '__main__':
	values = [1.2000000, 0.123456, -1.23456, 0.00123456, 0]
	for v in values:
		print('to_scientific_notation({}) = {}'.format(v, to_scientific_notation(v, 3)))
		print('convert_significant_digits({}) = {}'.format(v, convert_to_significant_digits(v, 3)))
		print('count_sigfigs({}) = {}'.format(v, count_sig_figs(str(v))))