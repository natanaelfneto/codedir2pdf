#!/usr/bin/python
import os

from shutil import *

from get_codeignore import *
from print_output import *


class SetPdfLocation(object):
    def __init__(self, ignoredlist, inputfolder, verbose):
        self.ignoredlist = ignoredlist
        self.folder = str(inputfolder)
        self.verbose = verbose
        self.pdf_folder = os.path.abspath(self.folder+'/pdf_folder/')

    def filter(self):
        echo = PrintVerbose(self.verbose) 
        echo.output('> destination pdf folder is: '+self.pdf_folder)
        if os.path.isdir(self.folder):
            echo.output('> checking if destination folder exist')
            if not os.path.isdir(self.pdf_folder):
                echo.output('> destination folder does not exist. creating ...')
                os.makedirs(self.pdf_folder)
        echo.output('> getting list of available files in :'+self.folder+' ...')
        for root, dirs, files in os.walk(self.folder, topdown=True):
            dirs[:] = [d for d in dirs if d not in self.ignoredlist[0]]
            for f in files:
                echo.output('> checking file: '+f+' ...')
                name, extension = os.path.splitext(str(f))
                echo.output('> filtering only PDF file ...') 
                if str(extension) == '.pdf':
                    echo.output('> pdf file origin '+os.path.abspath(f)+' ...')
                    echo.output('> checking file status ...')
                    if os.path.isfile(os.path.abspath(f)):
                        echo.output('> pdf destination '+os.path.join(self.pdf_folder, f)+' ...')
                        echo.output('> moving pdf file from origin to destination ...')
                        move(os.path.abspath(f),os.path.join(self.pdf_folder, f))
                    else:
                        echo.output('> skipping non-file...')
                else:
                    echo.output('> skipping non-pdf-file...')
            echo.output('> finished moving all pdf files to '+self.pdf_folder+' ...')
        
    def __del__(self):
        echo = PrintVerbose(self.verbose)
        echo.output('> pdf search task memory cleaned')