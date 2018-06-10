#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun May 20 07:54:03 2018

@author: mathuin
"""

radial1 = [(-1, -1), (0, -1), (1, -1),
           (-1, 0), (1, 0),
           (-1, 1), (0, 1), (1, 1)]

radial2 = [(-1, -2), (0, -2), (1, -2),
           (-2, -1), (2, -1),
           (-2, 0), (2, 0),
           (-2, 1), (2, 1),
           (-1, 2), (0, 2), (1, 2)]

radial3 = [(-1, -3), (0, -3), (1, -3),
           (-2, -2), (2, -2),
           (-3, -1), (3, -1),
           (-3, 0), (3, 0),
           (-3, 1), (3, 1),
           (-2, 2), (2, 2),
           (-1, 3), (0, 3), (1, 3)]

radial4 = [(-1, -4), (0, -4), (1, -4),
           (-2, -3), (2, -3),
           (-3, -2), (3, -2),
           (-4, -1), (4, -1),
           (-4, 0), (4, 0),
           (-4, 1), (4, 1),
           (-3, 2), (3, 2),
           (-2, 3), (2, 3),
           (-1, 4), (0, 4), (1, 4)]

# Purely for reference for balancing
# Just len of all radials up to the nth term for each indice
radialCurve = [8, 20, 36, 56]
print(len(radial1) + len(radial2) + len(radial3) + len(radial4))