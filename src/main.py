#!/usr/bin/python
import os, sys, getopt

from codelib import *
from loopfolder import *
from get_codeignore import *
from pdf_location import *
from print_output import *

__version__ = "0.0.2"


class File2Pdf(object):
    def __init__(self, ignoredlist, inputfolder, verbose):
        self.exclude = ignoredlist
        self.folder = inputfolder
        self.verbose = verbose

    def files2pdf(self, filename):
        echo = PrintVerbose(self.verbose)
        echo.output('> separating file extentions from file name ...')
        name, extension = os.path.splitext(str(filename))
        echo.output('> converting each file content found into PDF file ...') 
        if str(extension) in self.exclude[1] or str(name) in self.exclude[1]:
            echo.output('> ignoring PDF cnovertion of '+str(filename))
        else:
            code2pdf = Code2Pdf(str(filename), self.verbose)
            echo.output('> converting '+str(filename)+' to PDF ...') 
            code2pdf.init_print()
            echo.output('> converting is almost finished ...')
        echo.output('> converting'+str(filename)+' file into PDF file OK ...')

    def convert(self):
        echo = PrintVerbose(self.verbose)
        echo.output('> looping through root, directories and files content ...')
        for root, dirs, files in os.walk(self.folder, topdown=True):
            dirs[:] = [d for d in dirs if d not in self.exclude[0]]
            echo.output('> ignoring sub directories in .codeignore file ...')
            for f in files:
                echo.output('> file: '+f)
                self.files2pdf(f)
            echo.output('> CodeFolder2PDF is almost finished ...')
        echo.output('> CodeFolder2PDF is finished ...')
        
    def __del__(self):
        echo = PrintVerbose(self.verbose)
        echo.output('> CodeFolder2PDF task memory cleaned')


class CodeFolder2Pdf(object):
    def __init__(self, argv):
        self.__argv = argv

    def main(self):
        self.error_message = "invalid arguments were passed ..."
        self.help_message = "CodeFolder2PDF\nusage: pyhton code2pdf.py -[ opt ] [<inputfolder>]\n\n\
    -h                  Output this help message.\n\
    -i  <inputfolder>   Get all files in directory and its sub directories and convert to PDF.\n\
    -v                  Output the current module version.\n\
    -V                  Set verbose flag to True.\n"
        self.inputfolder = ''
        self.outputfile = ''
        self.verbose = False
        try:
            opts, args = getopt.getopt(self.__argv,"hi:vV")
        except getopt.GetoptError:
            print(self.error_message)
            print(self.help_message)
            sys.exit()
        for opt, arg in opts:
            if opt == '-h':
                print(self.help_message)
                sys.exit()
            elif opt == '-i':
                self.inputfolder = arg
                loop = LoopThroughFolders(
                    self.inputfolder,
                    self.verbose, 
                    self.help_message
                    )
                self.ignoredlist = loop.folders()
                filteredfiles = File2Pdf(
                    self.ignoredlist,
                    self.inputfolder,
                    self.verbose, 
                    )
                filteredfiles.convert()

                pdf = SetPdfLocation(
                    self.ignoredlist,
                    self.inputfolder,
                    self.verbose,
                )

                pdf.filter()

            elif opt == '-v':
                print 'version 0.0.1'
                sys.exit()
            elif opt == '-V':
                self.verbose = True


if __name__ == "__main__":
    c = CodeFolder2Pdf(sys.argv[1:])
    c.main()
