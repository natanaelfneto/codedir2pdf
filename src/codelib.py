#!/usr/bin/python
import sys

from pygments.lexers import get_lexer_for_filename
from pygments.formatters.html import HtmlFormatter
from pygments import highlight, styles

from xhtml2pdf import pisa

from main import *
from print_output import *


class Code2Pdf(object):
    def __init__(self, input_file, verbose):
        self.__input_file = input_file
        self.__output_file = input_file + '.pdf'
        self.verbose = verbose

    def init_print(self, linenos=False):
        echo = PrintVerbose(self.verbose)
        echo.output('> using: '+str(os.path.abspath(self.__input_file)))
        with open(self.__input_file) as f:
            echo.output('> reading file content ...')
            content = f.read()
        echo.output('> trying to import lexer and formatter for file type ...')
        try:
            lexer = get_lexer_for_filename(self.__input_file)
            echo.output('> lexer import done')
            formatter = HtmlFormatter(noclasses=True, linenos=linenos)
            echo.output('> formatter done')
            content = highlight('', lexer, formatter)
            echo.output('> content updated with lexer and formatter')
        except:
            echo.output('> content update could not happen')
            pass
        echo.output('> stating to write output as pdf content ...')
        with open(self.__output_file, "w+b") as out:
            echo.output('> using pisa library to convert: '+str(out))
            try:
                pdf = pisa.CreatePDF(content, dest=out)
            except:
                pass
        return pdf.err
        echo.output('> content is now save as pdf')

    def __del__(self):
        echo = PrintVerbose(self.verbose)
        echo.output('> Code2PDF task memory cleaned')


