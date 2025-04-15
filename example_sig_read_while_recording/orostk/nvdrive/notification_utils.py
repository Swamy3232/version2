from orostk.idn import Idn

command_id = {
    'run': 0,
    'pause': 1,
    'stop': 2,
    'accept': 3,
    'reject': 4,
    'manual_trigger': 5,
    'player_pause': 6
}

id_to_command = {
    0: 'run',
    1: 'pause',
    2: 'stop',
    3: 'accept',
    4: 'reject',
    5: 'manual_trigger',
    6: 'player_pause'
}

# These masks help to decrypt a module/submodule encoded in a UINT
UINT_MASK_VERSION = 0xFC000000
UINT_MASK_COLLECTION = 0x03FF0000
UINT_MASK_INDEX = 0x0000FFFF


def uint_idn_to_idn(module_uint, submodule_uint, setting):
    s_m_index = submodule_uint & UINT_MASK_INDEX
    s_m_collection = (submodule_uint & UINT_MASK_COLLECTION) >> 16
    m_index = module_uint & UINT_MASK_INDEX
    m_collection = (module_uint & UINT_MASK_COLLECTION) >> 16

    s_m = '{}:{}'.format(s_m_collection, s_m_index)
    m = m_collection
    idn = Idn(module=m)
    if idn.module[-1] == str(m_index):
        m_index = ''
    m_string = '{}{}'.format(idn.module, m_index)
    complete_idn = Idn(module=m_string, submodule=s_m)
    complete_idn.setting_id = setting
    return complete_idn
