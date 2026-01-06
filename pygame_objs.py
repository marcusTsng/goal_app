# CONSTANTS
BG_COLOUR = (0,0,0)
SCREEN_WIDTH, SCREEN_HEIGHT = 414, 896
TILE_COL = (48, 143, 44)

# SETUP
import pygame 
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# SPRITE CLASSES
class Sprite:
    active_sprites = []

    def __init__(self, w, l, x=0, y=0):
        Sprite.active_sprites.append(self)
        self.active = True
        self.rect = pygame.Rect(x, y, w, l)   
    
    def set_pos(self, x, y):  self.rect.center = (x,y)
    def get_pos(self): return self.rect.center[0], self.rect.center[1]

    def display(self): pass
    
    def set_active(self, active=True): 
        self.active = active
        if active: Sprite.active_sprites.append(self)
        else: Sprite.active_sprites.remove(self)

    @staticmethod
    def displaySprites():
        for x in Sprite.active_sprites:
            if not x.active: x.set_active(False)
            else: x.display()

class ImageSprite(Sprite):
    def __init__(self, path, x=0, y=0, tint=None):
        super().__init__(0, 0, x, y)
        try:
            self.img = pygame.image.load(f"Assets/{path}").convert_alpha()
        except pygame.error as e: 
            self.img = pygame.image.load(f"Assets/placeholder.png").convert_alpha()
        if tint: self.img.fill((tint), special_flags=pygame.BLEND_ADD)
        self.rect = self.img.get_rect(center=(x,y))  
    def display(self):
        screen.blit(self.img, self.rect)

class RectSprite(Sprite):
    def __init__(self, fill, w, l, x=0, y=0):
        super().__init__(w, l, x, y)
        self.fill = fill
    def display(self):
        pygame.draw.rect(screen, self.fill, self.rect)

# BUTTONS
class Button(RectSprite):
    buttons = []
    def __init__(self, fill, w, l, x=0, y=0, func = None):
        super().__init__(fill, w, l, x, y)
        Button.buttons.append(self)
        self.func = func
    def set_function(self, func): self.func = func
    def check_hover(self):
        if not self.active: return False
        
        mouse_x, mouse_y = pygame.mouse.get_pos()
        x, y = self.get_pos()
        if (mouse_x > x - self.rect.width / 2 and mouse_x < x + self.rect.width / 2) and (mouse_y > y - self.rect.height / 2 and mouse_y < y + self.rect.height / 2):
            if self.func: self.func()
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

# GAME OBJECTS
class Tile(ImageSprite):
    center_tile = None

    def __init__(self, relative_x = 0, relative_y = 0, color=TILE_COL):
        super().__init__("Terrain/Tile.png", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, color)
        self.relative_x = relative_x
        self.relative_y = relative_y
        if not Tile.center_tile: 
            Tile.center_tile = self
        else:
            self.rect.center = (SCREEN_WIDTH / 2 + 50 * relative_x + 50 * relative_y, SCREEN_HEIGHT / 2 + 32 * relative_x - 32 * relative_y)