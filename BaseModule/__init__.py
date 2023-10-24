from .BaseModule import *

from ._LogError_V3 import logerror    as logger
from .             import _vectors    as vec
from ._matrix      import Matrix      as Matrix
# package typings
from .        import bm_typings

__version__ = '3.1.5 numpy-array-support'
__name__    = "BaseModule"
__author__  = "https://github.com/777Chara777"
__all__     = ( "logger", "vec", "Matrix", "BaseModule", "bm_typings", )
__doc__     = """
The BaseModule module provides a set of fundamental tools for working with matrices, vectors, and error logging. It includes the following components:

Modules:
    logger: A logger that offers functions for recording error messages.
    vec: A module containing functions for vector operations.
    Matrix: A class for handling matrices.
    bm_typings: Data types used within the module.

Author: https://github.com/777Chara777

Module Version: 3.1.5 with NumPy array support.

It's important to note that this module utilizes some of its components from other submodules, such as BaseModule, _LogError_V3, vectors, and matrix.
"""
