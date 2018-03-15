#!/usr/bin/python
import argparse

import os, sys, getopt

# from pathlib import Path

from code2pdf import *

__version__ = "0.0.1"


class CodeFolder2Pdf(object):
    def __init__(self, argv):
        self.__argv = argv
    
    # def convert_files(self):


    def loop_inputfolder(self):
        if self.verbose:
            print '> checking input folder',self.inputfolder
        if os.path.isdir(self.inputfolder):
            if self.verbose:
                print('> input name is a valid folder ...')
                print('> lopping through files and sub directories ...')
            for root, dirs, files in os.walk(self.inputfolder):
                if self.verbose:
                    print('> ignoring file formats in .codeignore ...')
                for f in files:
                    if self.verbose:
                        print('> converting each file content found into PDF file ...')
                    if f.endswith('.pyc'):
                        if self.verbose:
                            print(str(f)+' ignored')
                    elif f.endswith('.pdf'):
                        if self.verbose:
                            print(str(f)+' ignored')
                    elif f.endswith('.codeignore'):
                        if self.verbose:
                            print(str(f)+' ignored')
                    elif f.endswith('.gitignore'):
                        if self.verbose:
                            print(str(f)+' ignored')
                    else:
                        if self.verbose:
                            print('> converting'+str(f)+' file into PDF file ...')
                        code2pdf = Code2Pdf(str(f))
                        code2pdf.init_print()
                        if self.verbose:
                            print('> converting'+str(f)+' file into PDF file OK ...')
                print('CodeFolder2PDF is done')
        else:
            print('error: the argument passed is not a valid directory')
            if self.verbose:
                print('> use . for local folder or /full/folder/path to diferent locations ...')
                print(self.help_message)
        if self.verbose:
            print('> all founded files loop is finished ...')


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
            sys.exit(2)
        for opt, arg in opts:
            if opt == '-h':
                print(self.help_message)
                sys.exit()
            elif opt == '-i':
                self.inputfolder = arg
                self.loop_inputfolder()
            elif opt == '-v':
                print 'version 0.0.1'
                sys.exit()
            elif opt == '-V':
                self.verbose = True

if __name__ == "__main__":
    c = CodeFolder2Pdf(sys.argv[1:])
    c.main()
