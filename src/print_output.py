#!/usr/bin/python
class PrintVerbose(object):    
    def __init__(self, verbose):
        self.verbose = verbose

    def output(self, output):
        if self.verbose:
            print(output)