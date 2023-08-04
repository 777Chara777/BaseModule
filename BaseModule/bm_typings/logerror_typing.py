
# LogError_V3
class BaseLogError(Exception):
    """Base class for Base-Log-Error errors."""

class NotFindDirectory(BaseLogError):
    """An error is raised when don't find directory to file"""

class NotFindLevel(BaseLogError):
    """An error is raised when don't find level"""

class NotFindArgument(BaseLogError): 
    """An error is raised when don't find argument :/"""

DEBUG    =    "DEBUG"
INFO     =     "INFO"
WARNING  =  "WARNING"
ERROR    =    "ERROR"
CRITICAL = "CRITICAL"
