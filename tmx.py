#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri May 25 21:59:31 2018

@author: mathuin
"""
import xml.etree.ElementTree as ET
from PIL import Image
import pygame
import os, sys
from copy import copy
import random
# import pyscroll
from log import Logger
from dungeonGenerator import dungeonGenerator
import dungeonGenerator as dungen
#### To be added to the main map.py ####

def generateGradient(color):
    gradient = []
    r = color[0]
    g = color[1]
    b = color[2]
    for i in range(24):
        gradient.append((r, g, b, i*10))
    return gradient

def gradientSurf(color):
    gradient = generateGradient(color)
    surf = pygame.Surface((24, 24)).convert_alpha()
    for i in range(24):
        color = gradient[i]
        for j in range(24):
            surf.set_at((i, j), color)
    return surf

class LightSource:
    def __init__(self, lradius=3, color=(255, 255, 255)):
        self.lradius = lradius
        self.color = color
    
def pyg_parse(src, tilex, tiley):
    img = pygame.image.load(src)
    tiles = []
    #print(tilex, tiley)
    for j in range(tiley):
        for i in range(tilex):
            #print(img.get_width(), img.get_height(), i*24, j*24)
            subsurf = img.subsurface((i*24, j*24, 24, 24))
            tiles.append(subsurf)
    return tiles

def pil_parse(src, tilex, tiley):
    img = Image.open(src)
    tiles = []
    for i in range(tilex): # int(self.height)/int(self.tileheight)
        for j in range(tiley):
            cropped = img.crop((i*24, j*24, (i+1)*24, (j+1)*24))
            tiles.append(cropped)
    return tiles

class Tileset:
    def __init__(self, fn=None, valueDict=None, image_loader=pyg_parse):
        # Time to rework for pygame
        self.firstgid = 1
        if fn:
            self.fn = fn
            self.xmlTree = ET.parse(fn)
            self.xmlRoot = self.xmlTree.getroot()
            self.__dict__.update(self.xmlRoot.attrib)
            for child in self.xmlRoot.iter('image'):
                #print(child)
                self.__dict__.update(child.attrib)
                self.tiles = image_loader(self.source, 
                                          int(self.width)/int(self.tilewidth),
                                          int(self.height)/int(self.tileheight))
                
                #print(len(self.tiles))
        if valueDict:
            self.__dict__.update(valueDict)
        
    def dictUpdate(self, dct):
        for key in dct:
            try:
                self.__dict__[key] = eval(dct[key])
            except:
                self.__dict__[key] = dct[key]

    #### Very basic stuff ####
    # TODO: Update this to allow for terrains and the like#
    def save(self):
        self.xmlRoot.attrib["name"] = self.name
        self.xmlRoot.attrib["tileCount"] = self.tilecount
        self.xmlRoot.attrib["tilewidth"] = self.tilewidth
        self.xmlRoot.attrib["tileheight"] = self.tileheight
        self.xmlRoot.attrib["colums"] = self.columns
        self.xmlTree.write(self.fn)

class TiledMap:
    rootAttribDefaultValues = {"version": "1.0", "orientation": "orthogonal",
                               "renderorder": "right-down", "width": "24", 
                               "height": "24", "tilewidth": "24", "tileheight": "24",
                               "nextobjectid": "1"}
    tilesetAttribDefaultValues = {"firstgid":"1", "source":"basic_tileset.tsx"}
    layerAttribDefaultValues = {"name": "Tile Layer 1", "width": "24", "height": "24"}
    dataAttribDefaultValues = {"encoding": "csv"}
    def __init__(self, fn=None, attribDict=None, image_loader=Image.open):
        #print(fn, attribDict)
        self.cx = 5
        self.cy = 5
        self.knownTiles = []
        if fn:
            fpath = os.path.dirname(os.path.abspath(fn)) + "/"
            self.fn = fn
            self.xmlTree = ET.parse(fn)
            self.xmlRoot = self.xmlTree.getroot()
            self.__dict__.update(self.xmlRoot.attrib)            
            self.tilesets = []
            self.layers = {}
            for iTileset in self.xmlRoot.iter('tileset'):
                tileset = Tileset(fpath + iTileset.attrib['source'])
                tileset.firstgid = iTileset.attrib['firstgid']
                self.tilesets.append(tileset)
            for iLayer in self.xmlRoot.iter('layer'):
                self.layers[iLayer.attrib['name']] = self.decodeCSV([item for item in iLayer.iter('data')][0])
        elif attribDict != None:
            fpath = os.path.dirname(sys.argv[0]) + "/assets/maps/"
            self.__dict__.update(attribDict)
            self.data = []
            self.grid = []
            self.tilesets = []
            self.xmlRoot = ET.Element('map')
            #print("Does it get here")
            for key in TiledMap.rootAttribDefaultValues:
                if hasattr(self, key):
                    self.xmlRoot.attrib[key] = getattr(self, key)
                else:
                    self.xmlRoot.attrib[key] = TiledMap.rootAttribDefaultValues[key]
                    setattr(self, key, TiledMap.rootAttribDefaultValues[key])
            if hasattr(self, "tmxtilesets"):
                for tilesetAttrib in getattr(self, "tmxtilesets"):
                    ET.SubElement(self.xmlRoot, "tileset", attrib=tilesetAttrib)
                    tileset = Tileset(fpath + tilesetAttrib['source'])
                    tileset.firstgid = tilesetAttrib['firstgid']
                    self.tilesets.append(tileset)
            else:
                ET.SubElement(self.xmlRoot, "tileset", attrib=TiledMap.tilesetAttribDefaultValues)
                tileset = Tileset(fpath + TiledMap.tilesetAttribDefaultValues['source'])
                tileset.firstgid = TiledMap.tilesetAttribDefaultValues['firstgid']
                self.tilesets.append(tileset)
            if hasattr(self, "tmxlayers"):
                for layerAttrib in getattr(self, "tmxlayers"):
                    defaultAttrib = copy(TiledMap.layerAttribDefaultValues)
                    defaultAttrib.update(layerAttrib)
                    dataEncoding = layerAttrib["dataEncoding"]
                    data = layerAttrib["data"]
                    del layerAttrib["dataEncoding"]
                    del layerAttrib["data"]
                    layer = ET.SubElement(self.xmlRoot, "layer", attrib=defaultAttrib)
                    dataElement = ET.SubElement(layer, "data", attrib={"encoding": dataEncoding})
                    dataElement.text = data
            else:
                layer = ET.SubElement(self.xmlRoot, "layer", attrib=TiledMap.layerAttribDefaultValues)
                data = ET.SubElement(layer, "data", attrib=TiledMap.dataAttribDefaultValues)
                self.layers = {}
                self.layers[layer.attrib['name']] = []
                for i in range(int(getattr(self, "width"))):
                    self.layers[layer.attrib['name']].append([])
                    for j in range(int(getattr(self, "height"))):
                        self.layers[layer.attrib['name']][i].append(0)
                #print(self.layers)
                data.text = self.encodeCSV(layer.attrib['name'])
        self.centerRect = pygame.Rect(0, 0, int(self.tilewidth), int(self.tileheight))
    
    def export(self, fn=None):
        if fn:
            with open(fn, 'w') as f:
                f.write(ET.tostring(self.xmlRoot))
                f.close()
        else:
            pass
            #print(ET.dump(self.xmlRoot))

    def generate(self, layerName):
        gen = dungeonGenerator(int(self.height), int(self.width))
        gen.placeRandomRooms(6, 24)
        gen.generateCorridors()
        gen.connectAllRooms()
        gen.placeWalls()
        #TODO: Remove export functions after finished testing
        gen.exportLightingPreview('assets/maps/test_lighting.png')
        gen.exportPreview('assets/maps/test.png')
        gen.exportMinimap('assets/maps/testmini.png')
        self.layers[layerName] = gen.toTiledMap(int(self.nextobjectid))
        self.grid = gen.grid
        for layerNode in self.xmlRoot.iter('layer'):
            if layerNode.attrib['name'] == layerName:
                [item for item in layerNode.iter('data')][0].text = self.encodeCSV(layerName)
    
    def center(self, rect):
        pass
    
    def draw(self, screen):
        greyOverlay = pygame.image.load('grey_overlay.png')
        dGreyOverlay = pygame.image.load('darkgrey_overlay.png')
        grey_knight = pygame.image.load('assets/entities/grey_knight.png')
        for layerKey in self.layers:
            layer = self.layers[layerKey]
            tileset = self.tilesets[0]
            brokenLineOfSight = []
            # It annoys the absolute shit out of me that I gotta do this twice
            #### Lighting Engine Code ####
            for xi in range(-5, 0):
                for yi in range(-5, 0):
                    if 0 < xi+self.cx < int(self.height) and 0 < yi+self.cy < int(self.width):
                        #print("Can find shit")
                        if not (self.grid[xi+self.cy][yi+self.cx] == 1 or \
                                self.grid[xi+self.cy][yi+self.cx] == 2):
                            brokenLineOfSight += [(x, y) for x in range(-5, xi) for y in range(-5, yi)]
            for xi in range(5):
                for yi in range(5):
                    if 0 < xi+self.cx < int(self.height) and 0 < yi+self.cy < int(self.width):
                        #print("Can find shit")
                        try:
                            if not (self.grid[xi+self.cy][yi+self.cx] == 1 or \
                                    self.grid[xi+self.cy][yi+self.cx] == 2):
                                brokenLineOfSight += [(x, y) for x in range(xi, 5) for y in range(yi, 5)]
                        except Exception as e:
                            print("Lighting Engine: %i, %i" % (xi+self.cx, yi+self.cy))
            #### Testing Lighting Engine ####
            #if random.randint(0, 10):
            #    colorMap = Image.new("RGB", (11, 11))
            #    lightingMap = Image.new("RGB", (11, 11))
                #for i in range(-5, 0):
                #    for j in range(-5, 0)
            #    try:
            #        for i in range(-5, 5):
            #            for j in range(-5, 5):
            #                colorMap.putpixel((i+5, j+5), dungen.colorMap[self.grid[j+self.cy][i+self.cx]])
                            
            #        for unseenTileX, unseenTileY in brokenLineOfSight:
            #            lightingMap.putpixel((unseenTileX+5, unseenTileY+5), (128, 0, 0))
            #    except:
            #         print("Lighting Engine: %i, %i" % (xi+self.cx, yi+self.cy))
            #        
            #    lightingMap.save("test/lightingMap_%i_%i.png" % (self.cy, self.cx))
            #    colorMap.save("test/colorMap_%i_%i.png" % (self.cy, self.cx))
            
            #### Regular Map Drawing Code ####
            for i in range(-5, 5):#len(layer)):
                if i+self.cx < 0 or i+self.cx > int(self.height):
                    row = [0] * int(self.width)
                else:
                    try:
                        row = layer[i+self.cx]
                    except Exception as e:
                        print("I:", len(layer), i+self.cx)
                        row = [0] * int(self.width)
                for j in range(-5, 5):
                    #if j+self.cy < 0 or j+self.cy > int(self.width):
                    #    column = 0
                    #else:
                    try:
                        column = row[j+self.cy]
                    except Exception as e:
                        print("J:", len(row), j+self.cy)
                        column = 0
                    if int(column) > 0:
                        if i > -3 and i < 3 and j > -3 and j < 3 and (i, j) not in brokenLineOfSight:
                            screen.blit(tileset.tiles[int(column)-1], ((j+5)*int(self.tilewidth), (i+5)*int(self.tileheight)))
                            if (j+self.cy+5, i+self.cx+5) not in self.knownTiles:
                                self.knownTiles.append((j+self.cy+5, i+self.cx+5))
                        elif (j+self.cy+5, i+self.cx+5) in self.knownTiles:
                            screen.blit(tileset.tiles[int(column)-1], ((j+5)*int(self.tilewidth), (i+5)*int(self.tileheight)))
                            screen.blit(greyOverlay, ((j+5)*int(self.tilewidth), (i+5)*int(self.tileheight)))
                        #elif (i, j) not in brokenLineOfSight: 
                        #    screen.blit(tileset.tiles[int(column)-1], ((j+5)*int(self.tilewidth), (i+5)*int(self.tileheight)))
                        #    screen.blit(dGreyOverlay, ((j+5)*int(self.tilewidth), (i+5)*int(self.tileheight)))
        screen.blit(grey_knight, (5*int(self.tilewidth), 5*int(self.tilewidth)))
    
    def encodeCSV(self, layerName):
        grid = self.layers[layerName]
        rows = []
        #print(grid)
        for i in range(len(grid)):
            row = grid[i]
            rowTxt = ','.join([str(column) for column in row])
            if i != len(grid)-1:
                rowTxt += ','
            rows.append(rowTxt)
        return '\n'.join(rows)

    def decodeCSV(self, csv):
        self.grid = []
        rows = csv.text.split('\n')
        for i in range(1, len(rows)):
            columns = rows[i].split(',')
            self.grid.append([])
            for column in columns:
                self.grid[i-1].append(int(column))
        #print(len(self.grid), len(self.grid[0]))
    
    def update(self, evt):
        if evt.type == pygame.KEYDOWN:
            if evt.key == pygame.K_LEFT:
                if self.cy-1 > -5:    
                    # Check if wall
                    if self.grid[self.cy-1][self.cx] != 5:
                        self.cy -= 1
            elif evt.key == pygame.K_RIGHT:
                if self.cy+1 < int(self.width) + 5:    
                    if self.grid[self.cy+1][self.cx] != 5:
                        self.cy += 1
            elif evt.key == pygame.K_DOWN:
                if self.cx < int(self.height) + 5:
                    if self.grid[self.cy][self.cx+1] != 5:
                        self.cx += 1
            elif evt.key == pygame.K_UP:
                if self.cx > 0:
                    if self.grid[self.cy][self.cx-1] != 5:
                        self.cx -= 1

if __name__ == "__main__":
    #Tileset("assets/maps/basic_tileset.tsx")
    tmap = TiledMap(attribDict={})#"assets/maps/for_xml_parsing.tmx")
    #ls = LightSource(color=(0, 0, 255))
    screen = pygame.display.set_mode((264, 264))
    tmap.generate("Tile Layer 1")
    tmap.export('assets/maps/test.tmx')
    #pygame.image.save(gradientSurf((0, 0, 0)), "gradient.png")
    pygame.display.set_caption("Tiled Map")
    while True:
        event = pygame.event.poll()
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        screen.fill((0, 0, 0))
        tmap.draw(screen)
        tmap.update(event)
        pygame.display.flip()
    