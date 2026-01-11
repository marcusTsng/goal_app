import pygame
import random
import math
import time
from pygame_objs import *
pygame.init()
pygame.display.set_caption("VOYAGE")
title_font = pygame.font.SysFont('arialrounded', 60)
main_font = pygame.font.SysFont('arialrounded', 30)
# description_font = pygame.font.SysFont('arialrounded', 15)
description_font = pygame.font.Font("Assets/Fonts/saxmono.ttf", 15)
points_font = pygame.font.Font("Assets/Fonts/saxmono.ttf", 30)

menu_clip_rect = pygame.Rect(80, 220, SCREEN_WIDTH - 160, 400)

# pygame.init()
# fonts = pygame.font.get_fonts()
# print(f"Total fonts available on this system: {len(fonts)}\n")
# print("List of available fonts:")
# for f in fonts:
#     print(f"* {f}")

points = 0
def savePoints():
    global points
    try:
        with open("points.txt", "w") as f:
            f.write(str(points))
    except Exception as e:
        print("Error retrieving points from database:", e)
def getPoints():
    global points
    try:
        with open("points.txt", "r") as f:
            data = f.read().strip()
            print(data)
            if data == "" or data == "None":
                points = 0
            else:
                points = int(data)
    except Exception as e:
        points = 0
        print("Error saving points to database:", e)

getPoints()

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
    def delete(self): 
        # LIAM
        # complete this
        del self

    @staticmethod
    def printTasks():
        print("---")
        for t in Task.tasks: print(t.name)

class Routine(Task):
    routines = []
    routineNames = []
    completedRoutines = []
    frequencies = []
    routineDescs = []
    lastIndexR = 0
    def __init__(self, name, frequency, description, type):
        super().__init__(name, description, type)
        self.name = name
        self.frequency = frequency
        self.index = Routine.lastIndexR
        Routine.routineDescs.append(self.description)
        Routine.frequencies.append(self.frequency)
        Routine.routineNames.append(self.name)
        Routine.routines.append(self)
        Routine.lastIndexR += 1
    def completeR(self):
        Routine.completedRoutines.append(self)
        Routine.routines.pop(self.index)
    @staticmethod
    def update_names():
        Routine.routineNames = []
        for x in Routine.routines: 
            Routine.routineNames.append(x.name)


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
        # LIAM
        # DEBUG THIS
        print("fat monkey bitch")
        Project.completedProjects.append(self)
        print(self.index)
        Project.projects.pop(self.index)
        addTile()
    @staticmethod
    def update_names():
        Project.projectNames = []
        for x in Project.projects: 
            Project.projectNames.append(x.name)

# pp = Project("pp1", 10, "ahfuwuwf", "Work")
# dih = Routine("pp2", 10, "fwhifwi", "School")





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

def routine_DS():
    timings = open("Routine timings", "a")
    timings.write(str(time.time()) + "\\n")
    timings.close()
    frequencies = open("Routine frequencies", "a")
    Routine.frequencies[-1] = str(Routine.frequencies[-1])
    frequencies.write(Routine.frequencies[-1] + "\\n")
    Routine.frequencies[-1] = float(Routine.frequencies[-1])
    frequencies.close()
    names = open("Routines", "a")
    names.write(Routine.routineNames[-1])
    names.close()
    descriptions = open("Routine descriptions", "a")
    descriptions.write(Routine.routineDescs[-1])
    descriptions.close()


def make(type=None):
    #Make user input stuff (MARCUS)

    task = None
    if type == "Project": 
        task = Project("New Project", 0, "Enter a description here", "Sport") 
        select_from_index(len(Project.projects) - 1, task.name)


    elif type == "Routine": 
        task = Routine("New Routine", 10000000000000000, "Enter a description here", "Sport")
        select_from_index(len(Routine.routines) - 1, task.name)
        routine_DS()

add_names = open("Routines", "r")
name_list = add_names.readlines()
add_frequencies = open("Routine frequencies", "r")
frequency_list = add_frequencies.readlines()
add_descriptions = open("Routine descriptions", "r")
description_list = add_descriptions.readlines()

for i in range(len(name_list)):
    task = Routine(name_list[i], frequency_list[i], description_list[i], "sport")


## UI SETUP
star_icon = ImageSprite("Buttons/Icons/star.png", SCREEN_WIDTH - 100, 35, (255,255,255))

add_project_button = Button("Buttons/add_button.png", 100, 750, priority=2, clip_rect=menu_clip_rect)
complete_project_button = Button("Buttons/complete_button.png", 100, 790, priority=12, tint=(0,255,0), tab="pmenu")
delete_project_button = Button("Buttons/trash_button.png", 150, 790, priority=12, tint=(255,0,0), tab="pmenu")
delete_routine_button = Button("Buttons/trash_button.png", 100, 790, priority=12, tint=(255,0,0), tab="menu")
add_routine_button = Button("Buttons/add_button.png", 100, 750, priority=2, clip_rect=menu_clip_rect)
complete_routine_button = Button("placeholder.png", 100, 150, tint=(0,255,0))
cancel_routine_button = Button("placeholder.png", 200, 150, tint=(255,0,0))

complete_project_button.set_active(False)
delete_project_button.set_active(False)
delete_routine_button.set_active(False)

name_text_box = Textbox(80,650,300,30, font= description_font, default_text="Title")
description_text_box = Textbox(80,680,300,30, font= description_font, default_text="Description")
time_text_box = Textbox(80,710,300,30, font= description_font, default_text="Frequency/Duration in days")
info_text_boxes=[name_text_box, description_text_box, time_text_box]

add_project_button.set_function(make, params="Project")
add_routine_button.set_function(make, params="Routine")

view_routines = Button("Buttons/Icons/routines_tab.png", 30, 30, BUTTON_BASE_COLORS)
view_projects = Button("Buttons/Icons/projects_tab.png", 80, 30, BUTTON_BASE_COLORS)

menu = PopUp(
    base=RectSprite((30,30,30,180),SCREEN_WIDTH, SCREEN_HEIGHT, 0, 0),
    items=[
        Button("Buttons/cancel_button.png", 50, 50, BUTTON_BASE_COLORS, priority=10, tab="menu"),
        add_routine_button, name_text_box, description_text_box
    ],
    hide_buttons=[view_routines, view_projects,star_icon],
    set_tab="menu",
    priority = 9
)
pmenu = PopUp(
    base=RectSprite((30,30,30,180),SCREEN_WIDTH, SCREEN_HEIGHT, 0, 0),
    items=[
        Button("Buttons/cancel_button.png", 50, 50, BUTTON_BASE_COLORS, priority=10, tab="pmenu"),
        add_project_button, name_text_box, description_text_box
    ],
    hide_buttons=[view_routines, view_projects,star_icon],
    set_tab="pmenu",
    priority = 9
)
amenu = PopUp(
    base=RectSprite((30,30,30,180),SCREEN_WIDTH, SCREEN_HEIGHT, 0, 0),
    items=[
        Button("Buttons/cancel_button.png", 50, 50, BUTTON_BASE_COLORS, priority=10, tab="amenu"),
    ],
    hide_buttons=[view_routines, view_projects],
    set_tab="amenu",
    priority = 9
)

rmenu = PopUp(
    base=RectSprite((30,30,30,245), 300, 200, (SCREEN_WIDTH - 300) / 2, (SCREEN_HEIGHT - 200) / 2),
    items=[complete_routine_button, cancel_routine_button],
    hide_buttons=[view_routines, view_projects, star_icon],
    set_tab="rmenu", 
    priority = 9
)

tile_data_tab = PopUp(
    base=RectSprite((30,30,30,180), SCREEN_WIDTH, 300, 0, SCREEN_HEIGHT-300),
    items=[],
    priority=8
)

def switch_to_menu(name):
    deselect_task_in_menu()
    if name == "menu":
        menu.set_active(True)
    elif name == "pmenu": 
        pmenu.set_active(True)
    elif name == "amenu":
        amenu.set_active(True)
    elif name == "rmenu":
        rmenu.set_active(True)
    set_tab(name)
def hide_menus(): 
    menu.set_active(False)
    pmenu.set_active(False)
    amenu.set_active(False)
    set_tab("main")

completed_routine_prompted = None
routine_queue = []
def prompt_rmenu(routine : Routine):
    global completed_routine_prompted, routine_queue
    tab = get_tab()

    if not routine in routine_queue: 
        routine_queue.append(routine)

    name = routine_queue[0].name 
    if tab != "rmenu":
        completed_routine_prompted = None
        if tab != "main": hide_menus()
        else:
            switch_to_menu("rmenu")
    else:
        r_name = name[:-1] if len(name) < 16 else f"{name[0:13]}..."
        prompt = f"Have you completed {r_name}?"
        x_pos = 70 if len(name) >= 16 else SCREEN_WIDTH/2 - (len(prompt)/2 * 8)
        display_text("ROUTINE CHECK", main_font, (80,SCREEN_HEIGHT/2 - 80))
        display_text(prompt, description_font, (x_pos,SCREEN_HEIGHT/2 - 20))

        if completed_routine_prompted != None: 
            routine_queue.remove(routine_queue[0])
            switch_to_menu("main")
            return completed_routine_prompted
def pick_routine_option(bool):
    print("PICK")
    global completed_routine_prompted
    completed_routine_prompted = bool

last_task = None
def find_in_array(arr, x):
    for i in range(len(arr)):
        if x == arr[i]: return i
def show_info_for_task(task =None):
    global last_task
    if not task: 
        display_text("No task selected", description_font, (80, 650))
        complete_project_button.set_active(False)
        delete_project_button.set_active(False)
        delete_routine_button.set_active(False)

        for x in info_text_boxes: x.set_active(False)
        return

    name = task.name
    description = task.description

    if task != last_task:
        last_task = task
        name_text_box.text = name
        description_text_box.text = description
        if isinstance(task, Routine):
            time_text_box.text = str(task.frequency)
            delete_routine_button.set_active(True)
            delete_routine_button.set_function(task.delete())
            x = task.index
            frequencies = open("Routine frequencies", "r+")
            frequen_list = frequencies.readlines()
            print(frequen_list)
            names = open("Routines", "r+")
            name_list = names.readlines()
            descriptions = open("Routine descriptions", "r+")
            desc_list = descriptions.readlines()
            frequen_list[x] = task.frequency
            name_list[x] = task.name
            desc_list[x] = task.description
            frequencies.seek(0)
            frequencies.truncate()
            names.seek(0)
            names.truncate()
            descriptions.seek(0)
            descriptions.truncate()
            for i in range(len(frequen_list)):
                frequen_list[i] = str(frequen_list[i])
            frequencies.writelines(frequen_list)
            names.writelines(name_list)
            descriptions.writelines(desc_list)
            frequencies.close()
            names.close()
            descriptions.close()
        else: 
            complete_project_button.set_active(True)
            delete_project_button.set_active(True)
            complete_project_button.set_function(task.completeP)
            delete_project_button.set_function(task.delete)
            time_text_box.text = str(task.duration)
    for x in info_text_boxes: x.set_active()

    task.name = name_text_box.text
    task.description = description_text_box.text
    if isinstance(task, Routine):
        f = time_text_box.text.strip()
        if f == "": f = 0
        else: f = int(f)

        task.frequency = f
        Routine.frequencies[find_in_array(Routine.routines, task)] = f
<<<<<<< Updated upstream
<<<<<<< Updated upstream
=======
        task.frequency = time_text_box.text
        Routine.frequencies[find_in_array(Routine.routines, task)] = task.frequency
>>>>>>> Stashed changes
=======
        task.frequency = time_text_box.text
        Routine.frequencies[find_in_array(Routine.routines, task)] = task.frequency
>>>>>>> Stashed changes
    else: 
        task.duration = time_text_box.text

    # display_text(name, description_font, (80, 650))
    # display_text(f"Type: {type}", description_font, (80, 680))
    # if tab == "pmenu":
    #     display_text(f"Duration: {t}", description_font, (80, 710))
    # else:
    #     display_text(f"Frequency: {t}", description_font, (80, 710))
    # display_text(f"Description: {description}", description_font, (80, 740))
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
complete_routine_button.set_function(func=pick_routine_option, params=True)
cancel_routine_button.set_function(func=pick_routine_option, params=False)
# add.set_function(switch_to_menu, "amenu")

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
            savePoints()
        if event.type == pygame.MOUSEBUTTONDOWN:
            button_down_time = time.time()
            dragging = True
            drag_base = mouse_pos
        if event.type == pygame.MOUSEBUTTONUP:
            if time.time() - button_down_time < click_threshold: 
                Button.check_all_hovers()
                Textbox.check_click(mouse_pos)
            dragging = False
        
        if event.type == pygame.MOUSEWHEEL and (current_tab == "menu" or current_tab == "pmenu"):
            menu_scroll(event.y * 10)

        for tb in Textbox.textboxes:
            if tb.active: tb.handle_event(event)
    
    if dragging and time.time() - button_down_time > click_threshold: 
        dx = mouse_pos[0] - drag_base[0]
        dy = mouse_pos[1] - drag_base[1]
        
        if current_tab == "main":
            new_offset = (SCREEN_OFFSET[0] + dx, SCREEN_OFFSET[1] + dy)
            SCREEN_OFFSET = new_offset
            set_screen_offset(new_offset)
        elif current_tab == "menu" or current_tab == "pmenu":
            menu_scroll(dy)

        drag_base = mouse_pos
    
    screen.blit(background_surface, (0, 0))
    # screen.fill(BG_COLOUR)
    Sprite.displaySprites()
    Textbox.update_all()

    if current_tab == "menu":
        update_projects(Routine.routines)
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
                clip_rect=menu_clip_rect, selectable=True
            )
            text = ""
            display_text(
                text, main_font,
                (80, 170 + 50 * (i + 1)),
                scrollable = True,
                clip_rect=menu_clip_rect, selectable=True
            )

        task : Routine = height_to_task(get_selected_task_height(), Routine.routines)
        x, y = add_routine_button.get_pos()
        add_routine_button.set_pos(x, len(Routine.routineNames) * 50 + 240 + get_scroll_offset())
        show_info_for_task(task)
    elif current_tab == "pmenu":
        update_projects(Project.projects)
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
                clip_rect=menu_clip_rect, selectable=True
            )
            text = ""
            display_text(
                text, main_font,
                (80, 170 + 50 * (i + 1)),
                scrollable = True,
                clip_rect=menu_clip_rect, selectable=True
            )

        task : Project = height_to_task(get_selected_task_height(), Project.projects)
        x, y = add_project_button.get_pos()
        add_project_button.set_pos(x, len(Project.projectNames) * 50 + 240 + get_scroll_offset())
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
                clip_rect=menu_clip_rect, selectable=True
            )
            text = ""
            display_text(
                text, main_font,
                (80, 170 + 50 * (i + 1)),
                scrollable = True,
                clip_rect=menu_clip_rect, selectable=True
            )

        task : Project = height_to_task(get_selected_task_height(), Project.projects)
        x, y = add_project_button.get_pos()
        add_routine_button.set_pos(x, len(Project.projectNames) * 50 + 240 + get_scroll_offset())
        show_info_for_task(task)
    if Tile.selected != None:
        tile_data_tab.set_active(True)
        display_text("Empty tile", main_font, (30, SCREEN_HEIGHT-250))
    else:
        tile_data_tab.set_active(False)
    check_time = open("Routine timings", "r")
    check_frequency = open("Routine frequencies")
    frequency_list = check_frequency.readlines()
    time_list = check_time.readlines()
    # if time_list[-1] == "":
    #     time_list.pop(-1)
    # if frequency_list[-1] == "":
    #     frequency_list.pop(-1)
    for i in range(len(time_list)):
        time_list[i] = float(time_list[i])
        frequency_list[i] = float(frequency_list[i])
        # print(time.time())
        # print(time_list[i] + 5 * Routine.frequencies[i])
        # print(time_list[i] + 5)
        # print(Routine.frequencies[i])

        if time.time() >= time_list[i] + frequency_list[i] and i <= len(Routine.routines) - 1:
            # LIAM

            completed = prompt_rmenu(Routine.routines[i])

            if completed != None: 
                
                if completed: print("Routine has been completed")
                else: print("Routine was not completed")

                time_list[i] = time.time()
                check_time.truncate()
                check_time.writelines(time_list)
    if current_tab == "main":
        display_text(str(points), points_font, (SCREEN_WIDTH-75, 25))

        complete_project_button.set_active(False)
        delete_project_button.set_active(False)
        delete_routine_button.set_active(False)

        for x in info_text_boxes: x.set_active(False)

    pygame.display.flip()
    Project.update_names()
    Routine.update_names()

pygame.quit()