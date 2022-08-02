#!/usr/bin/env python3

import os
import sys
import asyncio

import json
import yaml
import zipfile
import sqlite3
import inspect
import linecache
import ast
import traceback as tbs

from types import TracebackType

from datetime import datetime
from importlib import reload


__all__ = (
    'mcls',
    'mplatform_',
    'misdir',
    'misfile',
    'mkdir',
    'mlistdir',
    'mremove',
    'mgetlogin',
    'mgetcwd',
    'mrenamefile',
    'mdirname',
    'mismodules',
    'mutcnow',
    'mpause',
    'mdeque',
    'mjoin',
    'initModule',
    'reloadModule',
    'input_yaml',
    'loadall_yaml',
    'connectdb',
    'listtostr',
    'timeformat',
    'dictkey',
    'dictitems',
    'zipdecode',
    'zipencore',
    'Time',
    'get_size',
    'file_size',
    'LogError',
    'load_json',
    'input_json',
    'loadall_json',
    "trackback_format")

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

mutcnow = lambda : datetime.utcnow()

def mlistdir2(path: str, end_swich: str=None) -> "list | str":
    list_files: list=[]
    if misfile(path):
        for file in os.listdir(path):
            if file.endswith(end_swich) or end_swich is None:
                list_files.append(file)
    else:
        return f"Not find path: {path}"

def mpause(text: str):
    """pause"""
    print(text)
    sys.stdin.readline(1)

class mdeque(object):
    def __init__(self, maxlen:int) -> None:
        self.maxlen = maxlen
        self.array = []  

    def __str__(self) -> str:
        return str(self.array)
    
    def __repr__(self) -> str:
        return "<BaseModule.mdeque handlers=[maxlen=%s, array=%r]>" % (self.maxlen, self.array)
    
    def append(self, __object) -> None:
        if len(self.array) >= self.maxlen:
            del self.array[0]
        self.array.append(__object)     

    def converct(self) -> list:
        return self.array
    


def mjoin(__string: "list | mdeque | str", __iterable: str=' ', **kargs) -> 'str|list':
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
    if isinstance(__string, str):
        mess.append( str("{2}{0}{1}{0}".format(prefix, __string, '')) )
    else:
        for num, x in enumerate(__string if isinstance(__string, list) else __string.converct() ):
            mess.append( str("{2}{0}{1}{0}".format(prefix, x, __iterable if num != 0 else '')) )
    if next:
        return iter(mess)
    else:
        return ''.join(mess)

def Time(num: int=0):
    """This function"""
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
        return "Not Find Time numbre"

def get_size(start_path = '.'):
    """getting file weight
    * getting the weight of the form [bytes-TB, weight]"""
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

def getlist_size(size_: str):
    "Get list ['bytes', 'KB', 'MB', 'GB', 'TB'] -> [0, 1, 2, 3, 4]"
    return ['bytes', 'KB', 'MB', 'GB', 'TB'].index(size_)

def file_size(file_path):
    """getting file weight
    * getting the weight of the form [0-4, bytes-TB, weight]"""
    def convert_bytes(num):
        for x in [0, 1, 2, 3, 4]:
            if num < 1024.0:
                return (x, ['bytes', 'KB', 'MB', 'GB', 'TB'][x], num)
                # return "%s" % (x)
            num /= 1024.0
    if os.path.isfile(file_path):
        file_info = os.stat(file_path)
        return convert_bytes(file_info.st_size)

class __Module(Exception): pass
def initModule(Module: str) -> "False | __Module":
    """Module initialization"""
    try:
        __import__(Module)
    except Exception as ex:
        return {"Type": False, "Message": ex}
    if Module in mismodules:
        return {"Type": True, "Module": mismodules[Module]}
    return {"Type": False, "Message": None}

def reloadModule(Module: __Module) -> __Module:
    """Reload Module"""
    return reload(Module)
    
def load_json(derictory: str, *args) -> 'None | dict':
    """getting specific key from json file"""
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
    """loading dist file to json"""
    if isinstance(data, dict) and derictory.split('/')[-1].split('.')[-1] == 'json':
        with open(derictory, 'w', encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return True
    else:
        return False

def loadall_json(derictory: str) -> 'dict | None':
    """Getting the entire json file as a dict"""
    if misfile(derictory):
        try:
            with open(derictory, encoding="utf-8") as config_file:
                data = json.load(config_file)
            return data
        except Exception as ex:
            return (None, str(ex))
    else:
        return None

class loadall_json2:
    def __init__(self, path: str) -> None:
        if not misfile(path):
            return
        self.filepath = path

    def __enter__(self):
        self.data = loadall_json(self.filepath)
        return self.data
        
    def __exit__(self, type_, value_, traceback_):
        input_json(self.filepath, self.data)

def input_yaml(derictory: str, data: dict) -> 'bool':
    """loading dist file to yaml/yml"""
    if isinstance(data, dict) and derictory.split('/')[-1].split('.')[-1] in ['yml', 'yaml']:
        with open(derictory, 'w', encoding="utf-8") as f:
            yaml.dump(data, f)
        return True
    else:
        return False

def loadall_yaml(derictory: str) -> 'dict | None':
    """Getting the entire yaml/yml file as a dict"""
    if misfile(derictory):
        try:
            with open(derictory, encoding="utf-8") as config_file:
                data = yaml.load(config_file, Loader=yaml.FullLoader)
            return data
        except Exception as ex:
            return (None, str(ex))
    else:
        return None

from sqlite3.dbapi2 import Connection, Error

def connectdb(__path:str) -> 'None | Connection': 
    try:
        return sqlite3.connect(__path)
    except Error:
        return None

def listtostr(data: list) -> str:
    "List to String"
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
        except Exception as ex:
            return (False, ex)
    return None
def trackback_format(tb: TracebackType) -> dict:
    def traceback_get_info(tb) -> dict:

        def get_relevant_names(tree):
            return [node for node in ast.walk(tree) if isinstance(node, ast.Name)]

        def format_value(v):
            try:
                v = repr(v)
            except KeyboardInterrupt:
                raise
            except BaseException:
                v = u'<unprintable %s object>' % type(v).__name__

            max_length = 128
            if max_length is not None and len(v) > max_length:
                v = v[:max_length] + '...'
            return v

        def get_relevant_values(frame, tree):
            names = get_relevant_names(tree)
            values = []

            for name in names:
                text = name.id
                col = name.col_offset
                if text in frame.f_locals:
                    val = frame.f_locals.get(text, None)
                    values.append((text, col, format_value(val)))
                elif text in frame.f_globals:
                    val = frame.f_globals.get(text, None)
                    values.append((text, col, format_value(val)))

            values.sort(key=lambda e: e[1])

            return values

        frame_info = inspect.getframeinfo(tb)

        filename = frame_info.filename
        lineno = frame_info.lineno
        function = frame_info.function
        

        if filename == '<string>':
            source = ''
        else:
            source = linecache.getline(filename, lineno)

            source = source.strip()
        

        tree = ast.parse(source, mode='exec')
        relevant_values = get_relevant_values(tb.tb_frame, tree)

        return {
            "FilePath": filename,
            "Line": lineno,
            "Function": function,
            "Source": source,
            "args": relevant_values
        }

    def format_frame(data: dict, number: int=0) -> str:
        format_tb_str: str=''
        
        source = data["Source"]
        format_tb_str += '%s File "%s", line %s, in %s\n    %s' % (number, data["FilePath"], data["Line"], data["Function"], source)
        
        args:list = data["args"]
        args.reverse()


        if len(args) != 0:
            for num_line in range(len(args)):
                newline = ""

                for num_arg, arg in enumerate(args):
                    _, line, func = arg

                    format_number = int(num_arg+1) - int(num_line+1)

                    if format_number == 0:
                        newline += str(' ' * (line+4)) + f"└─ {func}"
                    
                    elif format_number > 0:
                        newline_list = list(newline)
                        newline_list[line+4] = "│"
                        newline = ''.join(newline_list)

                
                format_tb_str+=f'\n{newline}'

        return format_tb_str

    if tb is None:
        tb = sys.exc_info()[2]
        
    value = tbs.format_exception( *sys.exc_info() )[-1].replace("\n",'')

    format_traceback: dict={
        "Hadler_tb": "Traceback (most recent call last):",
        "Lists_tb": [],
        "ErrorName_tb": value
    }   

    number = 1
    while tb:
        format_traceback["Lists_tb"].append( format_frame ( traceback_get_info(tb), number ) )
        
        number+=1
        tb = tb.tb_next
    
    return format_traceback


class AsyncLock:
    def __init__(self) -> None:
        self.locker = asyncio.Lock()
    
    async def release(self) -> None:
        """open the lock"""
        self.locker.release()
    
    async def acquire(self) -> None:
        """close the lock"""
        await self.locker.acquire()
    
    async def loadjson(self, path: str) -> dict:
        await self.acquire()
        return loadall_json(path)
    
    async def inputjson(self, path: str, db:dict) -> None:
        input_json(path, db)
        await self.release()
        