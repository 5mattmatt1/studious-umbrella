#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Jun  2 15:38:09 2018

@author: mathuin
"""

import json
import yaml
import xml.etree.ElementTree as ET

class TuningData:
    # Special dict-esque class
    def __init__(self):
        self.defaultKeys = None
    
    def setDefaultKeys(self, keys):
        self.defaultKeys = keys
        
    def __getitem__(self, key):
        return self.__dict__.__getitem__(key)
        
    def __setitem__(self, key, value):
        if type(value) == dict:
            self.__dict__[key] = value
        elif type(value) == list:
            if self.defaultKeys:
                if len(self.defaultKeys) == value:
                    self.__dict__[key] = [(self.defaultKeys[i], value[i]) for i in range(len(value))]
                else:
                    raise AttributeError
            else:
                self.__dict__[key] = [(i, value[i]) for i in range(len(value))]

class TuningDataLoader:
    def __init__(self, fpath):
        if fpath[-4:] == '.xml':
            self.xmlLoad(fpath)
        elif fpath[-4:] == '.yml':
            self.yamlLoad(fpath)
        elif fpath[-5:] == '.json':
            self.jsonLoad(fpath)
            
def xmlLoadItemTuningData(fpath):
    elementTree = ET.parse(fpath)

def yamlLoadItemTuningData(fpath):
    data = yaml.load(fpath)

def jsonLoadItemTuningData(fpath):
    data = json.load(fpath)

def loadItemTuningData(fpath):
    if fpath[-4:] == '.xml':
        xmlLoadItemTuningData(fpath)
    elif fpath[-4:] == '.yml':
        yamlLoadItemTuningData(fpath)
    elif fpath[-5:] == '.json':
        jsonLoadItemTuningData(fpath)