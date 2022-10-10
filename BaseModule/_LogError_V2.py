from . import BaseModule as bm

import rich
import inspect


class LogError_V2:
    """
    commads Arguments : --onreture, --noprint
    """
    import time
    __version__ = '0.0.3'
    _startTime = time.time()

    # class TypesList(Enum):
    #     CRITICAL = 50
    #     ERROR = 40
    #     WARNING = 30
    #     INFO = 20
    #     DEBUG = 10

    TypesList = {
        'CRITICAL': 50,
        'ERROR': 40,
        'WARNING': 30,
        'INFO': 20,
        'DEBUG': 10
    }

    inv_TypesList = {v: k for k, v in TypesList.items()}
    
    class ErrorClass:
        class ErrorNoneLogger(Exception): pass
        class ErrorNotFindArgument(Exception): pass
        class ErrorNotBool(Exception): pass
        class ErrorLanguageNotExists(Exception): pass
        class TypesList(Exception): pass

    class logger:
        def __init__(self, FileName: str=None, languagemodule: str='eng', format:str='', \
            color: bool=False, messagelavel: 'LogError_V2.ErrorClass.TypesList' = None ) -> None:
            """
            #### Init commands Logger:
            LanguageModule: `rus|eng`
            format: this is the format of your message. attributes
                * {time%num%} - Time -> This is the number for the output type you can look at Time(%num%)
                * {level} - Message type [`DEBUG|INFO|WARNING|ERROR|CRITICAL`]
                * {message} - Your message \n
            color: `True|False` - support for the rich module.\n
            #### Commands Logger:
            Regular commands `debub|info|warn|error|crit`\n
            SaveConfig and WithSaveConfig commands `it's Regular commands and "rename"`
                * rename - Save the file as `filename{datetime}.zip` it's defaut format.`
            """
            self.TypeColor = color
            self.FileName = FileName
            self.lastLang = languagemodule
            self.defautformat = format
            self.PrefixLog = lambda : {
                'DEBUG': self.LanguageModule['PrefixLog']['DEBUG'],
                'INFO': self.LanguageModule['PrefixLog']['INFO'],
                'WARNING': self.LanguageModule['PrefixLog']['WARNING'],
                'ERROR': self.LanguageModule['PrefixLog']['ERROR'],
                'CRITICAL': self.LanguageModule['PrefixLog']['CRITICAL'],
            }
            self.defautlevel = int(LogError_V2.TypesList["WARNING"]) if messagelavel is None else int(messagelavel)
            
            self.LanguageModule = self.langmodule(languagemodule)

            

        def langmodule(self, lang:str, data_lang: dict=None) -> 'dict | LogError_V2.ErrorClass.ErrorLanguageNotExists':
            data = {
                'eng': {
                    'PrefixLog': {
                        'DEBUG': 'Debug',
                        'INFO': 'Info',
                        'WARNING': '[orange1]WARNING[/orange1]',
                        'ERROR': '[red]ERROR[/red]',
                        'CRITICAL': '[red3]CRITICAL[/red3]' 
                    },
                    'LangModule': {
                        'ReplaceLang': 'Changed language to `{0}`',
                        'ErrorNoFindLang': 'No such language exists `{0}`'
                    },
                    'ClassError': {
                        'ErrorArgument': 'No Find Argument {0}',
                        'ErrorArgumentNotFind': 'Argument not found: `{0}`',
                        'ErrorNotBool': "it's `{0} - {1}` not bool argument",
                        'ErrorNotFindName': 'Not find name in {0}'
                    }
                }, 
                'rus': {
                    'PrefixLog': {
                        'DEBUG': '[blue]Дебаг[/blue]',
                        'INFO': '[blue]Информацыя[/blue]',
                        'WARNING': '[yellow]ПРОЕДУПРЕЖДЕНИЕ[/yellow]',
                        'ERROR': '[red]ОШИБКА[/red]',
                        'CRITICAL': '[red]КРИТИЧЕСКАЯ ОШИБКА[/red]' 
                    },
                    'LangModule': {
                        'ReplaceLang': 'Язык изменён на `{0}`',
                        'ErrorNoFindLang': 'Такого языка не существует `{0}`'
                    },
                    'ClassError': {
                        'ErrorArgument': 'Не найден аргумент {0}',
                        'ErrorArgumentNotFind': 'Аргумент не найден: `{0}`',
                        'ErrorNotBool': "Это `{0} - {1}` не bool аргумент",
                        'ErrorNotFindName': 'Не найден название в {0}'
                    }
                }
            }   
            if data_lang is not None:
                data.update(data_lang)

            if lang in data:
                if self.lastLang != lang:
                    self.info(str(data[self.lastLang]['LangModule']['ReplaceLang']).format(lang))
                    self.lastLang = lang
                return data[lang]
            else:
                self.error(str(data['eng']['LangModule']['ErrorNoFindLang']).format(lang))
                self.lastLang = 'eng'
                return data['eng']
        
        def restart_lang(self, lang:str, data:dict=None) -> 'dict | None':
            self.LanguageModule = self.langmodule(lang,data)
            return self.LanguageModule

        def _log(self, level, msg, *args, **kargs):
            printon = True
            returnon = False

            current_frame = inspect.currentframe()
            caller_frame = current_frame.f_back
            code_obj = caller_frame.f_code
            code_obj_name = code_obj.co_name

            print(__file__, __name__, code_obj_name)

            mprint = print if not self.TypeColor else rich.print
            if int(level) >= int(self.defautlevel):
                listargs = ['--noprint', '--onreture']
                listkargs = ['format']
                if '--noprint' in args:
                    printon = False
                if '--onreture' in args:
                    returnon = True
                if [x for x in args] in listargs and len(args) != 0:
                    raise LogError_V2.ErrorClass.ErrorNotFindArgument(str(self.LanguageModule['ClassError']['ErrorArgument']).format(['' if x in listargs else x for x in args]))
                
                if 'format' in kargs or self.defautformat.strip() != '':
                    if 'format' in kargs:
                        message = kargs['format']
                    elif self.defautformat.strip() != '':
                        message = self.defautformat

                    if message.find('{leval}') != -1:
                        message = message.replace('{leval}', self.PrefixLog()[LogError_V2.inv_TypesList[level]])

                    if message.find('{message}') != -1:
                        message = message.replace('{message}', msg)

                    if message.find('{time') != -1 and message[message.find('{time') + 6] == "}":
                        number = int( message[ message.find('{time') + 5 ] )
                        text = f'{{time{number}}}'
                        message = message.replace(text, str(bm.Time(number)))

                    if printon:
                        mprint(message)
                    else:
                        return message
                    if returnon:
                        return message

                elif len(kargs) != 0 and kargs not in listkargs:
                    raise LogError_V2.ErrorClass.ErrorNotFindArgument(str(self.LanguageModule['ClassError']['ErrorArgumentNotFind']).format(" ".join(bm.dictkey(kargs))))

                else:
                    if printon:
                        mprint(self.PrefixLog()[LogError_V2.inv_TypesList[level]], msg)    
                    else:
                        return f'{self.PrefixLog()[LogError_V2.inv_TypesList[level]]} {msg}'
                    if returnon:
                        return f'{self.PrefixLog()[LogError_V2.inv_TypesList[level]]} {msg}'
                    

        def debug(self, msg, *args, **kargs):
            info = self._log(LogError_V2.TypesList["DEBUG"], msg, *args, **kargs)
            if info != None:
                return info
        
        def info(self, msg, *args, **kargs):
            info = self._log(LogError_V2.TypesList["INFO"], msg, *args, **kargs)
            if info != None:
                return info

        def warn(self, msg, *args, **kargs):
            info = self._log(LogError_V2.TypesList["WARNING"], msg, *args, **kargs)
            if info != None:
                return info

        def error(self, msg, *args, **kargs):
            info = self._log(LogError_V2.TypesList["ERROR"], msg, *args, **kargs)
            if info != None:
                return info

        def crit(self, msg, *args, **kargs):
            info = self._log(LogError_V2.TypesList["CRITICAL"], msg, *args, **kargs)
            if info != None:
                return info
        
    class _LogSave(logger):

        def __init__(self, file, languagemodule:str, format:str, color:bool, *args, **kargs) -> None:
            super().__init__(None)
            LogError_V2.logger.__init__(self, None)
            self.lastdefautlevel = self.defautlevel
            self.defautlevel = LogError_V2.TypesList['DEBUG']
            self.args = args
            self.kargs = kargs
            self.filename = file
            self.defautformat = format
            self.TypeColor = color
            self.LanguageModule = self.restart_lang(languagemodule)

        def debug(self, msg, *args, **kargs):
            # self.savefile.write(str(super().debug(msg, '--onreture', *args, **kargs))+'\n')
            if self.lastdefautlevel > self.defautlevel:
                args += ('--noprint',)
            with open(self.filename, mode=self.kargs['mode'], encoding=self.kargs['encoding']) as savefile:
                savefile.write(str(super().debug(msg, '--onreture', *args, **kargs))+'\n')

        def info(self, msg, *args, **kargs):
            # self.savefile.write(str(super().info(msg, '--onreture', *args, **kargs))+'\n')
            if self.lastdefautlevel > self.defautlevel:
                args += ('--noprint',)
            with open(self.filename, mode=self.kargs['mode'], encoding=self.kargs['encoding']) as savefile:
                savefile.write(str(super().info(msg, '--onreture', *args, **kargs))+'\n')

        def warn(self, msg, *args, **kargs):
            # self.savefile.write(str(super().warn(msg, '--onreture', *args, **kargs))+'\n')
            if self.lastdefautlevel > self.defautlevel:
                args += ('--noprint',)
            with open(self.filename, mode=self.kargs['mode'], encoding=self.kargs['encoding']) as savefile:
                savefile.write(str(super().warn(msg, '--onreture', *args, **kargs))+'\n')

        def error(self, msg, *args, **kargs):
            # self.savefile.write(str(super().error(msg, '--onreture', *args, **kargs))+'\n')
            if self.lastdefautlevel > self.defautlevel:
                args += ('--noprint',)
            with open(self.filename, mode=self.kargs['mode'], encoding=self.kargs['encoding']) as savefile:
                savefile.write(str(super().error(msg, '--onreture', *args, **kargs))+'\n')
        
        def crit(self, msg, *args, **kargs):
            # self.savefile.write(str(super().crit(msg, '--onreture', *args, **kargs))+'\n')
            if self.lastdefautlevel > self.defautlevel:
                args += ('--noprint',)
            with open(self.filename) as savefile:
                savefile.write(str(super().crit(msg, '--onreture', *args, **kargs))+'\n')
        
        def resave(self, selflogger: 'LogError_V2.logger', filename:str='', *args, **kargs):
            self.FileName = selflogger.FileName
            self.defautformat = selflogger.defautformat
            
            def savefile(filename:str):
                start = bm.Time(6)
                file = filename.split('.')[-2]
                format_file = f"{file}-{start}.gz"
                bm.zipencore(filename, format_file)
                open(filename, 'w')

            self.info('Save File', **kargs)

            savefile(filename) if str(filename).strip() != '' else savefile(self.FileName)

    class SaveConfig(_LogSave):
        def __init__(self, LoggerSelf: 'LogError_V2.logger', filename: str='', mode:str='a+', encoding='utf-8', **kargs) -> None:
            if filename.strip() != '':
                if not bm.misfile(filename): open(filename, 'w')

                # self.file = open(filename, mode, encoding=encoding, **kargs)
                # super().__init__(self.file, LoggerSelf.lastLang, '', LoggerSelf.TypeColor)
                super().__init__(filename, LoggerSelf.lastLang, '', LoggerSelf.TypeColor, mode=mode,encoding=encoding)
            else:
                if not bm.misfile(LoggerSelf.FileName):
                    open(LoggerSelf.FileName, 'w')
                # print( LoggerSelf.lastLang, LoggerSelf.defautformat, LoggerSelf.TypeColor)
                # self.file = open(LoggerSelf.FileName, mode, encoding=encoding, **kargs)
                filename = LoggerSelf.FileName
                # super().__init__(self.file, LoggerSelf.lastLang, LoggerSelf.defautformat, LoggerSelf.TypeColor)
                super().__init__(filename, LoggerSelf.lastLang, LoggerSelf.defautformat, LoggerSelf.TypeColor, mode=mode,encoding=encoding)

        # def __del__(self) -> None:
        #     self.file.close()


    class WithSaveConfig():
        def __init__(self, LoggerSelf: 'LogError_V2.logger', filename: str='', mode:str='a+', encoding='utf-8', **kargs):
            self._typesave = True
            self.kargs = kargs
            self.LoggerSelf = LoggerSelf
            self.filename = filename
            self.mode = mode
            self.encoding = encoding

            self.ziptype = False
            if 'ziptype' in self.kargs:
                if isinstance(self.kargs['ziptype'], bool):
                    self.ziptype = self.kargs['ziptype']
                else:
                    raise LogError_V2.ErrorClass.ErrorNotBool(str(LoggerSelf.LanguageModule['ClassError']['ErrorNotBool']).format(self.kargs['ziptype']))

        def __enter__(self):
            def __sizetest(path:str):
                if bm.file_size(path)[0] and self.ziptype:
                    with open(path, 'r', encoding="UTF-8") as save_file_to_zit:
                        file_to_zip = save_file_to_zit.read()
                    open(path, 'w')
                    zipped = file_to_zip
                    with open('.'.join(path.split('.')[:-1])+f'-{bm.Time(1)}.gz', 'w') as zip_save:
                        zip_save.write(zipped)
                        zip_save.close()

            if self.filename.strip() != '':
                if not bm.misfile(self.filename): open(self.filename, 'w')
                __sizetest(self.filename)

                self.file = open(self.filename, mode=self.mode, encoding=self.encoding)
                # return LogError_V2._LogSave(self.file, '')
                return LogError_V2._LogSave(self.file, self.LoggerSelf.lastLang, '', self.LoggerSelf.TypeColor)
            else:
                if self.LoggerSelf.FileName != None:
                    if not bm.misfile(self.LoggerSelf.FileName): open(self.LoggerSelf.FileName, 'w')
                    __sizetest(self.LoggerSelf.FileName)

                    self.file = open(self.LoggerSelf.FileName, mode=self.mode, encoding=self.encoding)
                    return LogError_V2._LogSave(self.file, self.LoggerSelf.lastLang, self.LoggerSelf.defautformat, self.LoggerSelf.TypeColor)
                else:
                    raise LogError_V2.ErrorClass.ErrorNoneLogger(str(self.LoggerSelf.LanguageModule['ClassError']['ErrorNotFindName']).format(self.filename.__class__))

        def __exit__(self, exc_type, exc_value, tb):
            self.file.close()