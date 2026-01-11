import pygame
import time
import json
from pygame_objs import *
pygame.init()
pygame.display.set_caption("CONQUEST")
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

tile_tab_showing = False

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
        del self

    @staticmethod
    def printTasks():
        print("---")
        for t in Task.tasks: print(t.name)

class Routine(Task):
    routines = []
    routineNames = []
    completedRoutines = []
    deletedRoutines = []
    lastIndexR = 0
    def __init__(self, name, frequency, description, type):
        super().__init__(name, description, type)
        self.name = name
        self.frequency = frequency
        self.time = time.time()
        self.index = Routine.lastIndexR
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
    def delete(self):
        Routine.deletedRoutines.append(self)
        Routine.routines.remove(self)
        deselect_task_in_menu()

    def to_dict(self):
        """Convert this Project to a JSON-serializable dictionary"""
        return {
            "name": self.name,
            "frequency": self.frequency,
            "time": self.time,
            "description": self.description,
            "type": self.type,               # assuming Task has this attribute
            "index": self.index,
            # Add any other important Task/Project attributes here
            # e.g. "status": self.status if exists
            # "created": self.created.isoformat() if you have datetime
        }

    @classmethod
    def from_dict(cls, data):
        """Reconstruct a Project from a dictionary (used when loading)"""
        # Create new instance
        project = cls(
            name=data["name"],
            frequency=data["frequency"],
            time=data["time"],
            description=data["description"],
            type=data["type"]
        )

        # Restore extra fields (index is important!)
        project.index = data.get("index", 0)

        return project


class Project(Task):
    projects = []
    projectNames = []
    completedProjects = []
    deletedProjects = []
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
        Project.completedProjects.append(self)
        Project.projects.remove(self)
        deselect_task_in_menu()
        addTile()
    def delete(self):
        Project.deletedProjects.append(self)
        Project.projects.remove(self)
        deselect_task_in_menu()
    @staticmethod
    def update_names():
        Project.projectNames = []
        for x in Project.projects: 
            Project.projectNames.append(x.name)

    def to_dict(self):
        """Convert this Project to a JSON-serializable dictionary"""
        return {
            "name": self.name,
            "duration": self.duration,
            "description": self.description,
            "type": self.type,               # assuming Task has this attribute
            "index": self.index,
            # Add any other important Task/Project attributes here
            # e.g. "status": self.status if exists
            # "created": self.created.isoformat() if you have datetime
        }

    @classmethod
    def from_dict(cls, data):
        """Reconstruct a Project from a dictionary (used when loading)"""
        # Create new instance
        project = cls(
            name=data["name"],
            duration=data["duration"],
            description=data["description"],
            type=data["type"]
        )

        # Restore extra fields (index is important!)
        project.index = data.get("index", 0)

        return project

### SPRITES AND OTHER VARIABLES
center_tile = Tile(color=(255,255,255))
center_tile.set_building("Hut")
center_tile.add_floor()

# datasave functions
def project_DS():
    data = []
    for project in Project.projects:
        data.append(project.to_dict())

    try:
        with open("Datasave/Projects.json", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print("Projects successfully saved to Projects.json")
    except Exception as e:
        print(f"Error saving projects: {e}")

def load_projects_DS():
    try:
        with open("Datasave/Projects.json", "r", encoding="utf-8") as f:
            data = json.load(f)

        for project in data:
            Project(project["name"], project["duration"], project["description"], "")

        print(f"Loaded projects successfully")
    except Exception as e:
        print(f"Error loading projects: {e}")
        return False

def routine_DS():
    data = []
    for project in Routine.routines:
        data.append(project.to_dict())

    try:
        with open("Datasave/Routines.json", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print("Projects successfully saved to Projects.json")
    except Exception as e:
        print(f"Error saving projects: {e}")

def load_routine_DS():
    try:
        with open("Datasave/Routines.json", "r", encoding="utf-8") as f:
            data = json.load(f)

        for routine in data:
            Routine(routine["name"], routine["frequency"], routine["description"], "")

        print(f"Loaded projects successfully")
    except Exception as e:
        print(f"Error loading routines: {e}")
        return False

def tiles_DS():
    data = []
    for tile in Tile.tiles:
        data.append(tile.to_dict())

    try:
        with open("Datasave/Tiles.json", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print("Tiles successfully saved to Projects.json")
    except Exception as e:
        print(f"Error saving projects: {e}")

def load_tiles_DS():
    try:
        with open("Datasave/Tiles.json", "r", encoding="utf-8") as f:
            data = json.load(f)

        Tile.tiles.clear()           # Clear old tiles to prevent duplication
        Tile.center_tile = None
        Tile.lastIndexP = 0          # if you ever add index to tiles

        for tile_data in data:
            # Create tile WITHOUT structure first
            tile = Tile(
                relative_x=tile_data["relative_x"],
                relative_y=tile_data["relative_y"],
                color=TILE_COL,
                priority=1
            )

            # If there's saved structure data → recreate it AFTER tile exists
            if tile_data.get("structure"):
                struct_data = tile_data["structure"]
                struct_type = Structure.types[struct_data["type_name"]]
                structure = Structure(tile, struct_type)  # ← pass the tile!
                structure.level = struct_data["level"]
                structure.points_needed = struct_data["points_needed"]
                structure.upgrade_time = struct_data["upgrade_time"]
                tile.structure = structure

                # Recreate floors (basic version – assumes only bottom image for now)
                # For full floors you'd need to save list of floor levels/paths
                for level in range(2, structure.level + 1):
                    path = struct_type["top"] if level == structure.level else struct_type["mid"]
                    Floor(tile.get_pos(), level, struct_type["level_height"], struct_type["bottom_level_height"], path)

        print(f"Loaded {len(Tile.tiles)} tiles successfully")
    except FileNotFoundError:
        print("No Tiles.json found – starting fresh")
    except Exception as e:
        print(f"Error loading tiles: {e}")

def make(type=None):
    task = None
    if type == "Project": 
        task = Project("New Project", 0, "Enter a description here", "Sport") 
        select_from_index(len(Project.projects) - 1, task.name)


    elif type == "Routine": 
        task = Routine("New Routine", 10000000000000000, "Enter a description here", "Sport")
        select_from_index(len(Routine.routines) - 1, task.name)


## UI SETUP
star_icon = ImageSprite("Buttons/Icons/star.png", SCREEN_WIDTH - 100, 35, (255,255,255))

add_project_button = Button("Buttons/add_button.png", 100, 750, priority=2, clip_rect=menu_clip_rect)
complete_project_button = Button("Buttons/complete_button.png", 100, 790, priority=12, tint=(0,255,0), tab="pmenu")
delete_project_button = Button("Buttons/trash_button.png", 150, 790, priority=12, tint=(255,0,0), tab="pmenu")
delete_routine_button = Button("Buttons/trash_button.png", 100, 790, priority=12, tint=(255,0,0), tab="menu")
add_routine_button = Button("Buttons/add_button.png", 100, 750, priority=2, clip_rect=menu_clip_rect)
complete_routine_button = Button("placeholder.png", 100, 150, tint=(0,255,0))
cancel_routine_button = Button("placeholder.png", 200, 150, tint=(255,0,0))

building_button = Button("placeholder.png", 70, 150, priority=12, tint=(255,0,0))
upgrade_button = Button("placeholder.png", 70, 150, priority=12, tint=(0,255,0))

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
    items=[building_button,upgrade_button],
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
    rmenu.set_active(False)
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
            hide_menus()
            switch_to_menu("main")
            return completed_routine_prompted
def pick_routine_option(bool):
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
            delete_routine_button.set_function(task.delete)
            x = task.index
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

load_projects_DS()
load_routine_DS()
load_tiles_DS()
if len(Tile.tiles) == 0:
    for _ in range(5): addTile()

while running:
    mouse_pos = pygame.mouse.get_pos()
    current_tab = get_tab()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            savePoints()
            project_DS()
            routine_DS()
            tiles_DS()
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
        tile_tab_showing = False

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
        tile_tab_showing = False

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
        tile_tab_showing = False

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
        if not tile_tab_showing:
            tile_tab_showing = True
            tile_data_tab.set_active(True)
        tile = Tile.selected

        text = "Empty tile"
        if tile.structure == None:
            building_button.set_active(True)
            upgrade_button.set_active(False)
            # building_button = Button("placeholder.png", 60, SCREEN_HEIGHT-150, priority=12, tint=(255,255,255))
        else:
            text = f"{tile.structure.name}, Level {tile.structure.level}"
            building_button.set_active(False)
            upgrade_button.set_active(True)
            # building_button = Button("placeholder.png", 60, SCREEN_HEIGHT-150, priority=12, tint=(255,255,255))
        points_needed = tile.get_points_needed()
    
        def build():
            global points
            if points > points_needed:
                if (tile.structure != None and time.time() - tile.structure.upgrade_time > 0.5) or tile.structure == None:
                    points -= points_needed      
                    Tile.build_structure(tile)
            else: print("Not enough points")

        building_button.set_function(build)
        display_text(text, main_font, (30, SCREEN_HEIGHT-250))
    else:
        tile_tab_showing = False
        tile_data_tab.set_active(False)
    # if time_list[-1] == "":
    #     time_list.pop(-1)
    # if frequency_list[-1] == "":
    #     frequency_list.pop(-1)

    for r in Routine.routines:
        t = r.time
        f = r.frequency * 86400
        if f == 0: f = 86400
        
        if time.time() >= t + f:
            completed = prompt_rmenu(r)

            if completed != None: 
                
                if completed:
                    points += 10
                    print("Routine has been completed")
                else: print("Routine was not completed")

                r.time = time.time()
    if current_tab == "main":
        display_text(str(points), points_font, (SCREEN_WIDTH-75, 25))

        complete_project_button.set_active(False)
        delete_project_button.set_active(False)
        delete_routine_button.set_active(False)

        for x in info_text_boxes: x.set_active(False)

    if building_button != None and not Tile.selected:
        building_button.set_active(False)

    pygame.display.flip()
    Project.update_names()
    Routine.update_names()

pygame.quit()