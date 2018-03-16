#!/usr/bin/python
import os

from get_codeignore import *
from print_output import *


class LoopThroughFolders(object):
    def __init__(self, inputfolder, verbose, help_message):
        self.folder = str(inputfolder)
        self.verbose = verbose
        self.help = help_message

    def folders(self):
        echo = PrintVerbose(self.verbose)
        if os.path.isdir(self.folder):
            echo.output('> input name is a valid folder ...')
            echo.output('> looking for .codeignore file in the input folder ...')
            if os.path.isfile(os.path.abspath(self.folder+'/.codeignore')):
                echo.output('> get absolute path of .codeignore file ...')
                ignorefile = os.path.abspath(self.folder+'/.codeignore')
                echo.output('> setting exclude directories ...')
                ignorelist = GetIgnoredFiles(ignorefile, self.verbose).get_codeignore()
            else:
                echo.output('> there is no .codeignore file in input folder')
            if self.verbose:
                echo.output('> lopping through files and sub directories ...')
        else:
            print('> error: the argument passed is not a valid directory')
            echo.output('> use . for local folder or /full/folder/path to diferent locations')
            echo.output(self.help)
            sys.exit()
        echo.output('> all founded files loop is finished')

        return ignorelist
        
    def __del__(self):
        echo = PrintVerbose(self.verbose)
        echo.output('> loop task memory cleaned')