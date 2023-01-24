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
misfile: bool # -> 
mkdir # -> 
mlistdir: list # -> 
mlistdir2: list | str # ->
mremove # -> 
mgetlogin: str # -> 
mgetcwd: str # -> 
mrenamefile # -> 
mdirname: str # -> 
mismodules: bool # -> 
mutcnow: time.time # -> 
mpause # -> 
mdeque # -> 
mjoin: str|list # -> 
initModule: bool | __Module # -> 
reloadModule: __Module # -> 
input_yaml: bool # -> 
loadall_yaml: dict # -> 
connectdb # -> 
listtostr: str # -> 
timeformat: str # -> 
dictkey: list # -> 
dictitems: list # -> 
zipdecode # -> 
zipencore # -> 
Time: str # -> 
get_size: str # -> 
file_size: list[int, str, int] # -> 
load_json: dict # -> 
input_json: bool # -> 
loadall_json: dict # -> 
trackback_format: str # -> 
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