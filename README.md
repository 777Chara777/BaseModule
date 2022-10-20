![Logo](assets/main.png)

# BaseModule
## This mod is like a swiss knife

### install
```
git clone https://github.com/777Chara777/BaseModule.git
```

### BaseModule.py
```py
from BaseModule._LogError_V3 import logerror as logger

# file -> save log in file

# format -> foramt message
# - {time$} -> $ - type time. Use BaseModule.Time( num:int )
# - {level} -> level log 'DEBUG/INFO/WARN/ERROR...'
# - {function} -> shows call
# - {message} -. it's message

# color -> if false use 'print()' or true use 'rich.print()'

# defautlevel -> ...

# maxfilesize -> not working

logger.add( file="logfile.log", format="{time3} | {level}\t | {function} - {message}", color=True, defautlevel="INFO" )

logger.savelog() # -> convert logfile in zip

logger.info(message="test :)") # -> send "00-00-0000 00:00:00 | INFO\t | __main__:<module>:1 - test :)"


@logger.catch
def test():
    print(0 / 2)

test() 
# 00-00-0000 00:00:00 | ERROR      | __main__:<module>:1 - An error has occurred
# Traceback (most recent call last):

# 1 File "<stdin>", line 3, in test
#   print(0 / 2)

# ZeroDivisionError: division by zero

```