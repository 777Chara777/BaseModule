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




Mein neues Zuhause

geschrieben am 17. September von Mira im Norden

Jetzt lebe ich also hier und es ist eigentlich ganz gut. Wir sind vor drei Monaten wegen meiner Mutter ziemlich spontan nach Kiel gezogen. Als meine Eltern uns vor einiger Zeit verkündet haben, dass wir bald umziehen würden, war ich erst mal total geschockt. Meine Mutter war schon langer nicht mehr so richtig zufrieden mit ihrer Arbeit und ich wusste, dass sie eine neue Stelle s sucht. Aber irgendwie habe ich den Gedanken immer verdrängt, dass wir möglicherweise aus unserem schönen kleinen Ort wegziehen. Nun hatte sie also eine neue Stelle an der Uniklinik in Kiel bekommen und sollte schon im nächsten Monat anfangen. Da mein Vater als Übersetzer arbeitet und sowieso immer zu Hause am Schreibtisch sitzt, ist für ihn ein Umzug kein Problem, Er nimmt seine Arbeit einfach mit. Ich konnte mir überhaupt nicht vorstellen, meine Freunde und 10 meine Schule zu verlassen. Mein Bruder und ich waren ziemlich verzweifelt. Aber was soll man machen, wenn man erst 16 ist! Wir mussten uns also irgendwie an den Gedanken gewöhnen. Und dann gab es viel zu organisieren. Meine Eltern führen mehrmals nach Kiel, um eine neue Wohnung für uns zu suchen. Mein Bruder und ich haben uns im Internet über die Schulen dort informiert und sind dann einmal mit unseren Eltern dorthin gefahren, um uns anzumelden. Dann mussten wir unsere Zimmer ausmisten. So ein Umzug ist ja eine gute Gelegenheit, um endlich

mal den alten Kram, den man nicht mehr braucht, wegzuschmeißen. Die letzten Wochen waren

dann hart. Ich musste mich von meinem Sportverein abmelden und mich von meinen Freunden

verabschieden. Das war ganz schrecklich und ich habe viel geweint. Aber als wir dann endlich im

Auto nach Kiel saßen, habe ich mich plötzlich auch ein bisschen auf mein neues Leben gefreut.

20 Der Anfang in einer neuen Stadt ist natürlich schwierig. Am ersten Tag bin ich sehr aufgeregt in

die neue Schule gegangen. Ich hatte Angst, dass ich keinen Anschluss finde und für immer allein

sein werde. Und die ersten Wochen waren wirklich schwierig. Ich kannte die Abläufe an der

neuen Schule nicht und ich vermisste meine alten Freunde. Aber nach ein paar Wochen freundete

Ich mich mit zwei supernetten Mädchen an und dann ging alles besser. Paula und Lilli zeigten mir

25 auch die Stadt. Ich wusste also ziemlich schnell, wo die beste Eisdiele ist und wo es die coolsten

T-Shirts gibt. Und Kiel ist im Sommer toll. Man kann ans Meer gehen, am Strand sitzen,

schwimmen gehen und große Schiffe anschauen. Ich habe sogar beschlossen, dass ich segeln lernen will. Gut, oder? Außerdem ist in Kiel auch mehr los ais in meinem alten Ort. Unsere neue Wohnung ist auch ganz schön. Mein neues Zimmer ist viel größer als mein altes. Insgesamt kann 30 ich sagen, dass der Umzug für mich eigentlich gut war. Ich habe viele neue Erfahrungen gemacht. Es ist nicht so einfach, wenn man neu in der Schule und in einer Stadt ist, aber man entwickelt sich dadurch auch weiter. Manchmal habe ich Sehnsucht nach meinem alten Leben. Aber ich skype oft mit meinen alten Freunden und in den Herbstferien kommt meine beste Freundin nach Kiel, um mich zu besuchen. Darauf warte ich schon sehnsüchtig