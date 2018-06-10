#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed May 23 23:10:53 2018

@author: mathuin
"""

from math import hypot

def findPath(gmap, startCoord, endCoord):
    pass

class AIScript:
    def __init__(self, weight):
        self.weight
        
    def onRun(self, gmap):
        pass
    
    def shInit(self):
        return False
    
    def viability(self):
        # Return 0-10
        # Some logic in between
        return max(min(1 * self.weight, 10), 0)

def findNeighbours(x, y, maxX, maxY, minX=0, minY=0):
    xi = (0, -1, 1) if minX < x < maxX - 1 else ((0, -1) if x > minX else (0, 1))
    yi = (0, -1, 1) if minY < y < maxY - 1 else ((0, -1) if y > minY else (0, 1))
    for a in xi:
        for b in yi:
            if a == b == 0:
                continue
            yield (x+a, y+b)

def findNeighboursDirect(x, y, maxX, maxY, minX=0, minY=0):
    xi = (0, -1, 1) if minX < x < maxX - 1 else ((0, -1) if x > minX else (0, 1))
    yi = (0, -1, 1) if minY < y < maxY - 1 else ((0, -1) if y > minY else (0, 1))
    for a in xi:
        for b in yi:
            if abs(a) == abs(b):
                continue
            yield (x+a, y+b)
            
def findNeighboursIndirect(x, y, maxX, maxY, minX=0, minY=0):
    xi = (0, -1, 1) if minX < x < maxX - 1 else ((0, -1) if x > minX else (0, 1))
    yi = (0, -1, 1) if minY < y < maxY - 1 else ((0, -1) if y > minY else (0, 1))
    for a in xi:
        for b in yi:
            if abs(a) != abs(b):
                continue
            yield (x+a, y+b)

class SwarmMoveAI:
    def __init__(self, entity, weight):
        self.entity = entity
        self.weight = weight
        self.targetTile = None
        
    def onTurn(self, gmap):
        # Don't worry about attacking
        # That can be it's own seperate script
        if self.targetTile:
            direc = findPath(gmap, self.entity.coord, self.targetTile)
        else:    
            swarmEntities = []
            for entity in gmap.entities:
                if entity.sid == self.entity.sid:
                    swarmEntities.append(entity)
            closestDoorway = None
            closestDist = float('inf')
            for i in range(len(int(gmap.width))):
                for j in range(len(int(gmap.height))):
                    # Find the nearest doorway to hide inside of
                    # Meant to reach out and fuck the player up
                    if gmap.grid[i][j] == 3:
                        for swarmEntity in swarmEntities:
                            dist = hypot(swarmEntity.x - i, swarmEntity.y - j)
                            if dist < closestDist:
                                closestDoorway = (i, j)
                                closestDist = dist
            neighbours = findNeighboursIndirect(closestDoorway[0], closestDoorway[1],
                                              gmap.width, gmap.height)
            bestNeighbour = None
            bestFriendliness = -float('inf')
            for neighbour in neighbours:
                if gmap.grid[neighbour[0]][neighbour[1]] == 1:
                    friendliness = [gmap.grid[friendlyNeighbour[0]][friendlyNeighbour[1]] for friendlyNeighbour in findNeighbours(neighbour[0], 
                                    neighbour[1], gmap.width, gmap.height)].count(1)
                    if friendliness > bestFriendliness:
                        bestNeighbour = neighbour
                        bestFriendliness = friendliness
            self.targetTile = bestNeighbour
            