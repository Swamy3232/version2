from orostk.idn.oros_idn import idn_to_legacy, legacy_to_idn


class Idn(object):
    """
    This class represents a NVGate IDN,
    it's used to convert legacies IDN to new IDNs
    in order to call old NVGate functions that use legacies IDN
    """
    def __init__(self, module, submodule=None, setting=None, analyzer=None):
        """

        :param module:
        :type module: str or int for legacy
        :param submodule:
        :type submodule: str or int for legacy
        :param setting:
        :type setting: str or int for legacy
        :param analyzer:
        :type analyzer: str
        """
        if isinstance(module, int):
            self._analyzer = None
            self._module = None
            self._submodule = None
            self._setting = None
            self._module_id = module
            self._submodule_id = submodule
            self._setting_id = setting
            self._load_idn()
        else:
            self._analyzer = analyzer
            self._module = module
            self._submodule = submodule
            self._setting = setting
            self._module_id = None
            self._submodule_id = None
            self._setting_id = None
            self._load_legacy()

    @property
    def analyzer(self):
        return self._analyzer if self._analyzer is not None else ''

    @analyzer.setter
    def analyzer(self, analyzer):
        self._analyzer = analyzer
        self._load_legacy()

    @property
    def module(self):
        return self._module if self._module is not None else ''

    @module.setter
    def module(self, module):
        self._module = module
        self._load_legacy()

    @property
    def submodule(self):
        return self._submodule if self._submodule is not None else ''

    @submodule.setter
    def submodule(self, submodule):
        self._submodule = submodule
        self._load_legacy()

    @property
    def setting(self):
        return self._setting if self._setting is not None else ''

    @setting.setter
    def setting(self, setting):
        self._setting = setting
        self._load_legacy()

    @property
    def module_id(self):
        return self._module_id

    @module_id.setter
    def module_id(self, module_id):
        self._module_id = module_id
        self._load_idn()

    @property
    def submodule_id(self):
        return self._submodule_id

    @submodule_id.setter
    def submodule_id(self, submodule_id):
        self._submodule_id = submodule_id
        self._load_idn()

    @property
    def setting_id(self):
        return self._setting_id

    @setting_id.setter
    def setting_id(self, setting_id):
        self._setting_id = setting_id
        self._load_idn()

    def __str__(self):
        idn_tab = []
        if self._analyzer is not None:
            idn_tab.append(str(self.analyzer))
        if self._module is not None:
            idn_tab.append(str(self.module))
        if self._submodule is not None:
            idn_tab.append(str(self.submodule))
        if self._setting is not None:
            idn_tab.append(str(self.setting))
        return '.'.join(idn_tab)

    def _load_legacy(self):
        """ Fulfill the attributes *_id thanks
        to OROSIdn
        """
        module, submodule, setting = idn_to_legacy(str(self))
        self._module_id = module
        self._submodule_id = submodule
        self._setting_id = setting

    def _load_idn(self):
        """
        Fullfill the attributes module, submodule, setting
        """
        module, submodule, setting = legacy_to_idn(self.module_id,
                                                   self.submodule_id,
                                                   self.setting_id)
        self._module = module
        self._submodule = submodule
        self._setting = setting
