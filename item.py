#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Item template

@author: mathuin
"""
from coremod.items import Item

class ItemName(Item):
    def __init__(self):
        # id, cost, imgPath
        Item.__init__(self, 0, 0, "/path/to/image/file.png")

    def onHit(self, player, enemy):
        Item.onHit(self, player, enemy)
        
    def onHurt(self, player, enemy):
        Item.onHurt(self, player, enemy)

    def onUse(self, player):
        Item.onUse(self, player)
    
    def draw(self, screen):
        Item.draw(self, screen)