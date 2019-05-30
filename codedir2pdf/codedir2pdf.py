#!/usr/bin/env python
from __future__ import print_function

# project name
__project__ = "codedir2pdf"

# project version
__version__ = "1.0"

# prohect author
__author__ = "natanaelfneto"
__authoremail__ = "natanaelfneto@outlook.com"

# project source code
__source__ = "https://github.com/natanaelfneto/codedir2pdf"

# project general description
__description__ = '''


# Author - Natanael F. Neto <natanaelfneto@outlook.com>
# Source - https://github.com/natanaelfneto/codedir2pdf.git
'''

# project short description
short_description = ""

# python imports
import argparse
import getpass
import logging
import pathlib
import os
import sys
import time
# third party imports
from codedir2pdf.code2pdf import Code2pdf


# 
class SourceValidator(object):
    '''
    Check for source path if the files are accessible and are actually files
    '''

    # path validity init
    def __init__(self):
        ''' 
            Initiate a Path Validator instance.
        '''

        # get loggert on a self instance
        self.logger = logger.adapter
        
    # path validity checker function
    def validate(self, source):
        '''
            Function to check if each parsed path is a valid source code file
            and if it can be accessed by this code.

            Arguments:
                paths: folder path to be checked
        '''

        # set basic variable for valid files
        valid_files = []

        # loop check through parsed path
        self.logger.debug('Checking validity of inputed source')

        # check if input is a list of files
        if isinstance(source, list):

            # for each file founded
            for filename in source:

                # update valid files
                valid_files += self.validate_helper(root=None, filename=filename)

        else:
            # get files inside current path
            for root, dirs, files in os.walk(source):

                # check if folder is not empty
                if files:
                    
                    # for each file founded
                    for filename in files:

                        # update valid files
                        valid_files += self.validate_helper(root, filename)
        
        # return all parsed valid files
        return valid_files

    # 
    def validate_helper(self, root, filename):
        '''
        Helper to validade files as DRY conformity
        '''

        # set basic variable for valid files
        valid_files = []

        # get absolute path
        if root:
            file = os.path.abspath(os.path.join(root, filename))
        else:
            file = os.path.abspath(filename)

        # append path if it exists, is accessible and is a file
        if os.access(file, os.F_OK) and os.access(file, os.R_OK) and os.path.isfile(file):

            if not quiet_flag:
                output = "Source path {0} was successfully parsed".format(file)
            else:
                output = "A source path was successfully parsed"
            
            # log output
            self.logger.debug(output)

            # append valid file to array
            valid_files.append(file)

        # if not, log the error
        else:
            if not quiet_flag:
                output = "Source path {0} could not be accessed as a file".format(file)
            else:
                output = "A source path could not be accessed as a file"

            # log output
            self.logger.debug(output)
    
        # return all parsed valid files
        return valid_files
    

# class for logger instancies and configurations
class Logger(object):

    # path validity init
    def __init__(self, folder=None, format=None, extra=None, debug_flag=False, quiet_flag=False):
        ''' 
            Initiate a Logger instance.
            Argument:
                logger: a logging instance for output and log
        '''

        # 
        log = {
            # setup of log folder
            'folder': folder,
            # set logging basic config variables
            'level': 'INFO',
            # 
            'date_format': '%Y-%m-%d %H:%M:%S',
            # 
            'filepath': folder+'/'+__project__+'.log',
            #
            'format': format,
            # extra data into log formatter
            'extra': extra
        }

        # set log name
        logger = logging.getLogger(__project__+'-'+__version__)

        # set formatter
        formatter = logging.Formatter(log['format'])

        # check debug flag
        if debug_flag:
            logger.setLevel('DEBUG')
        else:
            logger.setLevel('INFO')

        # check if log folder exists
        if not os.path.exists(log['folder']):
            if not quiet_flag:
                print("Log folder: {0} not found".format(log['folder']))
            else:
                print("Log folder not found")
            try:
                os.makedirs(log['folder'])
                if not quiet_flag:
                    print("Log folder: {0} created".format(log['folder']))
                else:
                    print("Log folder created")
            except Exception  as e:
                if not quiet_flag:
                    print("Log folder: {0} could not be created, error: {1}".format(log['folder'], e))
                else:
                    print("Log folder could not be created.")
                sys.exit()

        # setup of file handler
        file_handler = logging.FileHandler(log['filepath'])     
        file_handler.setFormatter(formatter)

        # setup of stream handler
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)

        # add handler to the logger
        logger.addHandler(file_handler)
        logger.addHandler(stream_handler)

        # update logger to receive formatter within extra data
        logger = logging.LoggerAdapter(logger, log['extra'])

        self.adapter = logger


# retrieve path to gitignore file from source
def get_gitignore_path(source):
    '''
    Argument(s):
        source: array of one or mode files and folders to be converted to pdf
    '''

    # aux variable
    path = None

    # get gitignore file inside source path
    for root, dirs, files in os.walk(source):
        # check if any file was found
        if files:
            # for each file founded
            for filename in files:
                if filename == '.gitignore':
                    # get absolute path
                    path = os.path.abspath(os.path.join(root, filename))
    
    # 
    return path


# retrieve content from gitignore file from source
def get_ignored(gitignore):
    '''
    Argument(s):
        gitignore: path to .gitignore file at source folder
    '''

    # aux variable
    content = None

    # base path from gitignore.io file
    base_path = os.path.dirname(__file__)

    # base parent path from gitignore.io file
    base_parent = os.path.abspath(os.path.join(base_path, os.pardir))

    # path to gitignore aux file source file
    gitignore_io = '{0}/assets/source.gitignore'.format(base_parent)

    # filter array substring
    _filter = [
        '!', '#', '[', ']',
        '$', '~', '@', '&',
        ':', ',', '{', '}'
    ]

    _extended = [
        '.git', '.md', '.txt', '.log', '.info',
        '.png', '.jpg', '.gif', '.psd', '.bmp',
        '__init__'
    ]

    # open and read gitignore.io file from assets
    with open(gitignore_io, 'r') as gitignore_io:

        # get raw content excuding line breakers
        raw = gitignore_io.read().splitlines()

        # filter empty items
        content = list(filter(None, raw))

        # filter commentaries
        gitignore_io_filter = [ line for line in content if not '#' in line ]

    # open and read gitignore file from project
    with open(gitignore, 'r') as gitignore:
        
        # get raw content excuding line breakers
        raw = gitignore.read().splitlines()
        
        # filter empty items
        content = list(filter(None, raw))
        
        # filter commentaries
        content = [ line for line in content if not '#' in line ]
        
        # filter items that contains matchiing substrings of filter array
        content = [ line for line in content if not any(f in line for f in _filter) ]
        
        # add not registable files to array if not present
        content.extend(gitignore_io_filter)
        content.extend(_extended)
        
    # 
    return content


# 
def list_files(dir):
    '''
    '''

    # aux variable
    r = []

    # walk through root, dirs and files
    for root, dirs, files in os.walk(dir):
        # get filenames
        for filename in files:
            # append full paths
            r.append(os.path.join(root, filename))
    
    # 
    return r


# 
def filtered(i):
    '''
    '''

    # 
    while '*' in i:
        i = i.replace('*','')

    # filter empty items
    _i = list(filter(None, i))

    # flat list to string
    _i = ''.join(_i)

    # 
    return _i


# 
def fix_separator(source_paths):
    '''
    '''

    # aux variable
    r = []

    # 
    for path in source_paths:

        # 
        if os.path.sep != '/':
            path = path.replace(os.path.sep, '/')

        # 
        r.append(path)

    # 
    return r


# 
def filter_ignored(source):
    '''
    '''
    
    # retrieve gitignore path from source path
    gitignore_path = get_gitignore_path(source)

    # get list of ignored directories and files name patters
    ignored = get_ignored(gitignore_path)

    # get filepaths from source
    source_paths = list_files(source)

    # 
    paths = fix_separator(source_paths)

    # 
    for path in source_paths:

        if os.path.sep != '/':
            path = path.replace(os.path.sep, '/')

        # 
        for i in ignored:
            
            # 
            if filtered(i) in path and path in paths:

                # 
                paths.remove(path)

    # 
    return paths


# 
def file2pdf(source, filepath):
    '''
    '''

    # 
    input_file = filepath

    #
    source_dirname = os.path.basename(os.path.dirname(source_name))

    # 
    filename = os.path.basename(filepath)

    # 
    if len(filename.split('.')[0]) is not None:
        filename = filename.split('.')[0]

    # 
    output_folder = os.path.join(os.path.dirname(source) ,os.path.basename(source_name)+"_pdfs")

    # 
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # 
    size_file = 'A2'

    # 
    if len(filename.replace('.','')) > 0:

        # 
        output_file = pathlib.Path('{0}/{1}.pdf'.format(output_folder, filename.replace('.','')))

        # create the Code2pdf object
        pdf = Code2pdf(input_file, output_file, size_file, source, output_folder)

        # call print method to print pdf
        pdf.init_print()


# command line argument parser
def args(args):
    '''
        Main function for terminal call of library
        Arguments:
            args: receive all passed arguments and filter them using
                the argparser library
    '''

    # argparser init
    parser = argparse.ArgumentParser(description=short_description)

    # files with limited lines
    parser.add_argument(
        'source',
        help='source folder to retrieve code files and convert then to PDF format', 
        default=None
    )

    # quiet flag argument parser
    parser.add_argument(
        '-q','--quiet', '--silent',
        action='store_true', 
        help='never output headers giving file names',
        default=False,
        required=False
    )

    # ignore flag argument parser
    parser.add_argument(
        '-i','--ignore',
        action='store_true', 
        help='do not convert files on gitignore',
        default=False,
        required=False
    )

    # debug flag argument parser
    parser.add_argument(
        '-d','--debug',
        action='store_true', 
        help='process debug flag',
        default=False,
        required=False
    )

    # version output argument parser
    parser.add_argument(
        '-v','--version',
        action='version',
        help='output software version',
        default=False,
        version=(__project__+"-"+__version__)
    )

    # passing filtered arguments as array
    args = parser.parse_args(args)

    if args.ignore:
        source = filter_ignored(args.source)
    else:
        source = args.source
    
    # call tail sources function
    run(
        debug=args.debug,
        quiet=args.quiet,
        name=args.source,
        source=source,
    )

# function to check and tail files
def run(debug=False, quiet=False, name=None, source=None):

    # normalizing debug variable
    global debug_flag
    debug_flag = debug

    # normalizing quiet variable
    global quiet_flag
    quiet_flag = quiet

    # normalize source name variable
    global source_name
    source_name = name

    # standard log folder
    log_folder = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)),'../log/'))

    # standard log format
    log_format = '%(asctime)-8s %(levelname)-5s [%(project)s-%(version)s] user: %(user)s LOG: %(message)s'

    # creates a logger instance from class Logger within:
    # an adapter (the logging library Logger Adapter) and the verbose flag
    global logger
    logger = Logger(
        folder = log_folder,
        format = log_format,
        debug_flag = debug_flag,
        extra = {
            'project':  __project__,
            'version':  __version__,
            'user':     getpass.getuser()
        },
    )

    # debug flag variable
    logger.adapter.debug('DEBUG flags was setted as: {0}'.format(debug))

    # create instance of class and validate files
    valid_files = SourceValidator().validate(source)

    for filepath in valid_files:
        file2pdf(source, filepath)

    # check if validate paths remained
    if not len(valid_files) > 0:
        logger.adapter.error('No paths were successfully parsed. Exiting...')
        sys.exit()


def main():
    args(sys.argv[1:])


# run function on command call
if __name__ == "__main__":
    main()

# end of code