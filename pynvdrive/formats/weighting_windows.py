"""
This module define all weighting window names associated to weighting window id
"""

weighting_windows = {
	316: 'WW_UNIFORM',
	333: 'WW_HANNING',
	334: 'WW_HAMMING',
	335: 'WW_KAISER_BESSEL',
	336: 'WW_FLATTOP',
	337: 'WW_EXPONENTIAL'
}

weighting_windows_names = {v: k for k, v in weighting_windows.items()}

weighting_windows_enbw = {
	316: 1,
	333: 1.5,
	334: 1.36,
	335: 1.8,
	336: 3.77,
	337: 1  # TODO : TBD
}
