# CONSTANTS
BG_COLOUR = (0,0,0)
SCREEN_WIDTH, SCREEN_HEIGHT = 414, 896
TILE_COL = (48, 143, 44)
SELECTION_TINT = (30,30,30)
SCREEN_OFFSET = (0,0)

# SETUP
import pygame 
import random
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# FUNCTIONS
def set_screen_offset(pos): 
    global SCREEN_OFFSET
    SCREEN_OFFSET = pos

# SPRITE CLASSES
class Sprite:
    active_sprites = []
    max_priority = 0

    def __init__(self, w, l, x=0, y=0, priority = 0):
        Sprite.active_sprites.append(self)
        if priority > Sprite.max_priority: Sprite.max_priority = priority
        if priority < 0: priority = 0

        self.active = True
        self.rect = pygame.Rect(x, y, w, l)   
        self.use_offset = False
        self.priority = priority
    
    def set_pos(self, x, y):  self.rect.center = (x,y)
    def get_pos(self): return self.rect.center[0], self.rect.center[1]

    def display(self): pass
    
    def set_active(self, active=True): 
        self.active = active
        if active: Sprite.active_sprites.append(self)
        else: Sprite.active_sprites.remove(self)

    @staticmethod
    def displaySprites():
        for p in range(Sprite.max_priority + 1):
            for x in Sprite.active_sprites:
                if x.priority != p: continue
                if not x.active: x.set_active(False)
                else: x.display()



class ImageSprite(Sprite):
    def __init__(self, path, x=0, y=0, tint=None, use_offset=False, priority=0):
        super().__init__(0, 0, x, y, priority)
        try:
            self.img = pygame.image.load(f"Assets/{path}").convert_alpha()
        except pygame.error as e: 
            self.img = pygame.image.load(f"Assets/placeholder.png").convert_alpha()
        if tint: self.img.fill((tint), special_flags=pygame.BLEND_ADD)
        self.rect = self.img.get_rect(center=(x,y))  
        self.use_offset = use_offset
    def display(self):
        offx, offy = 0,0
        if self.use_offset: offx, offy = SCREEN_OFFSET[0], SCREEN_OFFSET[1]

        pos_rect = pygame.Rect(0,0,self.rect.width, self.rect.height)
        pos_rect.center = (self.rect.centerx + offx, self.rect.centery + offy)
        screen.blit(self.img, pos_rect)

class RectSprite(Sprite):
    def __init__(self, fill, w, l, x=0, y=0, priority=0):
        super().__init__(w, l, x, y, priority)
        self.fill = fill
    def display(self):
        pygame.draw.rect(screen, self.fill, self.rect)

# BUTTONS
class Button(ImageSprite):
    buttons = []
    def __init__(self, path, x=0, y=0, tint=None, func = None, params = None, use_offset=False, priority=0):
        super().__init__(path, x, y, tint, use_offset, priority)
        Button.buttons.append(self)
        self.func = func
        self.params = params
    def set_function(self, func, params=None): 
        self.func = func
        self.params = params
    def check_hover(self):
        if not self.active: return False
        
        mouse_x, mouse_y = pygame.mouse.get_pos()
        x, y = self.get_pos()
        if (mouse_x > x - self.rect.width / 2 and mouse_x < x + self.rect.width / 2) and (mouse_y > y - self.rect.height / 2 and mouse_y < y + self.rect.height / 2):
            if self.func: 
                if self.params: self.func(self.params)
                else: self.func()
            return True
        return False
    
    def set_active(self, active=True):
        self.active = active
        if active: 
            Sprite.active_sprites.append(self)
            Button.buttons.append(self)
        else: 
            Sprite.active_sprites.remove(self)
            Button.buttons.remove(self)

    @staticmethod
    def check_all_hovers():
        for x in Button.buttons: x.check_hover()

def test(tile): print(f"Tile at {tile.relative_x}, {tile.relative_y} clicked at {pygame.time.get_ticks()}")

# GAME OBJECTS
class Tile(Button):
    center_tile = None
    tiles = []
    
    def __init__(self, relative_x = 0, relative_y = 0, color=TILE_COL, priority=0):
        super().__init__("Terrain/Tile.png", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, color, test, self, True, priority)
        self.relative_x = relative_x
        self.relative_y = relative_y
        self.building = None
        self.floors = 0
        if not Tile.center_tile: 
            Tile.center_tile = self
        else:
            self.rect.center = (SCREEN_WIDTH / 2 + 50 * relative_x + 50 * relative_y, SCREEN_HEIGHT / 2 + 32 * relative_x - 32 * relative_y)
        Tile.tiles.append(self)

    def set_building(self, name):
        self.building = name
    def add_floor(self):
        if self.building == None: print("No building on tile to build on")
        else: self.floors += 1

    @staticmethod
    def get_random_placement():
        isTaken = True
        t = None
        while isTaken:
            t = Tile.tiles[random.randint(0, len(Tile.tiles) - 1)]
            ntx = t.relative_x
            nty = t.relative_y
            c = random.randint(1,4)
            if c == 1:  ntx += 1
            elif c == 2: ntx -= 1
            elif c == 3: nty += 1
            elif c == 4: nty -= 1
            isTaken = False
            for x in Tile.tiles:
                if x.relative_x == ntx and x.relative_y == nty: 
                    isTaken = True
        return ntx, nty