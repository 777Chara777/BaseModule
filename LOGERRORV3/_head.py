import rich

def write(message, *args, color=False):
    _message = ''
    for x in args:
        _message+=f' {x}'
    mprint = print if not color else rich.print
    mprint(message + _message)
