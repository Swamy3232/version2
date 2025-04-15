from .quantity_provider import Unit


def convert_unit(value, src_unit: Unit, dst_unit: Unit = None):
    """Convert value to SI using user_unit (dict containing coeff_A and coeff_B allowing conversion from SI to
    this user unit)
    :param value: value to be converted
    :type value: int, float or list of them
    :param src_unit: source unit, it's the value unit
    :type src_unit: pynvdrive.quantity.quantity_provider.Unit class
    :param dst_unit: optional destination unit, default SI unit
    :type src_unit: pynvdrive.quantity.quantity_provider.Unit class
    """
    # TODO : Add dst_unit and reverted conversion (from SI to another)
    if not dst_unit: # Convert to SI unit
        coeff_A = src_unit.coeff_A
        coeff_B = src_unit.coeff_B

        if isinstance(value, (float, int)):
            return (value - coeff_B) / coeff_A

        elif isinstance(value, list):
            for idx, item in enumerate(value):
                data = convert_unit(value=item, src_unit=src_unit, dst_unit=dst_unit)
                value[idx] = data
            return value

        else:
            return value


