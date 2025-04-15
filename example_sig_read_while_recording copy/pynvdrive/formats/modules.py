"""
This module define all modules names associated to modules id
"""

# Modules names, associated to modules id, named as in NVGate idn
modules = {
	1: 'frontend',
	2: 'monitor',
	3: 'recorder',
	4: 'player',
	5: 'event',
	6: 'tachometer',
	7: 'generator',
	8: 'filter',
	9: 'weightingwindow',
	10: 'fft1',
	11: 'fft2',
	12: 'cpb',
	14: 'soa1',
	16: 'waterfall',
	17: 'soa2',
	18: 'fft3',
	19: 'fft4',
	21: 'ova',
	22: 'tda',
	498: 'tcp'
}

# Alternative name of modules, for display purpose
modules_alternative_names = {
	'cpb': 'oct'
}

modules_names_dict = {v: k for k, v in modules.items()}
