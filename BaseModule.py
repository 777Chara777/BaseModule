#!/usr/bin/env python3

import os
import sys

import json
import yaml
import rich
import zipfile

from datetime import datetime
from importlib import reload

# from enum import Enum

__all__ = ('mcls','misdir','misfile','Time','get_size','file_size','LogError','load_json','input_json','loadall_json')

def __system_info():
    return sys.platform

def __cls_info():
    if __system_info() == "win32":
        return "cls"
    elif __system_info() == 'linux':
        return 'clear'

mcls = lambda : os.system(__cls_info())

mplatform_ = lambda : __system_info()

misdir = lambda path : os.path.isdir(path)
misfile = lambda path : os.path.isfile(path)
mkdir = lambda path : os.mkdir(path)
mlistdir = lambda path : os.listdir(path)

mremove = lambda path : os.remove(path)
mgetlogin = lambda : os.getlogin()
mgetcwd = lambda : os.getcwd()

mrenamefile = lambda oldfilename, newfilename : os.rename(oldfilename, newfilename)
mdirname = lambda path : os.path.dirname(path)

mismodules = sys.modules

def mpause(text):
    print(text)
    sys.stdin.readline(1)

class mdeque(object):
    def __init__(self, maxlen:int) -> None:
        self.maxlen = maxlen
        self.array = []  

    def __str__(self) -> str:
        return str(self.array)
    
    def append(self, __object) -> None:
        if len(self.array) >= self.maxlen:
            del self.array[0]
        self.array.append(__object)     

    def converct(self) -> list:
        return self.array
    


def mjoin(data: "list | mdeque | str", string: str=' ', **kargs) -> 'str|list':
    """
    - prefix = ' '
    - next = `False|True`\n
    Example: mjoin(['ab', 'pq', 'rs'], '.') -> 'ab.pq.rs'
    """
    prefix = ""
    next = False
    if "prefix" in kargs:
        prefix = kargs['prefix']
    elif "next" in kargs:
        next = True

    mess:list = []
    if isinstance(data, str):
        mess.append( str("{2}{0}{1}{0}".format(prefix, data, '')) )
    else:
        for num, x in enumerate(data if isinstance(data, list) else data.converct() ):
            mess.append( str("{2}{0}{1}{0}".format(prefix, x, string if num != 0 else '')) )
    if next:
        return iter(mess)
    else:
        return ''.join(mess)

def Time(num: int=0):
    if num == -1:
        return (0,6)
    elif num == 0:
        return datetime.today().strftime("%d-%m-%Y %H:%M")
    elif num == 1:
        return datetime.today().strftime("%d-%m-%Y")
    elif num == 2:
        return datetime.today().strftime("%H:%M")
    elif num == 3:
        return str(datetime.today().strftime("%d-%m-%Y %H:%M:%S"))
    elif num == 4:
        return datetime.today().strftime("%H:%M:%S")
    elif num == 5:
        return int(datetime.today().strftime("%H%M%S"))
    elif num == 6:
        return int(datetime.today().strftime("%Y%m%d%H%M%S"))
    else:
        return "Not Find Time num"

def get_size(start_path = '.'):
    def convert_bytes(num):
        for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
            if num < 1024.0: 
                return f"{int(num)}"+" %s" % (x)
            num /= 1024.0
    total_size = 0
    for dirpath, _, filenames in os.walk(start_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            total_size += os.path.getsize(fp)
    return convert_bytes(total_size)

def file_size(file_path):
    def convert_bytes(num):
        # for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
        for x in [0, 1, 2, 3, 4]:
            if num < 1024.0:
                return [x, num]
                # return "%s" % (x)
            num /= 1024.0
    if os.path.isfile(file_path):
        file_info = os.stat(file_path)
        return convert_bytes(file_info.st_size)

class __Module(Exception): pass
def initModule(Module: str) -> "False | __Module":
    try:
        __import__(Module)
    except Exception as ex:
        return {"Type": False, "Message": ex}
    if Module in mismodules:
        return {"Type": True, "Module": mismodules[Module]}
    return {"Type": False, "Message": None}

def reloadModule(Module: __Module) -> __Module:
    # if Module in mismodules:
    return reload(Module)
    # return False
    
def load_json(derictory: str, *args) -> 'None | dict':
    if misfile(derictory) and len(args) != 0:
        with open(derictory, encoding="utf-8") as config_file:
            data: dict= json.load(config_file)
        data_info: dict={}
        for num, key in enumerate(args):
            if data.get(key) != None:
                if len(args)-num == 1 and len(data_info) == 0:
                    return data[key]
                data_info[key] = data[key]
        return data_info
    else:
        return None

def input_json(derictory: str, data: dict) -> 'bool':
    if isinstance(data, dict) and derictory.split('/')[-1].split('.')[-1] == 'json':
        with open(derictory, 'w', encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return True
    else:
        return False

def loadall_json(derictory: str) -> 'dict | None':
    if misfile(derictory):
        with open(derictory, encoding="utf-8") as config_file:
            data = json.load(config_file)
        return data
    else:
        return None

def input_yaml(derictory: str, data: dict) -> 'bool':
    if isinstance(data, dict) and derictory.split('/')[-1].split('.')[-1] in ['yml', 'yaml']:
        with open(derictory, 'w', encoding="utf-8") as f:
            yaml.dump(data, f)
        return True
    else:
        return False

def loadall_yaml(derictory: str) -> 'dict | None':
    if misfile(derictory):
        with open(derictory, encoding="utf-8") as config_file:
            data = yaml.load(config_file, Loader=yaml.FullLoader)
        return data
    else:
        return None

def listtostr(data: list) -> str:
    line = ''
    for x in data:
        line+=str(x)
    return line

def timeformat(time: int):
    date = {
        'M': 60,
        'H': 24,
        'D': 365,
        'Y': 100,
        'STL': 1
    }
    m= divmod(time, date['M'])[0]
    h= divmod(m, date['M'])[0]
    d= divmod(h, date['H'])[0]
    y= divmod(d, date['D'])[0]
    stl= divmod(y, date['Y'])[0]
    timelist = []
    if m != 0:
        timelist.append(f'#{m-h*date["M"]} minute')
    if h != 0:
        timelist.append(f'#{h-d*date["H"]} hour')
    if d != 0:
        timelist.append(f'#{d-y*date["D"]} days')
    if y != 0:
        timelist.append(f'#{y-stl*date["Y"]} year')
    if stl != 0:
        timelist.append(f'#{stl} century')

    return ' '.join(timelist)

def LogError(ctx, start_file, **kargs):
    direct = "./CrashLog" if "savefile" not in kargs else kargs["savefile"]
    if misdir(direct):
        start_file = start_file.split('\\')
        for x in os.getcwd().split('\\'):
            if x in start_file:
                start_file.remove(x)
            elif x.lower() in start_file:
                start_file.remove(x.lower())

        message = f"\n[{'/'.join(start_file)}] [UTC: {Time(0)}]: {ctx}"

        if misfile(f"{direct}/last.log") != True:
            open(f"{direct}/last.log", 'w').write(message)

        save = file_size(f"{direct}/last.log")
        if save[0] >= 2:
            with open(f"{direct}/last.log", 'r', encoding="UTF-8") as save_file_to_zit:
                file_to_zip = save_file_to_zit.read()
            open(f"{direct}/last.log", 'w')
            zipped = file_to_zip
            with open(f"{direct}/last-{Time(0)}.gz", 'w') as zip_save:
                zip_save.write(zipped)
        else:
            open(f"{direct}/last.log", 'a', encoding="UTF-8").write(message)
    else:
        os.mkdir(direct)

def dictkey(dictfile:dict) -> 'list | None':
    return [key for key in dictfile]

def dictitems(dictfile:dict) -> 'list | None':
    return [dictfile[item] for item in dictfile]

def zipdecode(filename: str) -> 'str | None':
    if misfile(filename):
        with zipfile.ZipFile(filename, 'r') as zipread:
            return zipread.read(zipread.namelist()[0]).decode('utf-8')
    return None

def zipencore(oldfile:str, filename: str) -> 'bool | None':
    if misfile(oldfile):
        try:
            with zipfile.ZipFile(filename, 'w') as zipsave:
                zipsave.write(oldfile)
            return True
        except:
            return False
    return None

class LogError_V2:
    """
    commads Arguments : --onreture, --noprint
    """
    import time
    __version__ = '0.0.3'
    _startTime = time.time()

    # class TypesList(Enum):
    #     CRITICAL = 50
    #     ERROR = 40
    #     WARNING = 30
    #     INFO = 20
    #     DEBUG = 10

    TypesList = {
        'CRITICAL': 50,
        'ERROR': 40,
        'WARNING': 30,
        'INFO': 20,
        'DEBUG': 10
    }

    inv_TypesList = {v: k for k, v in TypesList.items()}
    
    class ErrorClass:
        class ErrorNoneLogger(Exception): pass
        class ErrorNotFindArgument(Exception): pass
        class ErrorNotBool(Exception): pass
        class ErrorLanguageNotExists(Exception): pass
        class TypesList(Exception): pass

    class logger:
        def __init__(self, FileName: str=None, languagemodule: str='eng', format:str='', \
             color: bool=False, messagelavel: 'LogError_V2.ErrorClass.TypesList' = None ) -> None:
            """
            #### Init commands Logger:
            LanguageModule: `rus|eng`
            format: this is the format of your message. attributes
                * {Time%num%} - Time -> This is the number for the output type you can look at Time(%num%)
                * {Type} - Message type [`DEBUG|INFO|WARNING|ERROR|CRITICAL`]
                * {Msg} - Your message
                * {Root} - run file > not work\n
            color: `True|False` - support for the rich module.\n
            #### Commands Logger:
            Regular commands `debub|info|warn|error|crit`\n
            SaveConfig and WithSaveConfig commands `it's Regular commands and "rename"`
                * rename - Save the file as `filename{datetime}.zip` it's defaut format.`
            """
            self.TypeColor = color
            self.FileName = FileName
            self.lastLang = languagemodule
            self.defautformat = format
            self.PrefixLog = lambda : {
                'DEBUG': self.LanguageModule['PrefixLog']['DEBUG'],
                'INFO': self.LanguageModule['PrefixLog']['INFO'],
                'WARNING': self.LanguageModule['PrefixLog']['WARNING'],
                'ERROR': self.LanguageModule['PrefixLog']['ERROR'],
                'CRITICAL': self.LanguageModule['PrefixLog']['CRITICAL'],
            }
            self.defautlevel = LogError_V2.TypesList["WARNING"] if messagelavel is None else messagelavel
            
            self.LanguageModule = self.langmodule(languagemodule)

        def langmodule(self, lang:str, data_lang: dict=None) -> 'dict | LogError_V2.ErrorClass.ErrorLanguageNotExists':
            data = {
                'eng': {
                    'PrefixLog': {
                        'DEBUG': 'Debug',
                        'INFO': 'Info',
                        'WARNING': '[orange1]WARNING[/orange1]',
                        'ERROR': '[red]ERROR[/red]',
                        'CRITICAL': '[red3]CRITICAL[/red3]' 
                    },
                    'LangModule': {
                        'ReplaceLang': 'Changed language to `{0}`',
                        'ErrorNoFindLang': 'No such language exists `{0}`'
                    },
                    'ClassError': {
                        'ErrorArgument': 'No Find Argument {0}',
                        'ErrorArgumentNotFind': 'Argument not found: `{0}`',
                        'ErrorNotBool': "it's `{0} - {1}` not bool argument",
                        'ErrorNotFindName': 'Not find name in {0}'
                    }
                }, 
                'rus': {
                    'PrefixLog': {
                        'DEBUG': '[blue]Дебаг[/blue]',
                        'INFO': '[blue]Информацыя[/blue]',
                        'WARNING': '[yellow]ПРОЕДУПРЕЖДЕНИЕ[/yellow]',
                        'ERROR': '[red]ОШИБКА[/red]',
                        'CRITICAL': '[red]КРИТИЧЕСКАЯ ОШИБКА[/red]' 
                    },
                    'LangModule': {
                        'ReplaceLang': 'Язык изменён на `{0}`',
                        'ErrorNoFindLang': 'Такого языка не существует `{0}`'
                    },
                    'ClassError': {
                        'ErrorArgument': 'Не найден аргумент {0}',
                        'ErrorArgumentNotFind': 'Аргумент не найден: `{0}`',
                        'ErrorNotBool': "Это `{0} - {1}` не bool аргумент",
                        'ErrorNotFindName': 'Не найден название в {0}'
                    }
                }
            }   
            if data_lang is not None:
                data.update(data_lang)

            if lang in data:
                if self.lastLang != lang:
                    self.info(str(data[self.lastLang]['LangModule']['ReplaceLang']).format(lang))
                    self.lastLang = lang
                return data[lang]
            else:
                self.error(str(data['eng']['LangModule']['ErrorNoFindLang']).format(lang))
                self.lastLang = 'eng'
                return data['eng']
        
        def restart_lang(self, lang:str, data:dict=None) -> 'dict | None':
            self.LanguageModule = self.langmodule(lang,data)
            return self.LanguageModule

        def _log(self, level, msg, *args, **kargs):
            printon = True
            returnon = False

            mprint = print if not self.TypeColor else rich.print

            if level >= self.defautlevel:
                listargs = ['--noprint', '--onreture']
                listkargs = ['format']
                if '--noprint' in args:
                    printon = False
                if '--onreture' in args:
                    returnon = True
                if [x for x in args] in listargs and len(args) != 0:
                    raise LogError_V2.ErrorClass.ErrorNotFindArgument(str(self.LanguageModule['ClassError']['ErrorArgument']).format(['' if x in listargs else x for x in args]))
                
                if 'format' in kargs or self.defautformat.strip() != '':
                    if 'format' in kargs:
                        message = kargs['format']
                    elif self.defautformat.strip() != '':
                        message = self.defautformat

                    if message.find('{Type}') != -1:
                        message = message.replace('{Type}', self.PrefixLog()[LogError_V2.inv_TypesList[level]])

                    if message.find('{Msg}') != -1:
                        message = message.replace('{Msg}', msg)

                    if message.find('{Time') != -1 and message[message.find('{Time') + 6] == "}":
                        number = int( message[ message.find('{Time') + 5 ] )
                        text = f'{{Time{number}}}'
                        message = message.replace(text, str(Time(number)))

                    if message.find('{Root}') != -1:
                        message = message.replace('{Root}', __name__)

                    if printon:
                        mprint(message)
                    else:
                        return message
                    if returnon:
                        return message

                elif len(kargs) != 0 and kargs not in listkargs:
                    raise LogError_V2.ErrorClass.ErrorNotFindArgument(str(self.LanguageModule['ClassError']['ErrorArgumentNotFind']).format(" ".join(dictkey(kargs))))

                else:
                    if printon:
                        mprint(self.PrefixLog()[LogError_V2.inv_TypesList[level]], msg)    
                    else:
                        return f'{self.PrefixLog()[LogError_V2.inv_TypesList[level]]} {msg}'
                    if returnon:
                        return f'{self.PrefixLog()[LogError_V2.inv_TypesList[level]]} {msg}'
                    

        def debug(self, msg, *args, **kargs):
            info = self._log(LogError_V2.TypesList["DEBUG"], msg, *args, **kargs)
            if info != None:
                return info
        
        def info(self, msg, *args, **kargs):
            info = self._log(LogError_V2.TypesList["INFO"], msg, *args, **kargs)
            if info != None:
                return info

        def warn(self, msg, *args, **kargs):
            info = self._log(LogError_V2.TypesList["WARNING"], msg, *args, **kargs)
            if info != None:
                return info

        def error(self, msg, *args, **kargs):
            info = self._log(LogError_V2.TypesList["ERROR"], msg, *args, **kargs)
            if info != None:
                return info

        def crit(self, msg, *args, **kargs):
            info = self._log(LogError_V2.TypesList["CRITICAL"], msg, *args, **kargs)
            if info != None:
                return info
        
    class _LogSave(logger):

        def __init__(self, file, languagemodule:str, format:str, color:bool, *args, **kargs) -> None:
            super().__init__(None)
            LogError_V2.logger.__init__(self, None)
            self.defautlevel = LogError_V2.TypesList['DEBUG']
            # self.savefile = file
            self.args = args
            self.kargs = kargs
            self.filename = file
            self.defautformat = format
            self.TypeColor = color
            self.LanguageModule = self.restart_lang(languagemodule)

        def debug(self, msg, *args, **kargs):
            # self.savefile.write(str(super().debug(msg, '--onreture', *args, **kargs))+'\n')
            with open(self.filename, mode=self.kargs['mode'], encoding=self.kargs['encoding']) as savefile:
                savefile.write(str(super().debug(msg, '--onreture', *args, **kargs))+'\n')

        def info(self, msg, *args, **kargs):
            # self.savefile.write(str(super().info(msg, '--onreture', *args, **kargs))+'\n')
            with open(self.filename, mode=self.kargs['mode'], encoding=self.kargs['encoding']) as savefile:
                savefile.write(str(super().info(msg, '--onreture', *args, **kargs))+'\n')

        def warn(self, msg, *args, **kargs):
            # self.savefile.write(str(super().warn(msg, '--onreture', *args, **kargs))+'\n')
            with open(self.filename, mode=self.kargs['mode'], encoding=self.kargs['encoding']) as savefile:
                savefile.write(str(super().warn(msg, '--onreture', *args, **kargs))+'\n')

        def error(self, msg, *args, **kargs):
            # self.savefile.write(str(super().error(msg, '--onreture', *args, **kargs))+'\n')
            with open(self.filename, mode=self.kargs['mode'], encoding=self.kargs['encoding']) as savefile:
                savefile.write(str(super().error(msg, '--onreture', *args, **kargs))+'\n')
        
        def crit(self, msg, *args, **kargs):
            # self.savefile.write(str(super().crit(msg, '--onreture', *args, **kargs))+'\n')
            with open(self.filename) as savefile:
                savefile.write(str(super().crit(msg, '--onreture', *args, **kargs))+'\n')
        
        def resave(self, selflogger: 'LogError_V2.logger', filename:str='', *args, **kargs):
            self.FileName = selflogger.FileName
            self.defautformat = selflogger.defautformat
            
            def savefile(filename:str):
                start = Time(6)
                file = filename.split('.')[-2]
                format_file = f"{file}-{start}.gz"
                zipencore(filename, format_file)
                open(filename, 'w')

            self.info('Save File', **kargs)

            savefile(filename) if str(filename).strip() != '' else savefile(self.FileName)

    class SaveConfig(_LogSave):
        def __init__(self, LoggerSelf: 'LogError_V2.logger', filename: str='', mode:str='a+', encoding='utf-8', **kargs) -> None:
            if filename.strip() != '':
                if not misfile(filename): open(filename, 'w')

                # self.file = open(filename, mode, encoding=encoding, **kargs)
                # super().__init__(self.file, LoggerSelf.lastLang, '', LoggerSelf.TypeColor)
                super().__init__(filename, LoggerSelf.lastLang, '', LoggerSelf.TypeColor, mode=mode,encoding=encoding)
            else:
                if not misfile(LoggerSelf.FileName):
                    open(LoggerSelf.FileName, 'w')
                # print( LoggerSelf.lastLang, LoggerSelf.defautformat, LoggerSelf.TypeColor)
                # self.file = open(LoggerSelf.FileName, mode, encoding=encoding, **kargs)
                filename = LoggerSelf.FileName
                # super().__init__(self.file, LoggerSelf.lastLang, LoggerSelf.defautformat, LoggerSelf.TypeColor)
                super().__init__(filename, LoggerSelf.lastLang, LoggerSelf.defautformat, LoggerSelf.TypeColor, mode=mode,encoding=encoding)

        # def __del__(self) -> None:
        #     self.file.close()


    class WithSaveConfig():
        def __init__(self, LoggerSelf: 'LogError_V2.logger', filename: str='', mode:str='a+', encoding='utf-8', **kargs):
            self._typesave = True
            self.kargs = kargs
            self.LoggerSelf = LoggerSelf
            self.filename = filename
            self.mode = mode
            self.encoding = encoding

            self.ziptype = False
            if 'ziptype' in self.kargs:
                if isinstance(self.kargs['ziptype'], bool):
                    self.ziptype = self.kargs['ziptype']
                else:
                    raise LogError_V2.ErrorClass.ErrorNotBool(str(LoggerSelf.LanguageModule['ClassError']['ErrorNotBool']).format(self.kargs['ziptype']))

        def __enter__(self):
            def __sizetest(path:str):
                if file_size(path)[0] and self.ziptype:
                    with open(path, 'r', encoding="UTF-8") as save_file_to_zit:
                        file_to_zip = save_file_to_zit.read()
                    open(path, 'w')
                    zipped = file_to_zip
                    with open('.'.join(path.split('.')[:-1])+f'-{Time(1)}.gz', 'w') as zip_save:
                        zip_save.write(zipped)
                        zip_save.close()

            if self.filename.strip() != '':
                if not misfile(self.filename): open(self.filename, 'w')
                __sizetest(self.filename)

                self.file = open(self.filename, mode=self.mode, encoding=self.encoding)
                # return LogError_V2._LogSave(self.file, '')
                return LogError_V2._LogSave(self.file, self.LoggerSelf.lastLang, '', self.LoggerSelf.TypeColor)
            else:
                if self.LoggerSelf.FileName != None:
                    if not misfile(self.LoggerSelf.FileName): open(self.LoggerSelf.FileName, 'w')
                    __sizetest(self.LoggerSelf.FileName)

                    self.file = open(self.LoggerSelf.FileName, mode=self.mode, encoding=self.encoding)
                    return LogError_V2._LogSave(self.file, self.LoggerSelf.lastLang, self.LoggerSelf.defautformat, self.LoggerSelf.TypeColor)
                else:
                    raise LogError_V2.ErrorClass.ErrorNoneLogger(str(self.LoggerSelf.LanguageModule['ClassError']['ErrorNotFindName']).format(self.filename.__class__))

        def __exit__(self, exc_type, exc_value, tb):
            self.file.close()