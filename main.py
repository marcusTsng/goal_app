import pygame
import random
import math
import time

from pygame_objs import *

pygame.init()
pygame.display.set_caption("VOYAGE")
title_font = pygame.font.SysFont('arialrounded', 60)
main_font = pygame.font.SysFont('arialrounded', 30)
description_font = pygame.font.SysFont('arialrounded', 15)

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
    print("Pls make ts") # MARCUS

# def taskDisplay():
#     for i in range(len(Task.tasks)):
#         text_surface = my_font.render("gragr", False, (255, 255, 255))
#         screen.blit(text_surface, (207, 448))


class Task:
    tasks = []
    taskName = []
    completedTasks = []
    lastIndex = 0
    def __init__(self, name, description, type):
        self.name = name
        self.description = description
        self.type = type
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
    def __init__(self, name, frequency, description, type):
        super().__init__(name, description, type)
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
    def __init__(self, name, duration, description, type):
        super().__init__(name, description, type)
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

pp = Project("pp1", 10, "ahfuwuwf", "Work")
dih = Project("pp2", 10, "fwhifwi", "School")





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



def make(type=None):
    #Make user input stuff (MARCUS)

    task = None
    if type == "Project": 
        task = Project("project", 5, "description", "Sport") 

    elif type == "Routine": 
        task = Routine("routine", 5, "description", "Sport")



## UI SETUP
add_project_button = Button("placeholder.png", 100, 750, priority=2)
complete_project_button = Button("placeholder.png", 250, 750, priority=2, tint=(255,0,0))
add_routine_button = Button("placeholder.png", 100, 750, priority=2)
complete_routine_button = Button("placeholder.png", 250, 750, priority=2, tint=(255,0,0))

add_project_button.set_function(make, params="Project")
add_routine_button.set_function(make, params="Routine")


add = Button("Buttons/add_button.png", 30, 30, BUTTON_BASE_COLORS)
view_routines = Button("Buttons/list_button.png", 80, 30, BUTTON_BASE_COLORS)
view_projects = Button("Buttons/list_button.png", 130, 30, BUTTON_BASE_COLORS)

menu = PopUp(
    base=RectSprite((30,30,30,180),SCREEN_WIDTH, SCREEN_HEIGHT, 0, 0),
    items=[
        Button("Buttons/cancel_button.png", 50, 50, BUTTON_BASE_COLORS, priority=10, tab="menu"),
        add_routine_button, complete_routine_button
    ],
    hide_buttons=[add, view_routines, view_projects],
    set_tab="menu",
    priority = 9
)
pmenu = PopUp(
    base=RectSprite((30,30,30,180),SCREEN_WIDTH, SCREEN_HEIGHT, 0, 0),
    items=[
        Button("Buttons/cancel_button.png", 50, 50, BUTTON_BASE_COLORS, priority=10, tab="pmenu"),
        add_project_button, complete_project_button
    ],
    hide_buttons=[add, view_routines, view_projects],
    set_tab="pmenu",
    priority = 9
)
amenu = PopUp(
    base=RectSprite((30,30,30,180),SCREEN_WIDTH, SCREEN_HEIGHT, 0, 0),
    items=[
        Button("Buttons/cancel_button.png", 50, 50, BUTTON_BASE_COLORS, priority=10, tab="amenu"),
        add_project_button, complete_project_button
    ],
    hide_buttons=[add, view_routines, view_projects],
    set_tab="amenu",
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
        deselect_task_in_menu()
    elif name == "pmenu": 
        pmenu.set_active(True)
        deselect_task_in_menu()
    elif name == "amenu":
        amenu.set_active(True)
        deselect_task_in_menu()
    set_tab(name)
def hide_menus(): 
    menu.set_active(False)
    pmenu.set_active(False)
    amenu.set_active(False)
    set_tab("main")
def show_info_for_task(task =None):
    if not task: 
        display_text("No task selected", description_font, (80, 650))
        return


    name = task.name
    description = task.description
    type = task.type
    if isinstance(task, Routine):  # if the task is a routine
        t = task.frequency
    else: # if the task is a project
        t = task.duration

    
    tab = get_tab()

    display_text(name, description_font, (80, 650))
    display_text(f"Type: {type}", description_font, (80, 680))
    if tab == "pmenu":
        display_text(f"Duration: {t}", description_font, (80, 710))
    else:
        display_text(f"Frequency: {t}", description_font, (80, 710))
    display_text(f"Description: {description}", description_font, (80, 740))
def height_to_task(height, array):
    if len(array) == 0 or height == None: return None
    i = int((height-220)/50)
    return array[i]

# BUTTON SETUP
menu.items[1].set_function(hide_menus)
pmenu.items[1].set_function(hide_menus)
amenu.items[1].set_function(hide_menus)
view_projects.set_function(switch_to_menu, "pmenu")
view_routines.set_function(switch_to_menu, "menu")
add.set_function(switch_to_menu, "amenu")

### MAIN GAME LOOP
dragging = False
button_down_time = 0
click_threshold = 0.3
drag_base = (0,0) # for dragging

running = True
tab = get_tab()

background_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
draw_gradient(background_surface, (0,23,45), (0,0,0))

task_selected = None
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
                clip_rect=pygame.Rect(80, 220, SCREEN_WIDTH - 160, 400), selectable=True
            )
            text = ""
            display_text(
                text, main_font,
                (80, 170 + 50 * (i + 1)),
                scrollable = True,
                clip_rect=pygame.Rect(80, 220, SCREEN_WIDTH - 160, 400), selectable=True
            )

        task : Routine = height_to_task(get_selected_task_height(), Routine.routines)
        show_info_for_task(task)
    elif current_tab == "pmenu":
        Tile.deselect_tiles()
        tile_data_tab.set_active(False)

        text = ""
        display_text("Projects", title_font, (80, 110))
        for i in range(len(Project.projectNames)):
            text = f"{Project.projectNames[i]}" 
            display_text(
                text, main_font,
                (80, 170 + 50*(i+1)),
                scrollable = True,
                clip_rect=pygame.Rect(80, 220, SCREEN_WIDTH - 160, 400), selectable=True
            )
            text = ""
            display_text(
                text, main_font,
                (80, 170 + 50 * (i + 1)),
                scrollable = True,
                clip_rect=pygame.Rect(80, 220, SCREEN_WIDTH - 160, 400), selectable=True
            )

        task : Project = height_to_task(get_selected_task_height(), Project.projects)
        show_info_for_task(task)
    elif current_tab == "amenu":
        Tile.deselect_tiles()
        tile_data_tab.set_active(False)

        text = ""
        display_text("Add task", title_font, (80, 110))
        for i in range(len(Task.taskName)):
            text = f"{Task.taskName[i]}"
            display_text(
                text, main_font,
                (80, 170 + 50*(i+1)),
                scrollable = True,
                clip_rect=pygame.Rect(80, 220, SCREEN_WIDTH - 160, 400), selectable=True
            )
            text = ""
            display_text(
                text, main_font,
                (80, 170 + 50 * (i + 1)),
                scrollable = True,
                clip_rect=pygame.Rect(80, 220, SCREEN_WIDTH - 160, 400), selectable=True
            )

        task : Project = height_to_task(get_selected_task_height(), Project.projects)
        show_info_for_task(task)
    if Tile.selected != None:
        tile_data_tab.set_active(True)
        display_text("Empty tile", main_font, (30, SCREEN_HEIGHT-250))
    else:
        tile_data_tab.set_active(False)
    

    pygame.display.flip()
    update_projects(Project.projects)

pygame.quit()