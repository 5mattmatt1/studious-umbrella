#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Apr  9 11:55:59 2018

@author: mathuin
"""
import pygame
import pfont
pygame.font.init()
arial = pygame.font.Font(pygame.font.match_font(u'arial', True), 22)
marial = pygame.font.Font(pygame.font.match_font(u'arial', True), 12)
sarial = pygame.font.Font(pygame.font.match_font(u'arial', True), 8)

def centerhorz(awidth, bwidth):
    return int(round((bwidth-awidth)/2.))

class GuiObject:
    def __init__(self, x, y, width, height, parent=None):
        self.children = []
        self.parent = parent
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.remakeRect()
    
    def setX(self, x):
        if self.x != x:
            self.x = x
            self.remakeRect()
    
    def setY(self, y):
        if self.y != y:
            self.y = y
            self.remakeRect()
    
    def setWidth(self, width):
        if self.width != width:
            self.width = width
            self.remakeRect()
            
    def setHeight(self, height):
        if self.height != height:
            self.height = height
            self.remakeRect()
        
    def remakeRect(self):
        self.rect = pygame.Rect((self.x, self.y, self.width, self.height))

    def update(self, evt):
        for child in self.children:
            child.update(evt)
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            self.onHover()

    def onKeyPress(self, key):
        pass
    
    def onMousePress(self, mouseButton):
        pass
    
    def draw(self, surf):
        for child in self.children:
            child.draw(surf)
    
    def onHover(self):
        pass

class StatusEffect:
    def __init__(self, trns):
        self.turnsLeft = trns
        self.index = 0
    
    def onTurn(self, ent):
        self.turnsLeft -= 1
        if self.turnsLeft == 0:
            del ent.statusEffects[self.index]

class PosionStatusEffect(StatusEffect):
    def __init__(self, dmg, trns):
        StatusEffect.__init__(self, trns)
        self.dmg = dmg

    def getDamage(self):
        return self.dmg
    
    def onTurn(self, ent):
        ent.inflictDamage(self, ent)
        GuiObject.onTurn(self, ent)

class SkillEffect:
    def __init__(self, value):
        self.text = ""
        self.value = value
    
    def onTurn(self, player):
        pass
    
    def getText(self):
        return self.text.format(self.value)
    
    def onUse(self):
        pass
    
    def inflictStatusEffect(self, enemy, player):
        return None
    
    def calcDamage(self, enemy, player):
        return 0
    
class ActiveSkill:
    def __init__(self):
        self.effects = []

    def onUse(self):
        pass
    
    def onTurn(self, player):
        pass # Useful for things like auras
    
    def inflictStatusEffect(self, enemy, player):
        for effect in self.effects:
            tStatusEffect = effect.inflictStatusEffect(enemy, player)
            if tStatusEffect:
                enemy.addStatusEffect(tStatusEffect)

class PassiveSkill: 
    # No real reason to make a shared parent class with ActiveSkill due to duck typing and python
    # having multitype lists
    def __init__(self, img):
        self.img = img
        self.resistances = {}
        self.lvl = 0
        self.mlvl = 0
        
    def localize(self, txt, value):
        # TODO: Change to localization file with corresponding text keys
        if txt == 'magic_resistance':
            return pfont.wytSmall.render("Magic Resistance: {0}%".format(value))
        elif txt == 'elemental_resistance':
            # Would have the corresponding key be rv|Elemental Resistance: {0}%
            return pfont.renderRainbowText("Elemental Resistance: {0}%".format(value))

    def genTooltip(self):
        cHeight = 8
        cWidth = 8
        textSurfs = []
        yPadding = 0
        for resistance in self.resistances:
            textSurf = self.localize(resistance, self.resistances[resistance])
            cWidth = max(cWidth, textSurf.get_width()+8)
            cHeight += textSurf.get_height() + yPadding
            textSurfs.append(textSurf)
        toolTipSurf = pygame.Surface((cWidth, cHeight))
        toolTipSurf.fill((64, 64, 64))
        y = 4
        for textSurf in textSurfs:
            x = centerhorz(textSurf.get_width(), cWidth)
            toolTipSurf.blit(textSurf, (x, y))
            y += textSurf.get_height()
        return toolTipSurf

class SkillGuiObject(GuiObject):
    def __init__(self, x, y, skill, parent):
        GuiObject.__init__(self, x, y, 32, 32, parent)
        self.skill = skill
        self.hovering = False
        self.toolTip = None
    
    def draw(self, surf):
        surf.blit(self.skill.img, (self.x, self.y))
        if self.hovering and self.toolTip:
            # TODO: Add checks if the tooltip would be outside the gui
            toolTipx = self.x+centerhorz(self.toolTip.get_width(), self.width)
            toolTipy = self.y+centerhorz(self.height, self.toolTip.get_height())
            surf.blit(self.toolTip, (toolTipx, toolTipy))
        self.hovering = False
        
    def genTooltip(self):
        self.toolTip = self.skill.genTooltip()

    def onHover(self):
        # Finally everything is pretty much setup in order for me to draw the damn skill tooltips
        if not self.toolTip:
            self.genTooltip()
        self.hovering = True

class ProfessionGui(GuiObject):
    def __init__(self, profession):
        GuiObject.__init__(self, 0, 0, 256, 256, None)
        self.profession = profession
        self.img = pygame.image.load('skill_screen.png')
        for skill in self.profession.skills:
            #print(skill)
            if skill == 1:
                x, y = 78, 189
            elif skill == 2:
                x, y = 158, 189
            self.children.append(SkillGuiObject(x, y, self.profession.skills[skill], self))
                
        
    def draw(self, screen):
        screen.blit(self.img, (self.x, self.y))
        GuiObject.draw(self, screen)

class Profession:
    def __init__(self, img):
        self.skills = {}
        self.img = img
        self.lvl = 0

class MagicResistance(PassiveSkill):
    def __init__(self):
        PassiveSkill.__init__(self, pygame.image.load('mage_resistance_symbol.png'))
        # TODO: 
        self.resistances = {'magic_resistance': 5} # 5% per level?
        # Maybe manage it so that if the value is an integer than it manages as i*self.lvl, else it manages as lis[self.lvl] 

class ElementalResistance(PassiveSkill):
    def __init__(self):
        PassiveSkill.__init__(self, pygame.image.load('elemental_resistance_symbol.png'))
        self.resistances = {'elemental_resistance': 5}

class MageKiller(Profession):
    def __init__(self):
        Profession.__init__(self, pygame.image.load('magekiller_symbol.png'))
        self.skills[1] = MagicResistance()#PassiveSkill(pygame.image.load('mage_resistance_symbol.png'))
        self.skills[2] = ElementalResistance()

def renderRainbowText(text, padding=1, font=arial, bgColor=(64, 64, 64), outline=True, outlineColor=(0, 0, 0)):
    rainbowColors = [(255, 0, 0), (255, 165, 0), (255, 255, 0), (0, 128, 0), (0, 0, 255), (75, 0, 130), (238, 130, 238)]
    surfText = font.render(text, 0, outlineColor)
    if outline:
        finalSurfText = pygame.Surface((surfText.get_width()+3, surfText.get_height()+3))
        finalSurfText.fill(bgColor)
        for i in range(3):
            for j in range(3):
                finalSurfText.blit(surfText, (i, j))
    else:
        finalSurfText = pygame.Surface((surfText.get_width(), surfText.get_height()))
        finalSurfText.fill(bgColor)
    ri = 0
    if outline:
        x = 1
    else:
        x = 0
    for char in text:
        surfText = font.render(char, 0, rainbowColors[ri])
        finalSurfText.blit(surfText, (x, 0))
        x += surfText.get_width() #+ padding
        ri += 1
        if ri >= len(rainbowColors):
            ri = 0
    #x += surfText.get_width()
    return finalSurfText
    
def drawRainbowText(x, y, surf, text, font=arial):
    rainbowColors = [(255, 0, 0), (255, 165, 0), (255, 255, 0), (0, 128, 0), (0, 0, 255), (75, 0, 130), (238, 130, 238)]
    surfText = font.render(text, 0, (255, 255, 255))
    #x = centerhorz(surfText.get_width(), 256)
    #owidth = surfText.get_width()
    #ox = x
    ri = 0
    for char in text:
        surfText = font.render(char, 0, rainbowColors[ri])
        surf.blit(surfText, (x, y))
        x += surfText.get_width()
        ri += 1
        if ri >= len(rainbowColors):
            ri = 0
    #surf.blit(font.render(text, 0, (255, 255, 255)), (ox, surfText.get_height()))

if __name__ == '__main__':
    screen = pygame.display.set_mode((256, 256))
    pygame.display.set_caption('Rainbows')
    magekillerGui = ProfessionGui(MageKiller())
    #print(magekillerGui.rect.__dict__)
    while True:
        event = pygame.event.poll()
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        #drawRainbowText(screen, 'Rainbows')
        magekillerGui.draw(screen)
        magekillerGui.update(event)
        pygame.display.flip()