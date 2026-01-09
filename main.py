import pygame
import random
import math
import time

from pygame_objs import *

pygame.init()
pygame.display.set_caption("VOYAGE")
title_font = pygame.font.SysFont('arialrounded', 60)
main_font = pygame.font.SysFont('arialrounded', 30)

# pygame.init()
# fonts = pygame.font.get_fonts()
# print(f"Total fonts available on this system: {len(fonts)}\n")
# print("List of available fonts:")
# for f in fonts:
#     print(f"* {f}")


def addTile():
    x,y = Tile.get_random_placement()
    Tile(x,y)
for _ in range(5): addTile()

def addBuilding():
    print("Pls make ts")

# def taskDisplay():
#     for i in range(len(Task.tasks)):
#         text_surface = my_font.render("gragr", False, (255, 255, 255))
#         screen.blit(text_surface, (207, 448))


class Task:
    tasks = []
    taskName = []
    completedTasks = []
    lastIndex = 0
    def __init__(self, name):
        self.name = name
        self.index = Task.lastIndex
        Task.taskName.append(self.name)
        Task.tasks.append(self)
        Task.lastIndex+=1

    def complete(self):
        Task.completedTasks.append(self)
        Task.tasks.pop(self.index)
    def delete(self): del self

    @staticmethod
    def printTasks():
        print("---")
        for t in Task.tasks: print(t.name)

class Routine(Task):
    routines = []
    routineNames = []
    completedRoutines = []
    lastIndexR = 0
    def __init__(self, name, frequency):
        super().__init__(name)
        self.name = name
        self.frequency = frequency
        self.index = Routine.lastIndexR
        Routine.routineNames.append(self.name)
        Routine.routines.append(self)
        Routine.lastIndexR += 1
    def completeR(self):
        Routine.completedRoutines.append(self)
        Routine.routines.pop(self.index)


class Project(Task):
    projects = []
    projectNames = []
    completedProjects = []
    lastIndexP = 0 # this thing it bad order bad booboo
    def __init__(self, name, duration):
        super().__init__(name)
        self.name = name
        self.duration = duration
        self.index = Project.lastIndexP
        Project.projectNames.append(self.name)
        Project.projects.append(self)
        Project.lastIndexP += 1
    def completeP(self):
        Project.completedProjects.append(self)
        print(self.index)
        Project.projects.pop(self.index)
        addTile()

pp = Project("pp", 10)
dih = Project("pp", 10)





# test
# Task.printTasks()
# task = Task("task")
# task2 = Task("task2")
# task3= Task("task3")
# Task.printTasks()
# task2.complete()
# Task.printTasks()

### SPRITES AND OTHER VARIABLES

center_tile = Tile(color=(255,255,255))
center_tile.set_building("Hut")
center_tile.add_floor()
# tile1 = Tile(0, 1)
# tile2 = Tile(0, -1)
# tile3 = Tile(1, 0)
# tile4 = Tile(-1, 0)



## UI SETUP

add_button = Button("placeholder.png", 100, 750, priority=2)
complete_button = Button("placeholder.png", 250, 750, priority=2, tint=(255,0,0))

def make():
    test = Project("pp", 10)#Make user input stuff
    complete_button.set_function(test.completeP)
add_button.set_function(make)


add = Button("Buttons/add_button.png", 30, 30, BUTTON_BASE_COLORS)
view_routines = Button("Buttons/list_button.png", 80, 30, BUTTON_BASE_COLORS)
view_projects = Button("Buttons/list_button.png", 130, 30, BUTTON_BASE_COLORS)

menu = PopUp(
    base=RectSprite((30,30,30,180),SCREEN_WIDTH, SCREEN_HEIGHT, 0, 0),
    items=[
        Button("Buttons/cancel_button.png", 50, 50, BUTTON_BASE_COLORS, priority=10, tab="menu"),
        add_button, complete_button
    ],
    hide_buttons=[add, view_routines, view_projects],
    set_tab="menu",
    priority = 9
)
pmenu = PopUp(
    base=RectSprite((30,30,30,180),SCREEN_WIDTH, SCREEN_HEIGHT, 0, 0),
    items=[
        Button("Buttons/cancel_button.png", 50, 50, BUTTON_BASE_COLORS, priority=10, tab="pmenu"),
        add_button, complete_button
    ],
    hide_buttons=[add, view_routines, view_projects],
    set_tab="pmenu",
    priority = 9
)

tile_data_tab = PopUp(
    base=RectSprite((30,30,30,180), SCREEN_WIDTH, 300, 0, SCREEN_HEIGHT-300),
    items=[],
    priority=8
)

def switch_to_menu(name):
    if name == "menu":
        menu.set_active(True)
    elif name == "pmenu": 
        pmenu.set_active(True)
    set_tab(name)
def hide_menus(): 
    menu.set_active(False)
    pmenu.set_active(False)
    set_tab("main")

# BUTTON SETUP
menu.items[1].set_function(hide_menus)
pmenu.items[1].set_function(hide_menus)
view_projects.set_function(switch_to_menu, "pmenu")
view_routines.set_function(switch_to_menu, "menu")
add.set_function(make)

### MAIN GAME LOOP
dragging = False
button_down_time = 0
click_threshold = 0.2
drag_base = (0,0) # for dragging

running = True
tab = get_tab()

background_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
draw_gradient(background_surface, (0,23,45), (0,0,0))

while running:
    mouse_pos = pygame.mouse.get_pos()
    current_tab = get_tab()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            button_down_time = time.time()
            dragging = True
            drag_base = mouse_pos
        if event.type == pygame.MOUSEBUTTONUP:
            if time.time() - button_down_time < click_threshold: 
                Button.check_all_hovers()
            dragging = False
        
        if event.type == pygame.MOUSEWHEEL and current_tab == "menu":
            menu_scroll(event.y * 10)

    
    if dragging and time.time() - button_down_time > click_threshold: 
        dx = mouse_pos[0] - drag_base[0]
        dy = mouse_pos[1] - drag_base[1]
        
        if current_tab == "main":
            new_offset = (SCREEN_OFFSET[0] + dx, SCREEN_OFFSET[1] + dy)
            SCREEN_OFFSET = new_offset
            set_screen_offset(new_offset)
        elif current_tab == "menu":
            menu_scroll(dy)

        drag_base = mouse_pos
    
    screen.blit(background_surface, (0, 0))
    # screen.fill(BG_COLOUR)
    Sprite.displaySprites()
    if current_tab == "menu":
        Tile.deselect_tiles()
        tile_data_tab.set_active(False)

        text = ""
        display_text("Routines", title_font, (80, 110))
        for i in range(len(Routine.routineNames)):
            text = f"{Routine.routineNames[i]}"
            display_text(
                text, main_font,
                (80, 170 + 50*(i+1)),
                scrollable = True,
                clip_rect=pygame.Rect(80, 220, SCREEN_WIDTH - 160, 400)
            )
            text = ""
            display_text(
                text, main_font,
                (80, 170 + 50 * (i + 1)),
                scrollable = True,
                clip_rect=pygame.Rect(80, 220, SCREEN_WIDTH - 160, 400)
            )
            # text_surface = my_font.render(text, False, (255, 255, 255))
            # screen.blit(text_surface, (80, 170 + 50*(i+1)))
    elif current_tab == "pmenu":
        Tile.deselect_tiles()
        tile_data_tab.set_active(False)

        text = ""
        display_text("Projects", title_font, (80, 110))
        for i in range(len(Project.projectNames)):
            text = f"{Project.projectNames[i]}" # LIAM
            display_text(
                text, main_font,
                (80, 170 + 50*(i+1)),
                scrollable = True,
                clip_rect=pygame.Rect(80, 220, SCREEN_WIDTH - 160, 400)
            )
            text = ""
            display_text(
                text, main_font,
                (80, 170 + 50 * (i + 1)),
                scrollable = True,
                clip_rect=pygame.Rect(80, 220, SCREEN_WIDTH - 160, 400)
            )

    if Tile.selected != None:
        tile_data_tab.set_active(True)
        display_text("Empty tile", main_font, (30, SCREEN_HEIGHT-250))
    else:
        tile_data_tab.set_active(False)
    

    pygame.display.flip()
    update_projects(Project.projects)

pygame.quit()