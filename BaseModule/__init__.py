from . import _vectors as vec

from ._LogError    import LogError    as logger
from ._LogError_V2 import LogError_V2 as logger2
from ._LogError_V3 import logerror    as logger3

from ._matrix import Matrix

from .BaseModule import *
from .BaseModule import __all__

__version__ = '3.1.4'
__name__    = "BaseModule"
__author__  = "https://github.com/777Chara777"
