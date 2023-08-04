from types import TracebackType

from .bm_typings.logerror_typing import DEBUG, INFO, WARNING, ERROR, CRITICAL
from .m_logerror_v3 import _dop as dp, _trackback as tb

from . import BaseModule as bm
from .bm_typings import logerror_typing as tl


from zipfile import ZipFile


import functools
import inspect
import rich
import time

TypesLevels = {
    'CRITICAL': {"weight": 40, "function": exit},
    'ERROR':    {"weight": 30, "function": None   },
    'WARNING':  {"weight": 20, "function": None   },
    'INFO':     {"weight": 10, "function": None   },
    'DEBUG':    {"weight": 0,  "function": None   }
}

__version__ = '3.1.6'
__start__ = time.time()
# _core__instanses: dict={}

class Core:
    __core__instanses: dict={}
    def __init__(self, Caption="_default"):

        NameCore: str= Caption
        if NameCore not in self.__core__instanses:
            self.__core__instanses[NameCore] = {
                "depth": 0,
                "defautlevel": 'INFO',
                "defautformat": '{time3} | {coretype} {level}\t | {function} - {message}',
                "dir_file_save": None,
                "color": False,
                "maxfilesize": "100 KB"
            }
        self.options  : dict = self.__core__instanses[NameCore]
        self.handlers : dict = {}
        self._coreName: str  = NameCore
    
    def __repr__(self) -> str:
        return f"<BaseModule.LogError_V3.Core hash={hash(self)} name={self._coreName} \n - {self.options=}>"

        
class Singleton(type):
    _instanses = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instanses:
            cls._instanses[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instanses[cls]

# class Singleton_2:
#     _instanses: dict= {}
#     def __new__(cls, *args, **kwargs):
#         if cls not in cls._instanses:
#             cls._instanses[cls] = super(Singleton, cls).__new__(cls, *args, **kwargs)
#         return cls._instanses[cls]

class LogError_V3(metaclass=Singleton):
    def __init__(self):
        self._core = Core("_default")
        self.__LenCalls = 0


    def __repr__(self) -> str:
        return "<BaseModule.LogError_V3 handlers=%r, calls=%i, hash=%s, hash_core=%s, core_name=%s>" % (
            list(self._core.handlers.values()), 
            self.__LenCalls,
            hash(self), 
            hash(self._core), 
            self._core._coreName
        )

    def add(self, file = None, format = None, color = False, defaultlevel = "INFO",  maxfilesize = "100 KB", default_core = "_default"): 
        if file is not None:
            self.setfile(file)
        
        if format is not None:
            self.setformat(format)
        
        if color is not self._core.options["color"]:
            self.setcolor(color)
        
        if file is not self._core.options["defautlevel"]:
            self.setlevel(defaultlevel)
        
        if default_core != "_default":
            self.load_core(default_core)

    def load_core(self, Caption: str="_default"):
        """Set core type"""
        self._core = Core(Caption)

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
        file: str = self._core.options["dir_file_save"]
        name: str = file.split("/")[-1]
        with ZipFile(f"{file.replace(f'/{name}', '')}/{bm.Time(6)}-{name}.zip", "w") as newzip:
            newzip.write(file)
        open(file, 'w')

    def create_core(self, Caption: str="_default"):
        """Creating or Eding new core do not use it
        ```py
        with logerror.create_core("Test") as core:
            # core.setcolor  core.setformat  core.setfile  core.setlevel
            # core.getcolor  core.getformat  core.getfile  core.getlevel
            
            core.setcolor(True)
            core.setformat("{function} {message}")
        
        ``` """
        class CreateCore:

            def __enter__(_self) -> "dict":

                class Core2(Core):
                    def __init__(self, caption):
                        super().__init__(caption)
                    
                    def setcolor(self, __color: bool):
                        if isinstance(__color, bool):
                            self.options["color"] = __color
                    
                    def setformat(self, __format: str):
                        if isinstance(__format, str):
                            self.options["defautformat"] = __format
                        
                    def setfile(self, __file: str):
                        if bm.misfile(__file):
                            self.options["dir_file_save"] = __file
                        else:
                            raise Exception("File not found at given path '%s'" % __file)

                    def setlevel(self, __level: str):
                        """Set Defaut Format Standart `INFO`"""
                        if __level in TypesLevels:
                            self.options["defautlevel"] = __level

                    @property
                    def getcolor(self):
                        return self.options["color"]
                    @property
                    def getformat(self):
                        return self.options["defautformat"]
                    @property
                    def getfile(self):
                        return self.options["dir_file_save"]
                    @property
                    def getlevel(self):
                        return self.options["defautlevel"]

                return Core2(Caption)

            def __exit__(_self, exception_type, exception_value, traceback):
                pass

        return CreateCore()

    def _log(self, __level, __options, __message, *args, **kargs) -> None:
        """Logger foramt message and save to file"""

        self.__LenCalls+=1

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
            
            if dp.findmessage(__foramt, "{lencalls}"): 
                __foramt = __foramt.replace("{lencalls}", str(self.__LenCalls))

            if dp.findmessage(__foramt, "{coretype}"): 
                __foramt = __foramt.replace("{coretype}", str(self._core._coreName))

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
            
        if '--noprint' not in args and TypesLevels[__level]['weight'] >= TypesLevels[__options["defautlevel"]]['weight']:
            send_message = print if __options["color"] is False else rich.print
            send_message(message)
        
        if '--nosave' not in args and __options["dir_file_save"] is not None: savefile(message)
            
        if TypesLevels[__level]['function'] is not None:
            TypesLevels[__level]['function']()

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
        _exception=Exception,
        reverse   = False, *,
        level     = "ERROR" ,
        onerror   = None    ,
        message   = "An error has occurred",
        ignore_exceptions: tuple= (SystemExit,)):

        """
        - level = "ERROR" -> level send message
        - onerror = None -> will be called on error `lambda error : you're function`
        - message = "An error has occurred" -> error message
        - ignore_exceptions: tuple= (SystemExit,) -> ignore exeptions
        """

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

                options_depth = self._core.options.copy()
                options_depth['depth'] += 1
                
                if (type_ in ignore_exceptions): # Ignor_Exeptions 
                    self._log("INFO", options_depth, f"Ignor Exceptions: {type_.__name__}")
                    if onerror is not None:
                        onerror(value_)

                    if type_ in (SystemExit, KeyboardInterrupt,):
                        return False
                    
                    return not reverse

                if (type_ is None) or (not self_._decorator_type):
                    return

                traceback_request = tb._format_traceback( traceback_ ) 


                traceback_description = ""
                for t in traceback_request['Description']:
                    traceback_description += f"{t}\n\n"

                tracebacks_message = "%s\n%s\n\n%s%s" % (
                    message,
                    traceback_request['Header'],
                    traceback_description,
                    traceback_request['ErrorCaption']
                )
                
                self._log(level, options_depth, tracebacks_message)

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
