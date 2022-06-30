#!/usr/bin/env python3

import os
import sys

import json
import yaml
import zipfile
import sqlite3


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
    'loadall_json')

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

def file_size(file_path):
    """getting file weight
    * getting the weight of the form [0-4, weight]"""
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
        with open(derictory, encoding="utf-8") as config_file:
            data = json.load(config_file)
        return data
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
        with open(derictory, encoding="utf-8") as config_file:
            data = yaml.load(config_file, Loader=yaml.FullLoader)
        return data
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
        except:
            return False
    return None

