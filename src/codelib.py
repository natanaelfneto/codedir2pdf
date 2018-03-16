#!/usr/bin/python
import sys

from pygments.lexers import get_lexer_for_filename
from pygments.formatters.html import HtmlFormatter
from pygments import highlight

from xhtml2pdf import pisa

from main import *


class Code2Pdf(object):
    def __init__(self, input_file, verbose):
        self.__input_file = input_file
        self.__output_file = input_file + '.pdf'
        self.verbose = verbose

    def highlight_file(self, linenos):
        echo = PrintVerbose(self.verbose)
        lexer = get_lexer_for_filename(self.__input_file)
        formatter = HtmlFormatter(noclasses=True, linenos=linenos)
        try:
            with open(self.__input_file, 'r') as f:
                content = f.read()
        except IOError as exc:
            echo.output(exc.message)

        return highlight('', lexer, formatter)

    def init_print(self, linenos=False):
        try:
            content = self.highlight_file(linenos=linenos)
            with open(self.__output_file, "w+b") as out:
                pdf = pisa.CreatePDF(content, dest=out)
            return pdf.err
        except IOError as exc:
            echo.output(exc.message)

    def __del__(self):
        echo = PrintVerbose(self.verbose)
        echo.output('> Code2PDF task memory cleaned')


