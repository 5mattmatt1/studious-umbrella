#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Jun  2 15:23:06 2018

@author: mathuin
"""
import pygame
import random
from coremod.systems import EntitySystem, AffixSystem, GuiSystem
from coremod.gui import EvolveWeaponGui

class ItemSystem:
    data = {}
    def register(self, sid, item):
        # I know I know, very basic
        ItemSystem.data[sid] = item
        
    def __getitem__(self, key):
        return ItemSystem.data[key]

__ItemSystem__ = ItemSystem()

class Item:
    def __init__(self, sid, cost, imgPath):
        ItemSystem.register(sid, self.__class__)
        self.imgPath = imgPath
        self.img = None
        self.cost = cost

    def loadImage(self):
        self.img = pygame.image.load(self.imgPath)
        return self.img

    def getImage(self):
        return self.img if self.img else self.loadImage()

    def onUse(self, player):
        pass
    
    def blit(self, x, y, screen):
        if self.getImage():
            screen.blit((x, y), self.getImage())

class Weapon(Item):
    def __init__(self, sid, cost, imgPath, tuningData):
        Item.__init__(self, sid, cost, imgPath)
        self.enemiesKilled = []
        self.affixs = []
        self.tuningData = tuningData
        self.level = 0
        
    def onHit(self, player, enemy):
        pass
        
    def onHurt(self, player, enemy):
        pass

    def onUse(self, player):
        # TODO: Make swords usable
        pass
    
    def onLevelUp(self, player):
        enemyBoost = random.choice(self.enemiesKilled)
        enemy = EntitySystem[enemyBoost]
        affix = AffixSystem[enemy.tuningData['weaponBoosts']]
        self.affixs.append(affix)
        
    def update(self, evt):
        pass
    
class EvoWeapon(Weapon):
    def __init__(self, sid, tuningData):
        Weapon.__init__(self, sid, tuningData)
    
    def onLevelUp(self, player):
        Weapon.onLevelUp(self, player)
        # TODO: Make an evo screen
        weaponEvoGui = EvolveWeaponGui(self, player)
        sidGui = GuiSystem.addOverlay(weaponEvoGui)
        GuiSystem.setFocus(sidGui)