# -*- coding: utf-8 -*-
"""
Created on Mon Mar  5 09:05:08 2018

@game: The Grey Knight
@author: Mathuin
"""
import pygame

item_slot = pygame.image.load('assets/gui/item_slot.png') # Idea: create an image registry that only loads when needed 
base_tab = pygame.image.load('assets/gui/shop_tab.png')
tab_background = pygame.image.load('assets/gui/tab_background.png')
potion_tab = pygame.image.load('assets/gui/potion_tab.png')
health_potion = pygame.image.load('assets/items/health_potion.png')
mana_potion = pygame.image.load('assets/items/mana_potion.png')
mystery_potion = pygame.image.load('assets/items/mystery_potion.png')
weapons_tab = pygame.image.load('assets/gui/weapons_tab.png')
claws = pygame.image.load('assets/items/claws.png')
armour_tab = pygame.image.load('assets/gui/armour_tab.png')
bone_sword = pygame.image.load('assets/items/bone_sword.png')
#Anevis stuff
anevis_ranger_sword = pygame.image.load('assets/items/anevis/anevis_ranger_sword.png')
anevis_crossbow = pygame.image.load('assets/items/anevis/anevis_crossbow.png')
anevis_leather_helm = pygame.image.load('assets/items/anevis/anevis_leather_helm.png')
anevis_leather_armor = pygame.image.load('assets/items/anevis/anevis_leather_armor.png')
anevis_leather_pants = pygame.image.load('assets/items/anevis/anevis_leather_pants.png')
anevis_leather_boots = pygame.image.load('assets/items/anevis/anevis_leather_boots.png')
anevis_wooden_shield = pygame.image.load('assets/items/anevis/anevis_wooden_shield.png')

# GUI Inventory
inventory_base = pygame.image.load('assets/gui/inventory.png')

# Not gonna be used atm but will trend towards this system
class ImageRegistry:
    imgs = ['item_slot', 'base_tab']
    item_slot = 'assets/gui/item_slot.png'
    base_tab = 'assets/gui/shop_tab.png'

def preloadImageRegistry():
    for img in ImageRegistry.imgs:
        exec("ImageRegistry.%s = pygame.image.load(ImageRegistry.%s)" % img) # Quickly loads up every string
    del ImageRegistry.imgs[:]

def getImage(s): #ex. getImage('item_slot')
    img = eval('ImageRegistry.%s' % s)
    if type(s) == type(''):
        exec("ImageRegistry.%s = pygame.image.load(ImageRegistry.%s)" % img)
    return eval('ImageRegistry.%s' % s)
    
class Item:
    def __init__(self, img, cost, itemtype='item'):
        self.img = img
        self.cost = cost
        self.itemtype = itemtype

class Consumable(Item):
    def __init__(self):
        pass

class GUIManager:
    def __init__(self):
        self.active_guis = {}
        # Ex. keys: 'inventory', 'shop'
        
    def openGUI(self, key, gui):
        self.active_guis[key] = gui
        gui.parent = self
        
    def closeGUI(self, key): # just easier to find than vague code
        del self.active_guis[key]
       
    def mainloop(self, event, screen):
        # Mild reduction is overhead, with no loss in verbosity
        for gui in self.active_guis.values():
            gui.update(event)
            gui.draw(screen)

    def update(self, event):
        for gui in self.active_guis.values():
            gui.update(event)
    
    def draw(self, screen):
        for gui in self.active_guis.values():
            gui.draw(screen)
    
    def guiOpen(self, key):
        return self.active_guis.has_key(key)

class ItemSlot: # Do we even need an x and y?, probably, I'd rather have item have the variables
    def __init__(self, x, y, parent):
        # self.img = # Why not just use item_slot here? It is pretty static
        self.parent = parent        
        self.x = x
        self.y = y
        self.item = None # More than a little important
        self.width = item_slot.get_width()
        self.height = item_slot.get_height()
        self.clicked = False

    def draw(self, surface):
        surface.blit(item_slot, (self.x, self.y))
        if self.item:
            ix = int(round((self.width - self.item.img.get_width())/2.))
            iy = int(round((self.height - self.item.img.get_height())/2.))
            surface.blit(self.item.img, (self.x+ix, self.y+iy))
    
    def update(self, event):
        if pygame.Rect(self.x, self.y, self.width, self.height).collidepoint(pygame.mouse.get_pos()):
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: # Left click
                    if self.clicked == True:
                        self.onDoubleClick()
                        return 
                    if self.item and self.canPlace(self.parent.item):
                        tItem = self.parent.item
                        self.parent.item = self.item
                        self.item = tItem
                        self.parent.last_item_slot = self
                        self.onRemove()
                    self.clicked = True
                elif event.button == 3: # Right click
                    #print(self.getOAncestor(), self.getMacAncestor())
                    manager = self.getOAncestor()
                    if self.getMacAncestor().__class__ == InventoryGUI:
                        print('Inventory')
                        if manager.guiOpen('shop'):
                            shop = manager.active_guis['shop']
                            shop.addItem(shop.active_shop_tab, self.item)
                            self.item = None
                    elif self.getMacAncestor().__class__ == Shop:
                        print('Shop')
                        if manager.guiOpen('inventory'):
                            inv = manager.active_guis['inventory']
                            inv.addItem(self.item)

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    if not self.item and self.canPlace(self.parent.item):
                        self.item = self.parent.item
                        self.parent.item = None                        
                        self.onPlace()
                        # self.clicked = False
                    elif self.item and self.canPlace(self.parent.item):
                        tItem = self.parent.item
                        self.parent.item = self.item
                        self.item = tItem
                        self.parent.last_item_slot = self
                        self.onPlace()
                elif event.button == 3:
                    pass
        else:
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.clicked = False
    
    def canPlace(self, item):
        return True
        
    def onDoubleClick(self):
        pass
    
    def onPlace(self):
        pass
    
    def getOAncestor(self):
        temp = self
        while hasattr(temp, 'parent'):
            temp = temp.parent
        return temp

    def getMacAncestor(self):
        temp = self
        mtemp = None
        while hasattr(temp, 'parent'):
            mtemp = temp
            temp = temp.parent
        return mtemp

    def onRemove(self):
        pass

class ShopTab:
    def __init__(self, img, text, x, y, i, parent): # Parent will be required, this is a child gui class
        self.item_slots = []
        self.parent = parent
        self.item = None
        self.last_item_slot = None
        self.img = img # This will be the overlay
        self.text = text # Useful for a mouse over text
        # self.slotx = 0
        self.slotnx = 0
        # self.sloty = 0
        self.slotny = 0
        self.x = x
        self.y = y
        self.i = i
        # self.base_tab = pygame.image.load('assets/gui/shop_tab.png') # Actually need to preload this
        # Same deal as item_slot
        
    def generateItemSlots(self, x, y):
        # Should manage this well enough    
        slotx = int(round((155 - (x*item_slot.get_width()))/2.)) 
        sloty = int(round((118 - (y*item_slot.get_height()))/2.))
        self.slotnx = x
        self.slotny = y
        for j in range(y):
            t = []
            for i in range(x):
                t.append(ItemSlot(self.x+slotx + 36*i, self.y+base_tab.get_height() + sloty + 36*j, self))
            self.item_slots.append(t)
        # print(self.item_slots[0][0].getAncestor())
    
    def draw(self, surf):
        # Draw item slots
        tx = base_tab.get_width() * self.i
        surf.blit(base_tab, (self.x+tx, self.y))
        ix = int(round((base_tab.get_width() - self.img.get_width())/2.))
        iy = int(round((base_tab.get_height() - self.img.get_height())/2.))
        surf.blit(self.img, (self.x+ix+tx, self.y+iy))
        if self.i == self.parent.active_shop_tab:
            for j in range(self.slotny):
                for i in range(self.slotnx):
                    self.item_slots[j][i].draw(surf)
            if self.item:
                mx, my = pygame.mouse.get_pos()
                ix, iy = int(round(self.item.img.get_width()/2.)), int(round(self.item.img.get_height()/2.)) 
                if (mx-ix) < self.x:
                    fx = self.x
                elif (mx+ix) > self.x+tab_background.get_width():
                    fx = self.x+tab_background.get_width()-self.item.img.get_width()
                else:
                    fx = (mx-ix)
                #print(my-iy, self.y, tab_background.get_height())
                if (my-iy) < self.y+base_tab.get_height():
                    fy = self.y+base_tab.get_height()
                elif (my-iy) > self.y+tab_background.get_height():
                    fy = self.y+tab_background.get_height()+base_tab.get_height()-self.item.img.get_height()-3 #-self.item.img.get_height()
                    # print(self.item.img.get_height())
                else:
                    fy = my-iy
                #print(fy)
                surf.blit(self.item.img, (fx, fy))#(mx-ix,my-iy))
    
    def update(self, event):
        for j in range(self.slotny):
            for i in range(self.slotnx):
                self.item_slots[j][i].update(event)

class Shop:
    def __init__(self, x, y, parent=None):
        self.shop_tabs = []
        self.active_shop_tab = 0 # Should go ahead and make this an integer
        self.parent = parent
        self.x = x
        self.y = y
            
    def addTab(self, img, text):
        tTab = ShopTab(img, text, self.x, self.y, len(self.shop_tabs), self)
        self.shop_tabs.append(tTab)
        return tTab
        
    def addItem(self, tabN, item):
        tTab = self.shop_tabs[tabN]
        for j in range(tTab.slotny):
            for i in range(tTab.slotnx):
                tSlot = tTab.item_slots[j][i]
                if tSlot.item == None:
                    tSlot.item = item
                    return tSlot
    
    def addItemAt(self, tabN, i, j, item):
        self.shop_tabs.item_slots[j][i].item = item
    
    def onClick(self):
        pass
    
    def update(self, event):
        #for event in events:
        if event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[0]:
                for x in range(len(self.shop_tabs)):
                    # Might be worthwhile to generate these rects...
                    if pygame.Rect(self.x + (x*base_tab.get_width()), self.y, base_tab.get_width(), base_tab.get_height()-3).collidepoint(pygame.mouse.get_pos()):
                        self.active_shop_tab = x
        self.shop_tabs[self.active_shop_tab].update(event) # who cares about unactive ones boi
    
    def draw(self, surf):
        for i in range(len(self.shop_tabs)):
            shop_tab = self.shop_tabs[i]
            if i != self.active_shop_tab:
                shop_tab.draw(surf)
        # Really this is just a management system so just gonna draw the active one last
        surf.blit(tab_background, (self.x, -3+self.y+base_tab.get_height()))
        # print(self.active_shop_tab, len(self.shop_tabs))        
        if len(self.shop_tabs) > 0:
            # print('Quack')
            self.shop_tabs[self.active_shop_tab].draw(surf)

class EquipmentSlot(ItemSlot):
    def __init__(self, x, y, equipmentType, parent):
        ItemSlot.__init__(self, x, y, parent)
        self.equipmenttype = equipmentType
        
    def onDoubleClick(self):
        if self.item:
            for j in range(4):
                for i in range(6):
                    if self.parent.item_slots[j][i].item == None:
                        self.parent.item_slots[j][i].item = self.item
                        self.item = None
    
    def canPlace(self, item):
        if item:
            return self.equipmenttype == item.itemtype
        else:
            return True

class InventorySlot(ItemSlot):
    def __init__(self, x, y, parent):
        ItemSlot.__init__(self, x, y, parent)
        
    def onDoubleClick(self):
        if self.item:
            if self.item.itemtype == 'weapon':
                tItem = self.parent.weapon_item_slot.item
                self.parent.weapon_item_slot.item = self.item
                self.item = tItem
            elif self.item.itemtype == 'shield':
                tItem = self.parent.shield_item_slot.item
                self.parent.shield_item_slot.item = self.item
                self.item = tItem
            elif self.item.itemtype == 'helmet':
                tItem = self.parent.helmet_item_slot.item
                self.parent.helmet_item_slot.item = self.item
                self.item = tItem
            elif self.item.itemtype == 'armour':
                tItem = self.parent.armour_item_slot.item
                self.parent.armour_item_slot.item = self.item
                self.item = tItem
            elif self.item.itemtype == 'pants':
                tItem = self.parent.pants_item_slot.item
                self.parent.pants_item_slot.item = self.item
                self.item = tItem
            elif self.item.itemtype == 'boots':
                tItem = self.parent.boots_item_slot.item
                self.parent.boots_item_slot.item = self.item
                self.item = tItem
            else:
                print(self.item.itemtype)

class InventoryGUI:
    def __init__(self, x, y, player, parent=None):
        self.x = x
        self.y = y
        self.item = None
        self.item_slots = []
        self.last_item_slot = None
        self.parent = parent
        slotx = int(round((inventory_base.get_width() - (6*item_slot.get_width()))/2.))
        sloty = int(round(((inventory_base.get_height() - (4*item_slot.get_width()))/2.) + inventory_base.get_height()/8.))
        centerx = int(round((inventory_base.get_width()-item_slot.get_width())/2.))
        cy = int(round((inventory_base.get_height()-sloty)/6.))
        self.weapon_item_slot = EquipmentSlot(self.x+centerx-(item_slot.get_width()*1.5), cy*2.5, 'weapon', self)
        self.weapon_item_slot.item = Item(bone_sword, 25, 'weapon')
        self.shield_item_slot = EquipmentSlot(self.x+centerx+(item_slot.get_width()*1.5), cy*2.5, 'shield', self)
        self.shield_item_slot.item = Item(anevis_wooden_shield, 25, 'shield')
        self.helmet_item_slot = EquipmentSlot(self.x+centerx, cy, 'helmet', self)
        self.helmet_item_slot.item = Item(anevis_leather_helm, 25, 'helmet')
        self.armour_item_slot = EquipmentSlot(self.x+centerx, cy*2, 'armour', self)
        self.armour_item_slot.item = Item(anevis_leather_armor, 25, 'armour')
        self.pants_item_slot = EquipmentSlot(self.x+centerx, cy*3, 'pants', self)
        self.pants_item_slot.item = Item(anevis_leather_pants, 25, 'pants')
        self.boots_item_slot = EquipmentSlot(self.x+centerx, cy*4, 'boots', self)
        self.boots_item_slot.item = Item(anevis_leather_boots, 25, 'boots')
        for j in range(4):
            t = []
            for i in range(6):
                t.append(InventorySlot(self.x+slotx+36*i, self.y+base_tab.get_height() + sloty + 36*j, self))
            self.item_slots.append(t)
    
    def addItem(self, item):
        for j in range(4):
            for i in range(6):
                tItemSlot = self.item_slots[j][i]
                if tItemSlot.item == None:
                    tItemSlot.item = item
                    return 

    def draw(self, surf):
        surf.blit(inventory_base, (self.x, self.y))
        for j in range(4):
            for i in range(6):
                self.item_slots[j][i].draw(surf)
        self.weapon_item_slot.draw(surf)
        self.shield_item_slot.draw(surf)
        self.helmet_item_slot.draw(surf)
        self.armour_item_slot.draw(surf)
        self.pants_item_slot.draw(surf)
        self.boots_item_slot.draw(surf)
        if self.item:
            mx, my = pygame.mouse.get_pos()
            ix, iy = int(round(self.item.img.get_width()/2.)), int(round(self.item.img.get_height()/2.))
            surf.blit(self.item.img, (mx-ix,my-iy))
    
    def update(self, event):
        for j in range(4):
            for i in range(6):
                self.item_slots[j][i].update(event)
        self.weapon_item_slot.update(event)
        self.shield_item_slot.update(event)
        self.helmet_item_slot.update(event)
        self.armour_item_slot.update(event)
        self.pants_item_slot.update(event)
        self.boots_item_slot.update(event)

class Dummy:
    pass

def main():
    # Create screen
    screen = pygame.display.set_mode((160 + inventory_base.get_width(), max(160, inventory_base.get_height())))
    manager = GUIManager()
    character = Dummy()
    character.__dict__.update({'items':[], 'weapon':None, 'shield':None, 'helmet': None, 'armour': None, 'pants': None, 'boots': None}) 
    inventoryGUI = InventoryGUI(160, 0, character)    
    iy = int(round((max(160, inventory_base.get_height()) - 160)/2.))
    pygame.display.set_caption('Shop')
    pyShop = Shop(0, iy)
    pyShop.addTab(potion_tab, 'Potions').generateItemSlots(4, 3)
    pyShop.addTab(weapons_tab, 'Weapons').generateItemSlots(4, 3)
    pyShop.addTab(armour_tab, 'Armour').generateItemSlots(4, 3)
    pyShop.addItem(0, Item(health_potion, 10))
    pyShop.addItem(0, Item(mana_potion, 10))
    pyShop.addItem(0, Item(mystery_potion, 10))
    pyShop.addItem(1, Item(claws, 10, 'weapon'))
    pyShop.addItem(1, Item(anevis_ranger_sword, 25, 'weapon'))
    pyShop.addItem(1, Item(anevis_crossbow, 25, 'weapon'))
    pyShop.addItem(2, Item(anevis_leather_helm, 25, 'helmet'))
    pyShop.addItem(2, Item(anevis_leather_armor, 25, 'armour'))
    pyShop.addItem(2, Item(anevis_leather_pants, 25, 'pants'))
    pyShop.addItem(2, Item(anevis_leather_boots, 25, 'boots'))
    pyShop.addItem(2, Item(anevis_wooden_shield, 25, 'shield'))
    # Not much else to do other than maybe a header for the shop as well as allowing the 
    manager.openGUI('inventory', inventoryGUI)
    manager.openGUI('shop', pyShop)
    while True:
        screen.fill((0, 0, 0))
        event = pygame.event.poll()
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        manager.mainloop(event, screen)
        #pyShop.update(event)
        #inventoryGUI.update(event)
        #pyShop.draw(screen)
        #inventoryGUI.draw(screen)
        pygame.display.flip()

if __name__ == '__main__':
    main()