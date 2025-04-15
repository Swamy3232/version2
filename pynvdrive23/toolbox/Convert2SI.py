def Convert2SI(value, user_unit=None):
    """
    Convert value to SI using user_unit (dict containing coeff_A and coeff_B allowing conversion from SI to this user unit)
    """

    coeff_A = user_unit['coeff_A']
    coeff_B = user_unit['coeff_B']

    if isinstance(value, (float, int)):
        return (value - coeff_B) / coeff_A

    elif isinstance(value, list):
        for idx, item in enumerate(value):
            data = Convert2SI(value=item, user_unit=user_unit)
            value[idx] = data
        return value

    else:
        return value
