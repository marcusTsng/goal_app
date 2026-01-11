# CONSTANTS/STATICS
BG_COLOUR = (0,0,0)
SCREEN_WIDTH, SCREEN_HEIGHT = 414, 896
TILE_COL = (48, 143, 44)
SCREEN_OFFSET = (0,0)
BUTTON_BASE_COLORS = (60,60,60)#(230,145,56)
PANEL_BG_COLOR = (30,30,30,180)
SELECTION_TINT = (180,180,180)

TAB = "main" 

# SETUP
import pygame, random, time
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# FUNCTIONS
scroll_offset = 0
scroll_sensitivity = 1
projects = []
task_selected_in_menu = None
selector_height = None
def update_projects(proj):
    global projects 
    projects = proj
def get_scroll_offset():
    return scroll_offset
def select_from_index(i, text):
    global task_selected_in_menu, selector_height
    task_selected_in_menu = text
    selector_height = i * 50 + 220
def display_text(text, font, pos, color = (255,255,255), scrollable = False, clip_rect = None, selectable = False):
    global scroll_offset, task_selected_in_menu, selector_height

    # scrolling
    off = 0
    if scrollable: 
        clamp = -50 * (len(projects) - 1)
        if scroll_offset > 0: scroll_offset = 0
        elif scroll_offset <= clamp: scroll_offset = clamp
        off = scroll_offset
    draw_y = pos[1] + off

    # Rendering
    if selector_height == pos[1] and task_selected_in_menu:
        text_surface = font.render(text, True, SELECTION_TINT)
    else:
        text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(topleft=(pos[0], draw_y))

    # Handle selection when selectable = True
    if selectable:
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()[0]  # left mouse button

        if mouse_pressed and text_rect.collidepoint(mouse_pos):
            task_selected_in_menu = text
            selector_height = pos[1]

    # clip text for scrolling
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

def get_selected_task_name(): return task_selected_in_menu
def get_selected_task_height(): 
    if task_selected_in_menu: return selector_height
    else: return None

def deselect_task_in_menu(): 
    global task_selected_in_menu
    task_selected_in_menu = None

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

    def __init__(self, w, l, x=0, y=0, priority = 0, clip_rect= None):
        Sprite.active_sprites.append(self)
        if priority > Sprite.max_priority: Sprite.max_priority = priority
        if priority < 0: priority = 0

        self.active = True
        self.clip_rect = clip_rect
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
    def __init__(self, path, x=0, y=0, tint=None, use_offset=False, priority=0, clip_rect=None):
        super().__init__(0, 0, x, y, priority, clip_rect)
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

        old_clip = screen.get_clip()
        if self.clip_rect:
            screen.set_clip(self.clip_rect)

        pos_rect = pygame.Rect(0,0,self.rect.width, self.rect.height)
        pos_rect.center = (self.rect.centerx + offx, self.rect.centery + offy)
        screen.blit(self.img, pos_rect)

        screen.set_clip(old_clip)

class RectSprite(Sprite):
    def __init__(self, fill, w, l, x=0, y=0, priority=0, clip_rect=None):
        super().__init__(w, l, x, y, priority, clip_rect)
        self.fill = fill
        self.surface = pygame.Surface((w, l), pygame.SRCALPHA)
        if len(fill) == 3: 
            r,g,b = fill
            fill = (r,g,b, 255)
        self.surface.fill(fill)
    def display(self):
        screen.blit(self.surface, (self.rect.x, self.rect.y))
        # pygame.draw.rect(self.surface, self.fill, self.rect)

# TEXTBOX
# class Textbox:
#     textboxes = []
    
#     def __init__(self, x, y, w, h, default_text = "Empty", text_color=(255,255,255), blank_text_color=(100,100,100), bg_color=None):
#         self.active = False
#         self.text = default_text
#         self.default_text = default_text
#         self.empty = True
#         self.rect = pygame.Rect(x, y, w, h)
#         self.bg_color = bg_color
#         self.color = text_color
#         self.blank_color = blank_text_color
#         Textbox.textboxes.append(self)

#     def set_active(self, bool): self.active = bool

#     def display(self):
#         if self.bg_color != None:
#             pygame.draw.rect(screen, self.bg_color, self.rect)
#         if self.text == "": self.empty = True
#         if self.empty: 
#             self.text = self.default_text

#     @staticmethod
#     def display_all():
#         for x in Textbox.textboxes:
#             if not x.active: x.display()
class Textbox:
    textboxes = []
    active_textbox = None  # only one textbox active at a time (like most UIs)

    def __init__(self, x, y, w, h, default_text="Enter text...", 
                 text_color=(255,255,255), 
                 blank_text_color=(100,100,100), 
                 bg_color=None, 
                 font=None):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = ""
        self.default_text = default_text
        self.color = text_color
        self.blank_color = blank_text_color
        self.bg_color = bg_color
        self.active = False
        self.in_use = False
        self.font = font if font else pygame.font.Font(None, 32)  # default font

        Textbox.textboxes.append(self)

    def set_active(self, active=True):
        self.active = active


    def set_use(self, in_use=True):
        # Deactivate previous active textbox
        if in_use and Textbox.active_textbox and Textbox.active_textbox != self:
            Textbox.active_textbox.in_use = False
        
        self.in_use = in_use
        if in_use:
            Textbox.active_textbox = self
        elif Textbox.active_textbox == self:
            Textbox.active_textbox = None

    def handle_event(self, event):
        """Call this in your main event loop when the textbox is active"""
        if not self.in_use:
            return False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            elif event.key == pygame.K_RETURN or event.key == pygame.K_ESCAPE:
                self.set_use(False)  # exit editing
            elif event.unicode.isprintable():  # only printable characters
                self.text += event.unicode
            return True
        return False

    def display(self):
        if not self.active: return

        # Background
        if self.bg_color is not None:
            pygame.draw.rect(screen, self.bg_color, self.rect)
            # Optional: border when active
            if self.in_use:
                pygame.draw.rect(screen, (100, 180, 255), self.rect, 2, border_radius=4)

        # Text content
        display_text = self.text if self.text else self.default_text
        color = self.color if self.text else self.blank_color

        text_surf = self.font.render(display_text, True, color)
        
        # Center vertically, pad left a bit
        text_x = self.rect.x + 8
        text_y = self.rect.centery - text_surf.get_height() // 2
        
        # Simple clipping so text doesn't go outside box
        old_clip = screen.get_clip()
        screen.set_clip(self.rect)
        screen.blit(text_surf, (text_x, text_y))
        screen.set_clip(old_clip)

        # Optional: blinking cursor when active
        if self.in_use and (pygame.time.get_ticks() // 500) % 2 == 0:
            cursor_x = text_x + text_surf.get_width() + 2
            if cursor_x < self.rect.x + self.rect.width:
                pygame.draw.line(screen, self.color, 
                            (cursor_x, text_y), 
                            (cursor_x, text_y + text_surf.get_height()), 2)

    @staticmethod
    def update_all():
        """Call this once per frame instead of display_all"""
        for tb  in Textbox.textboxes:
            tb.display()
            

    @staticmethod
    def check_click(pos):
        """Call this when mouse is clicked (in event loop)"""
        for tb in Textbox.textboxes:
            if tb.rect.collidepoint(pos):
                tb.set_use(True)
                return True
        # Clicked outside → deactivate current
        if Textbox.active_textbox:
            Textbox.active_textbox.set_use(False)
        return False
            


# BUTTONS
class Button(ImageSprite):
    buttons = []
    
    def __init__(self, path, x=0, y=0, tint=None, func=None, params=None, use_offset=False, priority=0, tab="main", clip_rect=None):
        super().__init__(path, x, y, tint, use_offset, priority, clip_rect)
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
    
    def __init__(self, relative_x = 0, relative_y = 0, color=TILE_COL, priority=1, structure = None):
        super().__init__("Terrain/Tile.png", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, color, Tile.select_tile, self, True, priority)
        self.relative_x = relative_x
        self.relative_y = relative_y
        self.building = None
        self.floors = 0
        self.structure = structure
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
    
    @staticmethod
    def build_structure(tile):
        if tile.structure == None:
            tile.structure = Structure(tile, Structure.types["hut"])
        else:
            tile.structure.upgrade()
    
    def get_points_needed(self):
        if self.structure == None: return 5
        else: return self.structure.points_needed

    def to_dict(self):
        """Convert this Project to a JSON-serializable dictionary"""
        structure = None
        if self.structure: structure = self.structure.to_dict()             
        return {
            "relative_x": self.relative_x,
            "relative_y": self.relative_y,
            "structure": structure
        }

    # @classmethod
    # def from_dict(cls, data):
    #     """Reconstruct a Project from a dictionary (used when loading)"""
    #     # Create new instance
    #     project = cls(
    #         relative_x = data["relative_x"],
    #         relative_y = data["relative_y"],
    #         structure = data["structure"].from_dict(),
    #     )

    #     # Restore extra fields (index is important!)
    #     project.index = data.get("index", 0)

    #     return project
    @classmethod
    def from_dict(cls, data):
        tile = cls(
            relative_x=data["relative_x"],
            relative_y=data["relative_y"]
        )
        # Do NOT recreate structure here — it's done in load_tiles_DS
        return tile
    
# class Structure(ImageSprite):
#     types = {
#         "hut" : {
#             "name": "Hut",
#             "upgraded_name": "Tower",
#             "level_height": 8,
#             "bottom_level_height": 11,
#             "bottom" : "Structures/Hut/hut_single_floor.png", 
#             "mid" : "Structures/Hut/hut_mid_floor.png", 
#             "top" :"Structures/Hut/hut_top_floor.png"
#         }
#     }

#     def __init__(self, tile : Tile, structure_type=types["hut"]):
#         pos=tile.get_pos()
#         super().__init__(structure_type["bottom"], pos[0], pos[1], use_offset=True)
#         self.priority = tile.priority
#         self.level = 1
#         self.tile = tile
#         self.points_needed = 5
#         self.upgrade_time = time.time()
#         self.name = structure_type["name"]
#         self.struct = structure_type

#     def upgrade(self):
#         if time.time() - self.upgrade_time > 0.5:
#             self.upgrade_time = time.time()
#             self.points_needed += 5
#             self.level += 1
#             self.name = self.struct["upgraded_name"]
#             Floor(self.tile.get_pos(), self.level, self.struct["level_height"], self.struct["bottom_level_height"], self.struct["top"])

#     def to_dict(self):
#         """Convert this Project to a JSON-serializable dictionary"""
#         return {
#             # FINISH THIS            
#         }

#     @classmethod
#     def from_dict(cls, data):
#         """Reconstruct a Project from a dictionary (used when loading)"""
#         # Create new instance
#         project = cls(
#             # FINISH THIS
#         )

#         # Restore extra fields (index is important!)
#         project.index = data.get("index", 0)

#         return project

# class Floor(ImageSprite):
#     def __init__(self, base_pos, level, level_height, init_level_height, path):
#         add = level * level_height if level != 2 or level != 3 else init_level_height
#         x = base_pos[0]
#         y = base_pos[1]-add
#         super().__init__(path, x, y, use_offset=True, priority=1)
class Structure(ImageSprite):
    types = {
        "hut" : {
            "name": "Hut",
            "upgraded_name": "Tower",
            "level_height": 8,
            "bottom_level_height": 11,
            "bottom" : "Structures/Hut/hut_single_floor.png", 
            "mid" : "Structures/Hut/hut_mid_floor.png", 
            "top" :"Structures/Hut/hut_top_floor.png"
        }
    }

    def __init__(self, tile : Tile, structure_type=types["hut"]):
        pos=tile.get_pos()
        super().__init__(structure_type["bottom"], pos[0], pos[1], use_offset=True)
        self.priority = tile.priority
        self.level = 1
        self.tile = tile
        self.points_needed = 5
        self.upgrade_time = time.time()
        self.name = structure_type["name"]
        self.struct = structure_type

    def upgrade(self):
        if time.time() - self.upgrade_time > 0.5:
            self.upgrade_time = time.time()
            self.points_needed += 5
            self.level += 1
            self.name = self.struct["upgraded_name"]
            Floor(self.tile.get_pos(), self.level, self.struct["level_height"], self.struct["bottom_level_height"], self.struct["top"])

    def to_dict(self):
        """Convert this Project to a JSON-serializable dictionary"""
        return {
            "type_name": "hut",  # currently only hut exists - change when adding more types
            "level": self.level,
            "points_needed": self.points_needed,
            "upgrade_time": self.upgrade_time,
            # we don't need to save tile reference - we rebuild from tile data
        }

    @classmethod
    def from_dict(cls, data):
        """Reconstruct a Project from a dictionary (used when loading)"""
        # Note: this assumes the tile already exists when loading
        # You'll need to call this after the tile is recreated
        # For now we return None - real implementation needs tile context
        # In practice you should create Structure after loading the tile
        raise NotImplementedError(
            "Structure.from_dict needs the associated Tile instance. "
            "Call manually after tile reconstruction."
        )
        # Example of how it would look if tile were passed:
        # tile = ... # get tile from loaded data
        # structure_type = cls.types[data["type_name"]]
        # instance = cls(tile, structure_type)
        # instance.level = data["level"]
        # instance.points_needed = data["points_needed"]
        # instance.upgrade_time = data["upgrade_time"]
        # return instance

class Floor(ImageSprite):
    def __init__(self, base_pos, level, level_height, init_level_height, path):
        add = level * level_height if level != 2 or level != 3 else init_level_height
        x = base_pos[0]
        y = base_pos[1]-add
        super().__init__(path, x, y, use_offset=True, priority=1)

    def to_dict(self):
        return {
            "level": self.level,  # if you added self.level = level in __init__
            "path": self.img_path,  # you'll need to store this or derive it
            "x": self.rect.centerx,
            "y": self.rect.centery
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            base_pos=(data["x"], data["y"]),
            level=data["level"],
            level_height=8,                    # hardcoded for hut - improve later
            init_level_height=11,              # hardcoded for hut
            path=data["path"]                  # assumes you saved the path
        )