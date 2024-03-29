![Logo](assets/main.png)

# BaseModule
## This mod is like a swiss knife

### install 
`git clone https://github.com/777Chara777/BaseModule.git`

### BaseModule.py
```py
mcls: int # -> clear console
mplatform_: str # -> your platform
misdir: bool # -> is dir
misfile: bool # -> is file
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
Time: str # -> get Time now 
get_size: str # -> you can check size file
file_size: list[int, str, int] # -> you can check size file
load_json: dict # -> save json file
input_json: bool # -> load json file 
loadall_json: dict # ->  load all info json file 
trackback_format: str # -> return trackback_format
```

### LogError.py
```py
from BaseModule._LogError_V3 import logerror 
from BaseModule._LogError_V3 import INFO, CRITICAL

# logerror.add > args
# - file -> save log in file
# 
# - format -> foramt message
#    - {time$} -> $ - type time. Use BaseModule.Time( num:int )
#    - {level} -> level log 'DEBUG/INFO/WARN/ERROR...'
#    - {function} -> shows call
#    - {coretype} -> core type
#    - {lencalls} -> show len calls function log
#    - {message} -> it's message
# 
# - color -> if false use 'print()' or true use 'rich.print()'
# 
# - defaultlevel -> the minimum level at which the log will output a message to the console
# 
# - default_core -> which core will be selected by default
# 
# - maxfilesize -> not working

logerror.add( file="logfile.log", format="{lencalls}\t {time3} | {coretype} {level}\t | {function} - {message}", color=True, defaultlevel=INFO, default_core="MAIN_CORE" )

logerror.savelog() # -> convert logfile in zip

logerror.info(message="test :)") # -> send "1       00-00-0000 00:00:00 | MAIN_CORE INFO      | __main__:<module>:1 - test :)"


# @logerror.catch > args
# - level = "ERROR" -> level send message
# - onerror = None -> will be called on error
# - message = "An error has occurred" -> error message
# - ignore_exceptions: tuple= (SystemExit,) -> ignore exeptions


#logerror.create_core -> you create or edit a core without accepting it. used only in 'ContextManager or with'

with logerror.create_core("NewCore") as core:
    # core > there are many functions
    # - setcolor  | getcolor
    # - setformat | getformat
    # - setfile   | getfile
    # - setlevel  | getleval
    core.setformat("{lencalls}\t @{level} !{function} > {message}")
    core.setcolor(False)


# Test 1
@logerror.catch(level=CRITICAL, mesage="error message")
def test():
    print(2 / 0)

test() # call function

# 2       00-00-0000 00:00:00 | MAIN_CORE CRITICAL      | __main__:<module>:1 - error message
# Traceback (most recent call last):

# 1 File "<stdin>", line 3, in test
#   print(2 / 0)

# ZeroDivisionError: division by zero



# Test 2 'with ignore_exceptions'
@logerror.catch(level=CRITICAL, message="error message", ignore_exceptions=(SystemExit, ZeroDivisionError,))
def test():
    print(2 / 0)

test() # call function

# 3       00-00-0000 00:00:00 | MAIN_CORE INFO      | __main__:<module>:1 - Ignor Exceptions: ZeroDivisionError 

```