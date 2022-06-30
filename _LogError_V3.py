from .LOGERRORV3 import _dop as dp

from . import BaseModule as bm
from . import _TypesList as tl



import functools
import traceback
import inspect
import rich

import sys


TypesLevels = {
    'CRITICAL': 40,
    'ERROR': 30,
    'WARNING': 20,
    'INFO': 10,
    'DEBUG': 0
}

import time
__version = '3.0.1'
_startTime = time.time()

class Core:
    def __init__(self):
        self.options = {
            "depth": 0,
            "defautlevel": 'INFO',
            "defautformat": '{time3} | {level}\t | {function} - {message}',
            "dir_file_save": None,
            "color": False,
        }

        self.handlers: dict = {}

class LogError_V3():
    def __init__(self):
        self._core = Core()

        self.debug(f"Inti module LogError_V3 {__version}-{_startTime}")

    def __repr__(self) -> str:
        return "<BaseModule._LogError_V3 handlers=%r>" % list(self._core.handlers.values())

    def add(self, __file, __format, __color): pass

    def setcolor(self, __color):
        if isinstance(__color, bool):
            self._core.options["color"] = __color
    
    def setformat(self, __format: str):
        if isinstance(__format, int):
            self._core.options["defautformat"] = __format
        
    def setfile(self, __file: str):
        if bm.misfile(__file):
            self._core.options["dir_file_save"] = __file

        else:
            raise Exception("File not found at given path '%s'" % __file)

    def setlevel(self, __level: str):
        """Set Defaut Format Standart `INFO`"""
        if __level in TypesLevels:
            self._core.options["defautlevel"] = __level


    def _log(self, __level, __options, __message, *args, **kargs) -> None:
        """Logger foramt message and save to file"""

        def savefile(msg):
            if self._core.options["dir_file_save"] is not None:
                with open(self._core.options["dir_file_save"], 'a+', encoding='utf-8') as file:
                    file.write(f"{msg}\n")

        def format_message(__foramt: str, _message, level):
            """Foramt message"""

            if dp.findmessage(__foramt, "{time") and __foramt[dp.findmessage_2(__foramt, "{time") + 6] == "}":
                mess_number = int( __foramt[dp.findmessage_2(__foramt, "{time") + 5] )
                __foramt = __foramt.replace(f'{{time{mess_number}}}', bm.Time(mess_number))
            
            if dp.findmessage(__foramt, "{level}"): 
                __foramt = __foramt.replace("{level}", level)

            if dp.findmessage(__foramt, "{function}"):
                text = "%s:%s:%s" % ( dp._getframe(__options['depth']) )
                __foramt = __foramt.replace("{function}", text)

            if dp.findmessage(__foramt, "{message}"): 
                __foramt = __foramt.replace("{message}", _message)


            return __foramt


        if __level not in TypesLevels: return

        if __options["defautformat"].strip() != '':
            if '--noprefix' not in args:
                message = format_message( 
                    __options["defautformat"] if 'format' not in kargs else kargs['format'], __message, __level
                )
            else:
                message = __message
            
        if '--noprint' not in args and TypesLevels[__level] >= TypesLevels[__options["defautlevel"]]:
            send_message = print if __options["color"] is False else rich.print
            send_message(message)
        
        if '--nosave' not in args and __options["dir_file_save"] is not None: savefile(message)
            


    def debug(self, message, *args, **kargs) -> None:
        self._log("DEBUG", self._core.options, message, *args, **kargs)
    
    def info(self, message, *args, **kargs) -> None:
        self._log("INFO", self._core.options, message, *args, **kargs)

    def warn(self, message, *args, **kargs) -> None:
        self._log("WARNING", self._core.options, message, *args, **kargs)

    def error(self, message, *args, **kargs) -> None:
        self._log("ERROR", self._core.options, message, *args, **kargs)

    def crit(self, message, *args, **kargs) -> None:
        self._log("CRITICAL", self._core.options, message, *args, **kargs)

    def log(self, level, options, message, *args, **kargs) -> None:
        self._log(level, options, message, *args, **kargs)


    def catch(
        self,
        exception=Exception, *,
        level = "ERROR" ,
        reverse = False,
        onerror = None,
        message = "An error has occurred"):

        if callable(exception) and (
            not inspect.isclass(exception) or not issubclass(exception, BaseException)
        ):
            return self.catch()(exception)


        class Catcher:
            def __init__(self_, decorator_type):
                self_._decorator_type = decorator_type

            def __enter__(self_):
                return None
            
            def __exit__(self_, type_, value_, traceback_):
                
                if type_ is None:
                    return

                if not self_._decorator_type:
                    return

                traceback_request = traceback.format_exception( *sys.exc_info() )

                hadler, name_error, traceback_errors = dp._process_traceback(traceback_request)

                options_depth = self._core.options.copy()
                options_depth['depth'] += 1

                self._log(level, options_depth, message)


                self._log(level, options_depth, hadler, '--noprefix')

                for num, x in enumerate( range(0, len(traceback_errors), 2) ):
                    self._log(level, options_depth, f"{num+1} {traceback_errors[x]}\n\t{traceback_errors[x+1]}\n", '--noprefix')
                
                self._log(level, options_depth, name_error, '--noprefix')

                if onerror is not None:
                    onerror(value_)

                return not reverse

            def __call__(_, function):
                catch = Catcher(True)
                
                if inspect.iscoroutinefunction(function):

                    async def catch_wrapper(*args, **kwargs):
                        with catch:
                            return await function(*args, **kwargs)
                
                else:
                    def catch_wrapper(*args, **kwargs):
                        with catch:
                            return function(*args, **kwargs)

                functools.update_wrapper(catch_wrapper, function)
                return catch_wrapper
        

        return Catcher(False)

logerror = LogError_V3()