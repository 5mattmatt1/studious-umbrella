#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Apr  9 22:05:15 2018

@author: mathuin
"""
import pygame

refText = "ABCDEFGHIJKLMNOPQRSTUVWXYZ:!%abcdefghijklmno.pqrstuvwxyz1234567890/*+-"

class PFont:
    def __init__(self, pfontPath, size=8):
        self.baseImage = pygame.image.load(pfontPath)
        self.subImages = []
        self.size = size
        for j in range(self.baseImage.get_height()/size):
            for i in range(self.baseImage.get_width()/size):
                tSurf = self.baseImage.subsurface(pygame.Rect(i*size, j*size, size, size))
                self.subImages.append(tSurf.subsurface(tSurf.get_bounding_rect()))
        
    def render(self, text, padding=0):
        surfText = pygame.Surface(((self.size+padding)*len(text), self.size), pygame.SRCALPHA, 32)
        surfText.set_alpha()
        x = 0
        for char in text:
            if char == " ":
                x += (self.size/2) + padding
                continue
            if char not in refText:
                print("Tried to draw unknown character: %s" % char)
            else:
                index = refText.index(char)
                subImage = self.subImages[index]
                surfText.blit(subImage, (x, self.size-subImage.get_height()))
                x += subImage.get_width() + padding
        return surfText

    def renderWrapped(self, text, padding, width):
        pass

# TODO: Remake red-violet fonts to add "O"
wytSmall = PFont('pfont/wyt_pixel_font8.png', 8)
redSmall = PFont('pfont/red_pixel_font8.png', 8)
orangeSmall = PFont('pfont/orange_pixel_font8.png', 8)
yellowSmall = PFont('pfont/yellow_pixel_font8.png', 8)
greenSmall = PFont('pfont/green_pixel_font8.png', 8)
blueSmall = PFont('pfont/blue_pixel_font8.png', 8)
indigoSmall = PFont('pfont/indigo_pixel_font8.png', 8)
violetSmall = PFont('pfont/violet_pixel_font8.png', 8)
rainbowSmallFonts = [redSmall, orangeSmall, yellowSmall, greenSmall, blueSmall, indigoSmall, violetSmall]
def renderRainbowText(text, fonts=rainbowSmallFonts, size=8, padding=1):
    surfText = pygame.Surface(((size+padding)*len(text), size), pygame.SRCALPHA, 32)
    surfText.set_alpha()
    x = 0
    ri = 0
    for char in text:
        char = char.upper()
        if char == " ":
            x += size + padding
            continue
        if char not in refText:
            print("Tried to draw unknown character: %s" % char)
        else:
            index = refText.index(char)
            subImage = fonts[ri].subImages[index]
            surfText.blit(subImage, (x, 0))
            x += size + padding
            
        ri += 1
        if ri >= len(fonts):
            ri = 0
    return surfText

def renderRainbowTextWrapped(text, width, fonts=rainbowSmallFonts, size=8, padding=1):
    height = ((size*len(text))/width)*size 
    surfText = pygame.Surface((width, height), pygame.SRCALPHA, 32)
    surfText.set_alpha()
    x = 0
    y = 0
    ri = 0
    for char in text:
        char = char.upper()
        if char == " ":
            x += size + padding
        elif char not in refText:
            print("Tried to draw unknown character: %s" % char)
        else:
            index = refText.index(char)
            subImage = fonts[ri].subImages[index]
            surfText.blit(subImage, (x, y))
            x += size + padding
            ri += 1
            if ri >= len(fonts):
                ri = 0
        if x+size >= width:
            x = 0
            y += size + padding
    return surfText

if __name__ == '__main__':
    print("Testing pixel fonts...")
    screen = pygame.display.set_mode((256, 256))
    pygame.display.set_caption('Pixel Font Testing')
    testFont = PFont('pfont/wyt_pixel_font8.png', 8)
    title = renderRainbowText('IM RAINBOW FONT', padding=0) #testFont.render('THE GREY KNIGHT', padding=0)
    title2 = wytSmall.render('1234567890', padding=0)
    while True:
        event = pygame.event.poll()
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        screen.blit(title, (64, 0))
        screen.blit(title2, (64, title.get_height()))
        #screen.blit(testFont.subImages[0], (32, 0))
        #screen.blit(testFont.baseImage, (0, 0))
        pygame.display.flip()     