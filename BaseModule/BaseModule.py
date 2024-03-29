#!/usr/bin/env python3

import os
import sys
import time
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

from . import _vectors as vec 


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
    'load_json',
    'input_json',
    'loadall_json',
    "trackback_format",
    "drawLine",
    "cross",
    "memory",
    "are_crossing",
    "calculate_completion_time",
    "convert_seconds",
    "format_time"
    )

def calculate_completion_time(current_iteration, total_iterations, iteration_time):
    """
    This function calculates the estimated completion time for a task based on the current iteration, total iterations, and the time taken for each iteration.

    - current_iteration: The current iteration of the task (integer).
    - total_iterations: The total number of iterations for the task (integer).
    - iteration_time: The time taken for each iteration (float).

    Returns the estimated completion time in seconds.
    """
    return ( iteration_time*(total_iterations-current_iteration) )


def convert_seconds(seconds):
    """
    This function converts the given number of seconds into days, hours, minutes, and remaining seconds.

    - seconds: The number of seconds to convert (integer).

    Returns a tuple containing the number of days, hours, minutes, and seconds.
    """
    minutes = seconds // 60
    seconds %= 60
    hours = minutes // 60
    minutes %= 60
    days = hours // 24
    hours %= 24
    return days, hours, minutes, seconds

def format_time(time_list: "tuple[int, int, int, int]"):
    """
    This function formats the time units (days, hours, minutes, seconds) into a human-readable format.

    - time_list: A tuple containing the number of days, hours, minutes, and seconds (in that order).

    Returns a list of formatted time units, excluding units with a value of 0. If all units are 0, only the seconds unit is included.
    """
    time_units = ['день', 'час', 'мин', 'сек']
    formatted_time = []

    for i, unit in enumerate(time_list):
        if unit != 0:
            formatted_time.append(f'{int(unit)} {time_units[i]}')

    if len(formatted_time) == 4:
        formatted_time.pop()
    
    if sum(time_list) == 0:
        formatted_time.append(f"0 {time_units[-1]}")

    return formatted_time

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

class mdeque():
    def __init__(self, maxlen:int) -> None:
        self.__maxlen = maxlen
        self.__array = []  

    def __repr__(self) -> str:
        return "<BaseModule.BaseModule.mdeque handlers=[maxlen=%s, array=%r]>" % (self.__maxlen, self.__array)
    
    def __getitem__(self, __key: int):
        if isinstance(__key, int):
            return self.__array[__key]
        else:
            raise TypeError("please use `int` instead of `%s`" % __key.__class__.__name__)
    
    def __setitem__(self, __key: int, __value) -> None:
        if isinstance(__key, int):
            self.__array[__key] = __value
        else:
            raise TypeError("please use `int` instead of `%s`" % __key.__class__.__name__)

    def append(self, __object) -> None:
        if len(self.__array) >= self.__maxlen:
            del self.__array[0]
        self.__array.append(__object)     

    def converct(self) -> list:
        return self.__array
    


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
    
def load_json(derictory: str, *args) -> 'None | list':
    """getting specific key from json file"""
    if misfile(derictory) and len(args) != 0:
        with open(derictory, encoding="utf-8") as config_file:
            data: dict= json.load(config_file)
        data_info = [data[key] for key in args if key in data]
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

def SecTimeformat(time: int):
    "time.time() -> type(day, hour, minute, sec)"
    sec = int(time)

    minute = sec // 60
    hour = minute // 60
    day = hour // 24

    sec = sec % 60
    minute = minute % 60
    hour = hour % 24
        
    return (day, hour, minute, sec)

def drawLine(a: vec.Vector2D, b: vec.Vector2D, value: list, simble: str="-"):
    delta_x = abs(b.x - a.x)
    delta_y = abs(b.y - a.y)

    sign_x = 1 if a.x < b.x else -1

    sign_y = 1 if a.y < b.y else -1

    L = delta_x - delta_y
    while (a.x != b.x or a.y != b.y): 
        value[a.x][a.y] = simble

        L2 = L * 2
        
        if L2 > -delta_y: 
            L -= delta_y
            a.x += sign_x
        
        if L2 < delta_x:
            L += delta_x
            a.y += sign_y


def cross(a: vec.Vector2D, b: vec.Vector2D, c: vec.Vector2D, d: vec.Vector2D) -> "vec.Vector2D | None":
    def algoritm(a: vec.Vector2D, b: vec.Vector2D) -> "tuple[bool, vec.Vector2D]":
        f = b-a
        if 0 == f.x :
            return (False, )

        k = f.y/f.x
        b = a.y-(k*a.x)
        return (True, k, b)

    type_1, *t1 = algoritm(a, b)
    type_2, *t2 = algoritm(c, d)

    if type_1 is False or type_2 is False:
        return
    
    # function система уровнений 
    a = t1[0] - t2[0]
    if a == 0:
        return
    b = t1[1] - t2[1]

    x = -b/a
    y = t2[0]*x+t2[1]

    return vec.Vector2D(x, y)

def are_crossing(a: vec.Vector2D, b: vec.Vector2D, c: vec.Vector2D, d: vec.Vector2D) -> bool:
    "algorithm for determining the intersection of two segments"
    point_g = cross(a,b,c,d)
    if point_g is None:
        return False
    
    dis_ab = round(vec.distance(a, b), 2)
    dis_cd = round(vec.distance(c, d), 2)
    
    dis_a_g = vec.distance(a, point_g)
    dis_b_g = vec.distance(b, point_g)
    res = round( dis_a_g+dis_b_g, 2)

    if dis_ab != res:
        return False
    dis_c_g = vec.distance(c, point_g)
    dis_d_g = vec.distance(d, point_g)
    res = round( dis_c_g+dis_d_g, 2)

    if dis_cd != res:
        return False

    return True

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

def memory(func):
    """Cash the result of the function in save in file .pycash.json in __pycache__

    ```py
    @memory
    def sum(a, b) -> int:
        return a + b

    # Test 1 first
    sum(15, 43) # -> result 58 for "9 sec"

    # Test 2 second
    sum(15, 43) # -> result 58 for "0.01 sec"
    ```
    """
    if not misdir("./__pycache__/"):
        mkdir("./__pycache__")

    if not misfile("./__pycache__/.pycash.json"):
        open("./__pycache__/.pycash.json", "w").write("{}")
    
    cache = loadall_json("./__pycache__/.pycash.json")
    
    def wrapper(*args, **kwargs):
        name_function = f"{func.__name__} {str(args)} {str(kwargs)}"

        if name_function not in cache:
            cache[name_function] = func(*args, **kwargs)
            input_json("./__pycache__/.pycash.json", cache)
        
        return cache[name_function]
    
    return wrapper

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
        