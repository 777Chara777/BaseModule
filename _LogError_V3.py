from .LOGERRORV3._get_frame import get_frame
from .LOGERRORV3._head import write as logw

from . import BaseModule as bm
from . import _TypesList as tl

import functools
import traceback

import sys


TypesLevels = {
    'CRITICAL': 40,
    'ERROR': 30,
    'WARNING': 20,
    'INFO': 10,
    'DEBUG': 0
}

import time
__version = '3.0.0'
_startTime = time.time()

def addlevel(levelname: str, levelnumber: int):
    if levelname not in TypesLevels:
        TypesLevels[levelname] = levelnumber


class Core:
    def __init__(self):
        self.options = {
            "color": False,
            "logfile": None,
            "depth": 0,
            "defautlevel": 'INFO',
            "defautformat": '{time3} | {level}\t | {type} - {message}'
        }

class LogError_V3:
    def __init__(self) -> None:
        self._core = Core()
        self.options = self._core.options

    def __repr__(self) -> str:
        pass
    
    def setlevel(self,level):
        if level not in TypesLevels:
            raise tl.NotFindLevel(f"Not find level {level}")
        
        self.options["defautlevel"] = level

    def setformat(self, format:str):
        """set message format now ``{time3} |@{level}\t {type} | {message}``"""
        self.options["defautformat"] = format

    def setlogfile(self, filepath:str) -> None:
        def setlog():
            self.options['logfile'] = filepath
            open(filepath, 'w')

        if bm.misfile(filepath):
            setlog()
        elif bm.misdir(filepath):
            setlog()
        else: raise tl.NotFindDirectory(f"Not find directory, please check the path `{filepath}`")

    def _getframe(self, number=0):
        frame = get_frame(self.options['depth'] + (3 + number))

        code = frame.f_code

        try:
            name = frame.f_globals["__name__"]
        except KeyError:
            name = None

        return (name, code.co_name, frame.f_lineno)

    def _savefile(self, message):
        if self.options['logfile'] is not None:
            with open(self.options['logfile'], 'w') as file:
                file.write(str(message)+'\n')

    def _log(self, __level, __message, options, *args, **kargs):

        
        defautlevel_num = int(TypesLevels[options["defautlevel"]])

        if defautlevel_num > TypesLevels[__level]:
            return
        
        listkargs = ['format']
        listargs = ["--noprint"]

        if 'format' in kargs or options['defautformat'].strip() != '':
            if 'format' in kargs:
                message: str = kargs['format']

            elif options['defautformat'].strip() != '':
                message: str = options['defautformat']
            else: return

            if message.find('{level}') != -1:
                message = message.replace('{level}', __level)

            if message.find('{message}') != -1:
                message = message.replace('{message}', __message)
            
            if message.find('{type}') != -1:
                mess_type = "%s:%s:%s" % self._getframe(options['depth'])
                message = message.replace('{type}', mess_type)

            if message.find('{time') != -1 and message[message.find('{time') + 6] == "}":
                number = int( message[ message.find('{time') + 5 ] )
                text = f'{{time{number}}}'
                message = message.replace(text, str(bm.Time(number)))
            
            if "--noprint" not in args:
                logw(f"{message}", self.options['color'])

            if self.options['logfile'] is not None and "--nosave" not in args:
                with open(self.options['logfile'], 'a+', encoding='utf-8') as file:
                    file.write(f"{message}")


        elif len(kargs) != 0 and kargs not in listkargs:
            raise tl.NotFindArgument("Argument not found: `{0}`".format(" ".join(bm.dictkey(kargs))))
        
        else:
            logw(f"{__level} {message}", self.options['color'])

            if self.options['logfile'] is not None and "--nosave" not in args:
                with open(self.options['logfile'], 'a+', encoding='utf-8') as file:
                    file.write(f"\n{message}")


    def debug(self, __message, *args, **kargs):
        """debug message ``format(*args, **kwargs)``"""
        self._log("DEBUG", __message, self.options, *args, **kargs)

    def info(self, __message, *args, **kargs):
        """info message ``format(*args, **kwargs)``"""
        self._log("INFO", __message, self.options, *args, **kargs)

    def warn(self, __message,  *args, **kargs):
        """warning message ``format(*args, **kwargs)``"""
        self._log("WARNING", __message, self.options,  *args,**kargs)

    def error(self, __message, *args, **kargs):
        """error message ``format(*args, **kwargs)``"""
        self._log("ERROR", __message, self.options,  *args, **kargs)

    def crit(self, __message, *args,  **kargs):
        """critical message ``format(*args, **kwargs)``"""
        self._log("CRITICAL", __message, self.options, *args,**kargs)


    def log(self, __level, __message, *args, **kargs):
        """info message ``format(*args, **kwargs)``"""
        if __level not in TypesLevels:
            raise Exception("There is no such level")
        self._log(__level, __message, self.options, *args, **kargs)

    
    def catch(self,
        reverse = False,
        onerror = "An error has occurred",
        level = "ERROR"
        ):

        class Catcher:
            def __init__(self_, decorator_type):
                self_._decorator_type = decorator_type

            def __enter__(self_):
                return None
            
            def __exit__(self_, type_, value, traceback_):

                if not self_._decorator_type:
                    return

                out = traceback.format_exception( *sys.exc_info() )
                traceback_list = []

                for x in [x.replace("\n", '').split('  ') for x in out]:
                    for text in x:
                        if text != '':
                            traceback_list.append(text)

                depth_2 = self.options.copy()
                depth_2["depth"] = int(depth_2["depth"]) + 1

                self._log(level, onerror, depth_2)

                traceback_message = traceback_list.pop(0)
                error_raise = traceback_list.pop(-1)
                colortype = self.options["color"]
                
                logw(traceback_message, "--nosave", color=colortype)
                traceback_list_new = {}
                for num, x in enumerate( range(0, len(traceback_list), 2) ):
                    traceback_list_new[traceback_list[x]] = traceback_list[x+1]
                    logw(f"{num+1}", traceback_list[x], f"\n\t{traceback_list[x+1]}\n", color=colortype)
                logw(error_raise, color=colortype)


                json_file = f"{onerror} \n{traceback_message}\n{str(traceback_list_new)}\n{error_raise}"
                self._log(level, json_file, depth_2, "--noprint")

                return not reverse

            def __call__(_, function):
                catch = Catcher(True)

                def catch_wrapper(*args, **kwargs):
                    with catch:
                        return function(*args, **kwargs)

                functools.update_wrapper(catch_wrapper, function)
                return catch_wrapper

        return Catcher(False)


logerror = LogError_V3()