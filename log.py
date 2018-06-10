#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Jun  5 09:39:06 2018

@author: mathuin
"""

import time
import sys, traceback

class Logger:
    def __init__(self, fn="grey_knight.log"):
        self.fn = fn
        with open(fn, "w") as f:
            f.write('')
            f.close()
            
        with open(fn, "a") as f:
            self.log = f
        self.time = None

    def clear(self):
        self.log.close()
        with open(self.fn, "w") as f:
            f.write('')
            f.close()
            
        with open(self.fn, "a") as f:
            self.log = f
            
    def startTime(self):
        self.time = time.time()

    def logTime(self, identifier):
        if self.time:
            self.write("%s: %i" % (identifier, str(time.time()-self.time)))
        else:
            self.write("%s: Bad Timer" % identifier)

    def write(self, data):
        self.log.write(data)

    def traceback(self):
        exc_type, exc_value, exc_traceback = sys.exc_info()
        traceback.print_tb(exc_traceback, limit=1, file=self.log)
    
    def __uninit__(self):
        self.log.close()