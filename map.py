# -*- coding: utf-8 -*-
"""
Created on Sat Mar 17 10:54:07 2018

@author: mathuin
"""
import pygame
import pytmx
from pytmx.util_pygame import pygame_image_loader
import random
import math
from dungeonGenerator import dungeonGenerator

# Some Utils
def angleOf(p1, p2): #Taken off of Stack Overflow
    deltaY = (p1[1] - p2[1]);
    deltaX = (p2[0] - p1[0]);
    return math.degrees(math.atan2(deltaY, deltaX));

def weightedhighint(a, b):
    choices = []
    refRange = range(a, b)
    for i in range(b-a):
        choices += [refRange[i]]*max(int(round(i/2.)), 1)
    return random.choice(choices)

class Room:
    def __init__(self, minRoomWidth, maxRoomWidth, minRoomHeight, maxRoomHeight, i, parent):
        self.minRoomWidth = minRoomWidth
        self.maxRoomWidth = maxRoomWidth
        self.minRoomHeight = minRoomHeight
        self.maxRoomHeight = maxRoomHeight
        self.roomBorders = []
        self.roomInteriors = []
        self.parent = parent
        self.baseX = 0
        self.baseY = 0
        self.width = 0
        self.height = 0
        self.minX = 0
        self.maxX = 0
        self.minY = 0
        self.maxY = 0        
        self.i = i
        # Might be slightly harder to assemble into a cohesive Tiled map
        
    def __str__(self):
        return 'Room #%i' % self.i
    
    def __repr__(self):
        return 'Room #%i' % self.i
    
    def generate(self):
        baseX = random.randint(0, self.parent.width)
        baseY = random.randint(0, self.parent.height)
        self.cx = baseX
        self.cy = baseY
        roomWidth = weightedhighint(self.minRoomWidth, self.maxRoomWidth) #random.randint(self.minRoomWidth, self.maxRoomWidth)
        roomHeight = weightedhighint(self.minRoomHeight, self.maxRoomHeight) #random.randint(self.minRoomHeight, self.maxRoomHeight)
        self.width = roomWidth
        self.height = roomHeight
        lDistMax = roomWidth
        rDistMax = roomWidth
        uDistMax = roomHeight
        dDistMax = roomHeight
        parentRoomBorders = self.parent.getRoomBorders()
        parentRoomInteriors = self.parent.getRoomInteriors()
        for x in range(0, roomWidth):
            for y in range(0, roomHeight):
                if (baseX+x, baseY) in parentRoomBorders:    
                    rDistMax = min(rDistMax, x)
                if (baseX-x, baseY) in parentRoomBorders:
                    lDistMax = min(lDistMax, x)
                if (baseX, baseY+y) in parentRoomBorders:
                    dDistMax = min(dDistMax, x)
                if (baseX, baseY-y) in parentRoomBorders:
                    uDistMax = min(uDistMax, x)
                if (baseX+x) >= self.parent.width:
                    rDistMax = min(rDistMax, x)
                if (baseX-x) <= 0:
                    lDistMax = min(lDistMax, x)
                if (baseY+y) >= self.parent.height:
                    dDistMax = min(dDistMax, y)
                if (baseY-y) <= 0:
                    uDistMax = min(uDistMax, y)
                    
        if lDistMax > rDistMax:
            rDist = rDistMax
            lDist = min(roomWidth-rDist, lDistMax)
        elif lDistMax < rDistMax:
            lDist = lDistMax
            rDist = min(roomWidth-lDist, rDistMax)
        else:
            lDist = random.randint(0, lDistMax)
            rDist = min(roomWidth-lDist, rDistMax)
            if lDist+rDist < roomWidth:
                lDist = min(roomWidth-rDist, lDistMax)
        #lDistMax: uDistMax
        #rDistMax: dDistMax
        if uDistMax > dDistMax:
            dDist = dDistMax
            uDist = min(roomWidth-dDist, uDistMax)
        elif uDistMax < dDistMax:
            uDist = uDistMax
            dDist = min(roomWidth-uDist, dDistMax)
        else:
            uDist = random.randint(0, uDistMax)
            dDist = min(roomWidth-uDist, dDistMax)
            if uDist+dDist < roomWidth:
                uDist = min(roomWidth-dDist, uDistMax)
        self.minx = self.cx - lDist
        self.maxx = self.cx + rDist
        self.miny = self.cy - uDist
        self.maxy = self.cy + dDist
        # Generate Interior
        for i in range(lDist):
            for j in range(uDist):
                coords = (baseX-i, baseY-j)
                valid = coords not in parentRoomBorders and coords not in parentRoomInteriors
                if i == lDist-1 or j == uDist-1:
                    if valid:
                        self.roomBorders.append(coords)
                else:
                    if valid:
                        self.roomInteriors.append(coords)

        for i in range(rDist):
            for j in range(uDist):
                coords = (baseX+i, baseY-j)
                valid = coords not in parentRoomBorders and coords not in parentRoomInteriors
                if i == rDist-1 or j == uDist-1:
                    if valid:
                        self.roomBorders.append(coords)
                else:
                    if valid:
                        self.roomInteriors.append(coords)

        for i in range(lDist):
            for j in range(dDist):
                coords = (baseX-i, baseY+j)
                valid = coords not in parentRoomBorders and coords not in parentRoomInteriors
                if i == lDist-1 or j == dDist-1:
                    if valid:
                        self.roomBorders.append(coords)
                else:
                    if valid:
                        self.roomInteriors.append(coords)

        for i in range(rDist):
            for j in range(dDist):
                coords = (baseX+i, baseY+j)
                valid = coords not in parentRoomBorders and coords not in parentRoomInteriors
                if valid:
                    if i == rDist-1 or j == dDist-1:
                        self.roomBorders.append(coords)
                    else:
                        self.roomInteriors.append(coords)
    
    def drawminimap(self, surf):
        pass

class Structure:
    def __init__(self, parent):
        # First example of this will be monster room/spider nest
        pass

class MapGenerator:
    def __init__(self, minRooms=18, maxRooms=38, width=64, height=64, minRoomWidth=5, maxRoomWidth=14, minRoomHeight=3, maxRoomHeight=12):
        self.nRooms = weightedhighint(minRooms, maxRooms)#random.randint(minRooms, maxRooms)
        self.width = width
        self.height = height
        self.minRoomWidth = minRoomWidth
        self.maxRoomWidth = maxRoomWidth
        self.minRoomHeight = minRoomHeight
        self.maxRoomHeight = maxRoomHeight
        self.rooms = []
        self.structures = []
        self.roomBorders = []
        self.roomInteriors = []
        self.hallwayInteriors = []
        self.hallwayBorders = []
        #print(self.nRooms)
        for i in range(self.nRooms):
            tRoom = Room(minRoomWidth, maxRoomWidth, minRoomHeight, maxRoomHeight, i, self)
            self.rooms.append(tRoom)
            tRoom.generate()
        self.generateHallways()
        self.exportMinimap()
    
    def getRoomBorders(self):
        final = []        
        for room in self.rooms:
            for coord in room.roomBorders:
                if coord not in final:
                    final.append(coord)
        return final
        
    def getRoomInteriors(self): # Should I change variable names? Probably
        final = []        
        for room in self.rooms:
            for coord in room.roomInteriors:
                if coord not in final:
                    final.append(coord)
        return final
        
    def exportMinimap(self):
        minimapSurf = pygame.Surface((self.width*2, self.height*2))
        for coord in self.getRoomBorders():
            x, y = coord[0] * 2, coord[1] * 2
            for i in range(0, 2):
                for j in range(0, 2):
                    minimapSurf.set_at((x+i, y+j), (64, 64, 64))
        for coord in self.getRoomInteriors():
            x, y = coord[0] * 2, coord[1] * 2
            for i in range(0, 2):
                for j in range(0, 2):
                    minimapSurf.set_at((x+i, y+j), (128, 128, 128))
        for coord in self.hallwayInteriors:
            x, y = coord[0] * 2, coord[1] * 2
            for i in range(0, 2):
                for j in range(0, 2):
                    minimapSurf.set_at((x+i, y+j), (128, 128, 128))
        # for debugging
        for room in self.rooms:
            x, y = room.cx*2, room.cy*2
            for i in range(0, 2):
                for j in range(0, 2):
                    minimapSurf.set_at((x+i, y+j), (255, 0, 0))

        for room in self.rooms:
            roomSurf = pygame.Surface((room.width*2, room.height*2))
            for coord in room.roomBorders:
                x, y = (coord[0]-room.minx) * 2, (coord[1]-room.miny) * 2
                for i in range(0, 2):
                    for j in range(0, 2):
                        roomSurf.set_at((x+i, y+j), (64, 64, 64))
            for coord in room.roomInteriors:
                x, y = (coord[0]-room.minx) * 2, (coord[1] - room.miny) * 2
                for i in range(0, 2):
                    for j in range(0, 2):
                        roomSurf.set_at((x+i, y+j), (128, 128, 128))
            x, y = (room.cx - room.minx)*2, (room.cy - room.miny)*2
            for i in range(0, 2):
                for j in range(0, 2):
                    roomSurf.set_at((x+i, y+j), (255, 0, 0))
            pygame.image.save(roomSurf, 'roomImages/room_%i.png' % room.i)
        pygame.image.save(minimapSurf, 'minimap.png')

    def generateHallways(self):
        # Not yet
        data = {room: (room.cx, room.cy) for room in self.rooms}
        closest = {}
        for room in self.rooms:
            nahcx = -1
            nahcy = -1
            mind = float('inf')
            nahroom = None
            nahdirec = -1
            for key in data:
                if key != room:
                    tcx, tcy = data[key]
                    td = math.sqrt((room.cx - tcx)**2 + (room.cy - tcy)**2)
                    theta = angleOf((room.cx, room.cy), (tcx, tcy))
                    if theta < 0:
                        theta += 360
                    tdirec = int(round(theta))/45
                    # Might not need to be restricted
                    if td < mind: # and tdirec in [0, 2, 4, 6]:
                        mind = td
                        nahcx, nahcy = tcx, tcy
                        nahdirec = tdirec
                        nahroom = key
            closest[room] = nahroom
            #print(nahdirec)
        print('---------------')
        print('Generation Time')
        print('Rooms: %i' % len(closest))
        for room in closest:
            if room.cx < nahroom.cx and room.cy > nahroom.cy:
                print(room, nahroom)
                print((room.cx, room.cy), (nahroom.cx, nahroom.cy))
                nahroom = closest[room]
                wxi = room.cx
                wxf = nahroom.cx
                for x in range(min(room.cx, nahroom.cx), max(room.cx, nahroom.cx)):
                    if (x, room.cy) in room.roomBorders or (x, room.cy) in room.roomInteriors:
                        wxi = x
                    if (x, nahroom.cy) in nahroom.roomBorders or (x, nahroom.cy) in nahroom.roomInteriors:
                        wxf = x
                twxi = min(wxi, wxf)
                twxf = max(wxi, wxf)
                wxi = twxi
                wxf = twxf
                dy = abs(room.cy - nahroom.cy)
                dx = abs(wxi - wxf)
                iYbreaks = random.randint(1, max(dx/4, 1))
                ybreaks = {}
                lybreak = wxi
                ly = nahroom.cy
                for i in range(iYbreaks):
                    #print(wxi, wxf, iYbreaks)
                    #else:
                    #    ybreak = 
                    if ly != room.cy and lybreak < wxf-iYbreaks+len(ybreaks):
                        print(wxi, wxf)
                        print(lybreak != wxf-iYbreaks+len(ybreaks), lybreak, wxf-iYbreaks+len(ybreaks))
                        print(ly)
                        ybreak = random.randint(lybreak, wxf-iYbreaks+len(ybreaks))
                        ybreaks[ybreak] = random.randint(ly, room.cy)
                        for x in range(wxi, ybreak):
                            self.hallwayInteriors.append((x, ly))
                            print('Horz: (%i, %i)' % (x, ly))
                        for y in range(ly, ybreaks[ybreak]):
                            self.hallwayInteriors.append((ybreak, y))
                            print('Vert: (%i, %i)' % (ybreak, y))
                        lybreak = ybreak
                        ly = ybreaks[ybreak]
                    

class TGKMap(pytmx.TiledMap):
    def __init__(self, filename, **kwargs):
        pytmx.TiledMap.__init__(self, filename, image_loader=pygame_image_loader, **kwargs)
        # Should be good for now
        #print(len(self.layers))
    # Engine
    def draw(self, surf):
        for layer in self.layers:
            for x, y, image in layer.tiles():
                surf.blit(image, (self.tilewidth*x,self.tileheight*y)) # Simple function setup
    
    def update(self, event):
        pass

import time
class Animation:
    def __init__(self, **kwargs):
        self.t = time.time()
        self.i = 0
        self.iter = 1
        # self.__dict__.update(kwargs) ?
        self.x = kwargs['x']
        self.y = kwargs['y']
        if kwargs.has_key('ilist'):
            self.ilist = kwargs['ilist']
    
    def draw(self, surf):
        dt = time.time() - self.t
        #print(self.x, self.y)
        surf.blit(self.ilist[self.i], (self.x, self.y))
        #print(self.i)        
        if dt > (1/10.):
            if self.i+self.iter >= len(self.ilist) or self.i+self.iter < 0:
                self.iter = -self.iter
            self.i += self.iter
            self.t = time.time()

def cheap_reduce_alpha(image, alpha):
    # Better function
    for x in range(image.get_width()):
        for y in range(image.get_height()):
            r, g, b, a = image.get_at((x,y))
            image.set_at((x,y), (r, g, b, max(0, a-int(round(alpha)))))            
            #image.set_at()
import copy
class FadeAnimation(Animation):
    def __init__(self, path, x, y, frames=6, fpf=26):
        self.i = 0
        img_list = []
        img = pygame.image.load(path).convert_alpha()
        for i in range(frames):
            timg = img.copy()
            cheap_reduce_alpha(timg, (fpf*i))
            pygame.image.save(timg, 'assets/entities/erroar_test_%i.png' % i)
            img_list.append(timg)
        Animation.__init__(self, x=x, y=y, ilist=img_list)
# Build/Spell ideas
# Mageslayer
# Aura that reduces max mana and mana regeneration
# Main skills would have no mana requirement
# Bloodknight
# No health regeneration from sources other than life steal
# Gets damage boost from % of health left
def mainloop():
    screen = pygame.display.set_mode((576, 576))
    pygame.display.set_caption('Map')
    #gmap = TGKMap('assets/maps/test_dungeon.tmx')
    #MapGenerator()
    #erroar = FadeAnimation('assets/entities/erroar_test.png', 256, 256) 
    while True:
        screen.fill((0, 0, 0))
        event = pygame.event.poll()
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        #gmap.draw(screen)
        #gmap.update(event)
        #erroar.draw(screen)
        pygame.display.flip()

def mapGenTest():
    #### Test has the Grawn seal of approval ####
    gen = dungeonGenerator(100, 100)
    gen.placeRandomRooms(6, 24)
    gen.generateCorridors()
    gen.connectAllRooms()
    gen.placeWalls()
    gen.exportPreview()
    gen.exportMinimap()

if __name__ == '__main__':
    pass
    #mapGenTest()
    #mainloop()