# CONSTANTS/STATICS
BG_COLOUR = (0,0,0)
SCREEN_WIDTH, SCREEN_HEIGHT = 414, 896
TILE_COL = (48, 143, 44)
SCREEN_OFFSET = (0,0)
BUTTON_BASE_COLORS = (100,100,100)#(230,145,56)
PANEL_BG_COLOR = (30,30,30,180)

TAB = "main" # tab can be main, menu, add

# SETUP
import pygame 
import random
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# FUNCTIONS
scroll_offset = 0
scroll_sensitivity = 1
projects = []
def update_projects(proj):
    global projects 
    projects = proj
def display_text(text, font, pos, color = (255,255,255), scrollable = False, clip_rect = None):
    global scroll_offset
    off = 0
    text_surface = font.render(text, False, color)
    if scrollable: 
        clamp = 50 * len(projects)
        if scroll_offset > 0: scroll_offset = 0
        elif scroll_offset <= clamp: scroll_offset = clamp
        off = scroll_offset
    draw_y = pos[1] + off

    if clip_rect:
        old_clip = screen.get_clip()
        if isinstance(clip_rect, pygame.Rect):
            screen.set_clip(clip_rect)
        else:
            screen.set_clip(pygame.Rect(clip_rect))
        screen.blit(text_surface, (pos[0], draw_y))
        screen.set_clip(old_clip)
    else:
        screen.blit(text_surface, (pos[0], draw_y))

    # screen.blit(text_surface, (pos[0], pos[1] + off))
def menu_scroll(dy): 
    global scroll_offset
    scroll_offset += scroll_sensitivity * dy

def set_screen_offset(pos): 
    global SCREEN_OFFSET
    SCREEN_OFFSET = pos

def get_tab(): return TAB
def set_tab(tab): 
    global TAB
    TAB = tab


def draw_gradient(surface, start_color, end_color):
    """Draws a vertical linear gradient on the surface."""
    # Convert colors to pygame.Color objects for easier manipulation
    c1 = pygame.Color(start_color)
    c2 = pygame.Color(end_color)
    
    # Calculate color step per pixel height
    height = surface.get_height()
    for y in range(height):
        # Linear interpolation of color based on the y position
        # lerp() blends two colors by a factor (0.0 to 1.0)
        color = c1.lerp(c2, y / height)
        # Draw a 1-pixel-high rectangle across the entire width
        pygame.draw.rect(surface, color, (0, y, surface.get_width(), 1))

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
        elif self in Sprite.active_sprites: Sprite.active_sprites.remove(self)

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
        self.surface = pygame.Surface((w, l), pygame.SRCALPHA)
        if len(fill) == 3: 
            r,g,b = fill
            fill = (r,g,b, 255)
        self.surface.fill(fill)
    def display(self):
        screen.blit(self.surface, (self.rect.x, self.rect.y))
        # pygame.draw.rect(self.surface, self.fill, self.rect)

# BUTTONS
class Button(ImageSprite):
    buttons = []
    
    def __init__(self, path, x=0, y=0, tint=None, func=None, params=None, use_offset=False, priority=0, tab="main"):
        super().__init__(path, x, y, tint, use_offset, priority)
        Button.buttons.append(self)
        self.func = func
        self.params = params
        self.tab = tab
        
        # Create mask once for pixel-perfect collision (uses alpha channel)
        self.mask = pygame.mask.from_surface(self.img)

    def set_function(self, func, params=None): 
        self.func = func
        self.params = params

    def check_hover(self):
        if not self.active or get_tab() != self.tab:
            return False
        
        mouse_x, mouse_y = pygame.mouse.get_pos()
        
        # Get button's top-left position on screen (accounting for offset)
        offx, offy = (SCREEN_OFFSET[0], SCREEN_OFFSET[1]) if self.use_offset else (0, 0)
        button_x = self.rect.centerx + offx - self.img.get_width() // 2
        button_y = self.rect.centery + offy - self.img.get_height() // 2
        
        # Relative mouse position within the button image
        rel_x = mouse_x - button_x
        rel_y = mouse_y - button_y
        
        # Quick bounds check
        if rel_x < 0 or rel_y < 0 or rel_x >= self.img.get_width() or rel_y >= self.img.get_height():
            return False
        
        # Pixel-perfect check
        if self.mask.get_at((int(rel_x), int(rel_y))):
            if self.func:
                if self.params is not None:
                    self.func(self.params)
                else:
                    self.func()
            return True
        
        return False
    
    def set_active(self, active=True):
        self.active = active
        if active: 
            if self not in Sprite.active_sprites:
                Sprite.active_sprites.append(self)
            if self not in Button.buttons:
                Button.buttons.append(self)
        else: 
            if self in Sprite.active_sprites:
                Sprite.active_sprites.remove(self)
            if self in Button.buttons:
                Button.buttons.remove(self)

    @staticmethod
    def check_all_hovers():
        is_Tile = False
        for x in Button.buttons:
            if x.check_hover() and isinstance(x, Tile): is_Tile = True
        if not is_Tile: Tile.deselect_tiles()
class PopUp:
    def __init__(self, items : dict = None, base : RectSprite = None, hide_buttons = [], set_tab = None, priority = 1):
        if not items: items = []
        # if not base:  base = RectSprite((100,100,100), SCREEN_HEIGHT, 200, 0, SCREEN_HEIGHT-200, priority=3)
        items.insert(0, base)
        self.base = base
        self.items = items
        self.active = False
        self.hide_buttons = hide_buttons
        self.set_tab = set_tab
        self.base.priority = priority
        self.set_active(False)

        for x in self.items:
            if x != self.base: x.rect.center = (x.rect.centerx + base.rect.x, x.rect.centery + base.rect.y)
            x.tab = set_tab
            x.priority = priority + 1

    def set_active(self, bool): 
        self.active = bool
        for x in self.hide_buttons: x.set_active(not bool)
        for x in self.items: x.set_active(bool)

        if bool and self.set_tab: set_tab(self.set_tab)
        elif not bool and self.set_tab: set_tab("main")
    def toggle_active(self): self.set_active(not self.active)

# GAME OBJECTS
class Tile(Button):
    center_tile = None
    tiles = []
    selector = ImageSprite("Terrain/tile_selection.png", 0, 0, (255,255,255), priority=2, use_offset=True)
    selector.set_active(False)
    selected = None
    
    def __init__(self, relative_x = 0, relative_y = 0, color=TILE_COL, priority=1):
        super().__init__("Terrain/Tile.png", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, color, Tile.select_tile, self, True, priority)
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
    def select_tile(tile): 
        Tile.selector.rect.center = tile.rect.center
        Tile.selector.set_active(True)
        Tile.selected = tile
    @staticmethod
    def deselect_tiles(): 
        Tile.selector.set_active(False)
        Tile.selected = None

    @staticmethod
    def get_random_placement():
        if len(Tile.tiles) == 0: return 0, 0

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
    
# class Structure(ImageSprite):
#     types = {
#         "hut" : ["Structures/Hut/hut_single_floor", "Structures/Hut/hut_mid_floor", "Structures/Hut/hut_top_floor"]
#     }

    # def __init__(self, tile : Tile, structure_type=types.hut):
    #     pos=tile.get_pos()
    #     super().__init__(structure_type[0], pos[0], pos[1], use_offset=True)
    #     self.priority = tile.priority