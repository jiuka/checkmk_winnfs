import os
import re
import imp
import pytest

@pytest.fixture
def check(request):
    return CheckTest(request)

class CheckTest(object):
    def __init__(self, request):
        self.request = request
        self.__set_name()
        self.__load_check()

    @property
    def name(self):
        return self.module.check_info

    def parse(self):
        assert self._name in self.module.check_info, "No check named '%s' defined" % self._name
        assert 'parse_function' in self.module.check_info[self._name], "Check %s has no parse_function" % self._name

        return self.module.check_info[self._name]['parse_function'](self.__get_agent_output())

    def inventory(self):
        assert self._name in self.module.check_info, "No check named '%s' defined" % self._name
        assert 'inventory_function' in self.module.check_info[self._name], "Check %s has no inventory_function" % self._name

        return list(self.module.check_info[self._name]['inventory_function'](self.__get_parsed()))

    def check(self, item, params={}):
        p = {}
        if 'default_levels_variable' in self.check_info:
            p.update(self.factory_settings)
        p.update(params)

        return list(self.module.check_info[self._name]['check_function'](item, p,self.__get_parsed()))

    @property
    def check_info(self):
        return self.module.check_info[self._name]

    @property
    def factory_settings(self):
        return self.module.factory_settings[self.check_info['default_levels_variable']]

    def __get_agent_output(self):
        info = self.__getattr('AGENT')
        info = info.splitlines(False)

        section = None
        sep = None
        output = []


        for line in info:
            if re.match(r'^<<<[^<>]+>>>$', line):
                section = line[3:-3].split(':')[0]
                if re.match(r'.+:sep\((\d+)\)(?::|>>>$)', line):
                    sep = chr(int(re.match(r'.+:sep\((\d+)\)(?::|>>>$)', line).group(1)))
                else:
                    sep = None
                continue
            if not section == self._name:
                continue
            if line == '':
                continue
            output.append(line.split(sep))
        return output

    def __get_parsed(self):
        if 'parse_function' in self.module.check_info[self._name]:
            return self.module.check_info[self._name]['parse_function'](self.__get_agent_output())
        else:
            return self.__get_agent_output()

    def __set_name(self):
        self._name = self.__getattr('test_for')
        if not self._name:
            return

        if self.request.module.__name__.startswith('test_'):
            self._name = self.request.module.__name__[5:]
            return

        raise pytest.UsageError('Please specify the check to test with "test_for = \'my_check\'" at module level.')

    def __load_check(self):
        path = os.path.join('checks', self._name)

        if not os.path.exists(path):
            raise MissingFileError(path)

        source = open(path, 'r').read()
        code = compile(source, path, 'exec')
        module = imp.new_module(self._name)

        exec(self._HEADER, module.__dict__)
        exec(code, module.__dict__)

        self.module = module

    def __getattr(self, attr):
        if self.request.cls and attr in self.request.cls:
            return getattr(self.request.cls, attr)
        return getattr(self.request.module, attr, None)

    _HEADER = '''
import sys, os, time, socket, re
def regex(r):
    __tracebackhide__ = True
    import re
    try:
        rx = re.compile(r)
    except Exception as e:
        raise AssertionError("Invalid regular expression '%s': %s" % (r, e))
    return rx
# The following data structures will be filled by the checks
check_info                         = {} # all known checks
checkgroup_of                      = {} # groups of checks with compatible parametration
check_includes                     = {} # library files needed by checks
precompile_params                  = {} # optional functions for parameter precompilation, look at df for an example
check_default_levels               = {} # dictionary-configured checks declare their default level variables here
factory_settings                   = {} # factory settings for dictionary-configured checks
check_config_variables             = [] # variables (names) in checks/* needed for check itself
snmp_info                          = {} # whichs OIDs to fetch for which check (for tabular information)
snmp_scan_functions                = {} # SNMP autodetection
active_check_info                  = {} # definitions of active "legacy" checks
special_agent_info                 = {}

def saveint(i):
    # type: (Any) -> int
    """Tries to cast a string to an integer and return it. In case this
    fails, it returns 0.
    Advice: Please don't use this function in new code. It is understood as
    bad style these days, because in case you get 0 back from this function,
    you can not know whether it is really 0 or something went wrong."""
    try:
        return int(i)
    except (TypeError, ValueError):
        return 0


def savefloat(f):
    # type: (Any) -> float
    """Tries to cast a string to an float and return it. In case this fails,
    it returns 0.0.
    Advice: Please don't use this function in new code. It is understood as
    bad style these days, because in case you get 0.0 back from this function,
    you can not know whether it is really 0.0 or something went wrong."""
    try:
        return float(f)
    except (TypeError, ValueError):
        return 0.0
'''
