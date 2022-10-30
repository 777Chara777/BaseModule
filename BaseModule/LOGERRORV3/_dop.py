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