#!/usr/bin/python
from print_output import *


class GetIgnoredFiles(object):
    def __init__(self, codeignore_file, verbose):
        self.codeignore_file = str(codeignore_file)
        self.verbose = verbose

    def get_codeignore(self):
        echo = PrintVerbose(self.verbose)
        echo.output('> reading codeignore as file ...')
        with open(self.codeignore_file) as f:
            echo.output('> reading all lines from file ...')
            content = f.readlines()
            echo.output('> removing line breaks from content ...')
            content = [x.strip() for x in content]
            isdir = ''
            echo.output('> looping through each line for getting directories and files')
            for line in content:
                if "#directories:" in line:
                    dir_list = []
                    isdir = True
                elif "#files:" in line:
                    file_list = []
                    isdir = False
                if isdir and "#directories:" not in line and line != '' and len(line) > 2:
                    echo.output('> '+line+' saved as directory')
                    dir_list.append(line)
                elif not isdir and "#files:" not in line and line != '' and len(line) > 2:
                    file_list.append(line)
                    echo.output('> '+line+' saved as file')
            content_list = [dir_list, file_list]

        return content_list
        
    def __del__(self):
        echo = PrintVerbose(self.verbose)
        echo.output('> check for content from .codeignore file is done')