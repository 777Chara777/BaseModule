from ._get_frame import get_frame

def findmessage(mesasge: str, __findtext: str) -> bool:
    if mesasge.find(__findtext) != -1:
        return True
    return False

def findmessage_2(mesasge: str, __findtext: str) -> "int | bool":
    """return number or False"""
    if mesasge.find(__findtext) != -1:
        return mesasge.find(__findtext)
    return False


def _getframe(depth, number=0):
    frame = get_frame(depth + (4 + number))
    code = frame.f_code

    try:
        name = frame.f_globals["__name__"]
    except KeyError:
        name = None

    return (name, code.co_name, frame.f_lineno) 

# def _process_traceback(data: str) -> tuple:
#     traceback_list = []

#     for x in [x.replace("\n", '').split('  ') for x in data]:
#         for text in x:
#             if text != '':
#                 traceback_list.append(text)

#     traceback_message = traceback_list.pop(0)
#     error_raise = traceback_list.pop(-1)

#     return (traceback_message, error_raise, traceback_list)