from types import TracebackType
from .LOGERRORV3 import _dop as dp
from .LOGERRORV3 import _trackback as tb

from . import BaseModule as bm
from . import _TypesList as tl

from zipfile import ZipFile

import asyncio

import functools
import inspect
import rich


TypesLevels = {
    'CRITICAL': 40,
    'ERROR': 30,
    'WARNING': 20,
    'INFO': 10,
    'DEBUG': 0
}

import time
_version = '3.1.2'
_startTime = time.time()

class Core:
    def __init__(self):
        self.options = {
            "depth": 0,
            "defautlevel": 'INFO',
            "defautformat": '{time3} | {level}\t | {function} - {message}',
            "dir_file_save": None,
            "color": False,
            "maxfilesize": "100 KB"
        }

        self.handlers: dict = {}
    
    def __repr__(self) -> str:
        return f"<BaseModule._LogError_V3.Core {self.options}>"
        
class Singleton(type):
    _instanses = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instanses:
            cls._instanses[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instanses[cls]

class LogError_V3(metaclass=Singleton):
    def __init__(self):
        self._core = Core()
        self.loop = bm.AsyncLock()
        self.eventloop = asyncio.get_event_loop()


    def __repr__(self) -> str:
        return "<BaseModule._LogError_V3 handlers=%r, hash=%s>" % (list(self._core.handlers.values()), hash(self))

    def add(self, file = None, format = None, color = False, defautlevel = "INFO", maxfilesize = "100 KB"): 
        if file is not None:
            self.setfile(file)
        
        if format is not None:
            self.setformat(format)
        
        if color is not self._core.options["color"]:
            self.setcolor(color)
        
        if file is not self._core.options["defautlevel"]:
            self.setlevel(defautlevel)

    def setcolor(self, __color: bool):
        if isinstance(__color, bool):
            self._core.options["color"] = __color
    
    def setformat(self, __format: str):
        if isinstance(__format, str):
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

    def savelog(self):
        "save log file in .zip"
        file = self._core.options["dir_file_save"]
        name = str(file).split("/")[-1]
        with ZipFile(f"{file.replace(f'/{name}', '')}/{bm.Time(6)}-{name}.zip", "w") as newzip:
            newzip.write(file)
        open(file, 'w')

    def _log(self, __level, __options, __message, *args, **kargs) -> None:
        """Logger foramt message and save to file"""

        def savefile(msg):
            # await self.loop.acquire()
            if __options["dir_file_save"] is not None:
                
                int_number_type: int = bm.getlist_size(str(__options["maxfilesize"]).split(" ")[1])
                number, _, _ = bm.file_size(__options["dir_file_save"])
                name = str(__options["dir_file_save"]).split("/")[-1]
                if int_number_type < number:
                    with ZipFile(f"{bm.Time(6)}-{name}.zip", "w") as newzip:
                        newzip.write(__options["dir_file_save"])
                    open(__options["dir_file_save"], 'w')

                with open(__options["dir_file_save"], 'a+', encoding='utf-8') as file:
                    file.write(f"{msg}\n")
            # await self.loop.release()

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
                __foramt = __foramt.replace("{message}", str(_message))


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
        _exception=Exception, *,
        level = "ERROR" ,
        reverse = False,
        onerror = None,
        message = "An error has occurred"):

        if callable(_exception) and (
            not inspect.isclass(_exception) or not issubclass(_exception, BaseException)
        ):
            return self.catch()(_exception)


        class Catcher:
            def __init__(self_, decorator_type):
                self_._decorator_type = decorator_type

            def __enter__(self_):
                return None
            
            def __exit__(self_, type_, value_, traceback_: TracebackType):
                
                if type_ is None:
                    return

                if not self_._decorator_type:
                    return

                traceback_request = tb._format_traceback( traceback_ ) 

                options_depth = self._core.options.copy()
                options_depth['depth'] += 1

                traceba = ""
                for t in traceback_request['Lists_tb']:
                    traceba += f"{t}\n\n"

                tracebacks_text = f"{message}\n{traceback_request['Hadler_tb']}\n\n{traceba}{traceback_request['ErrorName_tb']}"

                self._log(level, options_depth, tracebacks_text)

                if onerror is not None:
                    onerror(value_)

                return not reverse

            def __call__(_, function):
                catch = Catcher(True)
                
                if inspect.iscoroutinefunction(function):
                    async def catch_wrapper(*args, **kwargs):
                        with catch:
                            return await function(*args, **kwargs)
                
                elif inspect.isgeneratorfunction(function):
                    def catch_wrapper(*args, **kwargs):
                        with catch:
                            return (yield from function(*args, **kwargs))
                
                else:
                    def catch_wrapper(*args, **kwargs):
                        with catch:
                            return function(*args, **kwargs)

                self._core.handlers[str(len(self._core.handlers)-1)] = function
                functools.update_wrapper(catch_wrapper, function)
                return catch_wrapper
        

        return Catcher(False)

logerror = LogError_V3()

