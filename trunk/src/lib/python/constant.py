#!/usr/bin/python -B

import sys

class _constant:
    class ConstantValueChangeError(TypeError): pass
    def __setattr__(self,key,value):
        if self.__dict__.has_key(key):
            raise self.ConstantValueChangeError, "Will not change constant's value. Constant name is '%s', requested value to be set is '%s'." %(key, value)
        self.__dict__[key]=value

sys.modules[__name__]=_constant()
