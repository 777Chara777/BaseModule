from types import TracebackType

import inspect
import linecache
import ast
import traceback as tbs
import sys

def get_traceback_information(tb) -> dict:

    def get_relevant_names(tree):
        return [node for node in ast.walk(tree) if isinstance(node, ast.Name)]

    def format_value(v):
        try:
            v = repr(v)
        except KeyboardInterrupt:
            raise
        except BaseException:
            v = u'<unprintable %s object -_->' % type(v).__name__

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
    

    try:
        tree = ast.parse(source, mode='exec')
        relevant_values = get_relevant_values(tb.tb_frame, tree)
    except SyntaxError:
        relevant_values = []

    return {
        "FilePath": filename,
        "Line": lineno,
        "Function": function,
        "Source": source,
        "args": relevant_values
    }

def format_traceback_frame(data: dict, number: int=0) -> str:
    format_tb_str: str=''
    
    source = data["Source"]
    format_tb_str += '%i File "%s", line %i, in %s\n    %s' % (number, data["FilePath"], data["Line"], data["Function"], source)
    
    args:list = data["args"]
    args.reverse()


    if len(args) != 0:
        for num_line in range(len(args)):
            newline = ""

            for num_arg, arg in enumerate(args):
                name_func, line, func = arg

                line+=4
                name_func_len = len(name_func)

                name_func_value = 0

                if name_func_len != 1:
                    name_func_value = 1 if (name_func_len % 2 == 0 or name_func_len == 3) else 2

                format_number = int(num_arg+1) - int(num_line+1)

                if format_number == 0:
                    newline += str(' ' * (line+name_func_value)) + f"└─ {func}"
                
                elif format_number > 0:
                    newline_list = list(newline)
                    newline_list[line+name_func_value] = "│"
                    newline = ''.join(newline_list)

            
            format_tb_str+=f'\n{newline}'

    return format_tb_str

def _format_traceback(traceback: TracebackType=None, **kargs) -> dict:

    if traceback is None:
        traceback = sys.exc_info()[2]
        
    if "value" not in kargs:
        kargs["value"] = tbs.format_exception( *sys.exc_info() )[-1].replace("\n",'')

    format_traceback: dict={
        "Header": "Traceback (most recent call last):",
        "Description": [],
        "ErrorCaption": kargs["value"]
    }   

    number = 0
    while traceback:
        if number != 0: format_traceback["Description"].append( format_traceback_frame ( get_traceback_information(traceback), number ) )
        
        number+=1
        traceback = traceback.tb_next
    
    return format_traceback






# ┬ ↓ не использовать


# └ │ ─ ╤

# ╤
# │
# └─