![Logo](assets/main.png)

# BaseModule
## This mod is like a swiss knife

### install
```
git clone https://github.com/777Chara777/BaseModule.git
```

### BaseModule.py
```py
mcls: int # -> clear console
mplatform_: str # -> your platform
misdir: bool # -> i's dir
misfile: bool # -> i's file
mkdir # -> create dir
mlistdir: list # -> check files 
mlistdir2: list | str # -> check files v2
mremove # -> delete file
mgetlogin: str # -> user
mgetcwd: str # -> derectory
mrenamefile # -> rename file
mdirname: str # -> returns the directory component of a pathname
mismodules: bool # -> check module
mutcnow: time.time # -> return UTC time
mpause # -> in consile plause
mdeque # -> ...
mjoin: str|list # -> is join
initModule: bool | __Module # -> import module 
reloadModule: __Module # -> reload module
input_yaml: bool # -> save yml file
loadall_yaml: dict # -> load yml file 
connectdb # -> connect to database
listtostr: str # -> list to string
timeformat: str # -> time format
dictkey: list # -> extract keys from the dict
dictitems: list # -> extract items from the dict
zipdecode # -> decode zip file
zipencore # -> encode zip file
Time: str # -> get Time 
get_size: str # -> you can check size file
file_size: list[int, str, int] # -> you can check size file
load_json: dict # -> save json file
input_json: bool # -> load json file 
loadall_json: dict # ->  load all info json file 
trackback_format: str # -> return trackback_format
```

### LogError.py
```py
from BaseModule._LogError_V3 import logerror as logger

# file -> save log in file

# format -> foramt message
# - {time$} -> $ - type time. Use BaseModule.Time( num:int )
# - {level} -> level log 'DEBUG/INFO/WARN/ERROR...'
# - {function} -> shows call
# - {coretype} -> core type
# - {message} -> it's message

# color -> if false use 'print()' or true use 'rich.print()'

# defautlevel -> ...

# maxfilesize -> not working

logger.add( file="logfile.log", format="{time3} | {coretype} {level}\t | {function} - {message}", color=True, defautlevel="INFO" )

logger.savelog() # -> convert logfile in zip

logger.info(message="test :)") # -> send "00-00-0000 00:00:00 | _default INFO      | __main__:<module>:1 - test :)"


@logger.catch
def test():
    print(0 / 2)

test() 
# 00-00-0000 00:00:00 | _default ERROR      | __main__:<module>:1 - An error has occurred
# Traceback (most recent call last):

# 1 File "<stdin>", line 3, in test
#   print(0 / 2)

# ZeroDivisionError: division by zero

```