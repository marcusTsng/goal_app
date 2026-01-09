import pygame
import random
import math
import time

from pygame_objs import *

pygame.init()
pygame.display.set_caption("VOYAGE")
my_font = pygame.font.SysFont('Comic Sans MS', 30)




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
    completedRoutines = []
    lastIndexR = 0
    def __init__(self, name, frequency):
        super().__init__(name)
        self.name = name
        self.frequency = frequency
        self.index = Routine.lastIndexR
        Routine.routines.append(self)
        Routine.lastIndexR += 1
    def completeR(self):
        Routine.completedRoutines.append(self)
        Routine.routines.pop(self.index)


class Project(Task):
    projects = []
    completedProjects = []
    lastIndexP = 0
    def __init__(self, name, duration):
        super().__init__(name)
        self.name = name
        self.duration = duration
        self.index = Project.lastIndexP
        Project.projects.append(self)
        Project.lastIndexP += 1
    def completeP(self):
        Project.completedProjects.append(self)
        Project.projects.pop(self.index)
        addTile()

pp = Project("pp", 10)
dih = Project("dih", 10)





# test
# Task.printTasks()
# task = Task("task")
# task2 = Task("task2")
# task3= Task("task3")
# Task.printTasks()
# task2.complete()
# Task.printTasks()

### SPRITES AND OTHER VARIABLES

add_button = Button("placeholder.png", 150, 150, priority=2)
complete_button = Button("placeholder.png", 300, 150, priority=2, tint=(255,0,0))

center_tile = Tile(color=(255,255,255))
center_tile.set_building("Hut")
center_tile.add_floor()
# tile1 = Tile(0, 1)
# tile2 = Tile(0, -1)
# tile3 = Tile(1, 0)
# tile4 = Tile(-1, 0)

def make():
    test = Project("pp", 10)
    complete_button.set_function(test.completeP)
add_button.set_function(make)


# FUNCTIONS
def add_task(): pass 
def view_tasks(): pass 


## UI SETUP
add = Button("Buttons/add_button.png", 30, 30, BUTTON_BASE_COLORS, add_task)
view = Button("Buttons/list_button.png", 80, 30, BUTTON_BASE_COLORS, view_tasks)

pop_up = PopUp(
    items=[
        Button("placeholder.png", 5, 5, BUTTON_BASE_COLORS, priority=10)
    ],
    hide_buttons=[add, view]
)
pop_up.items[1].set_function(pop_up.toggle_active)
view.set_function(pop_up.toggle_active)
add.set_function(add_task)

### MAIN GAME LOOP
dragging = False
button_down_time = 0
click_threshold = 0.2
drag_base = (0,0) # for dragging

running = True
while running:

    mouse_pos = pygame.mouse.get_pos()

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
    
    
    if dragging and time.time() - button_down_time > click_threshold: 
        dx = mouse_pos[0] - drag_base[0]
        dy = mouse_pos[1] - drag_base[1]
        
        new_offset = (SCREEN_OFFSET[0] + dx, SCREEN_OFFSET[1] + dy)
        
        SCREEN_OFFSET = new_offset
        set_screen_offset(new_offset)

        drag_base = mouse_pos
    
    screen.fill(BG_COLOUR)
    Sprite.displaySprites()
    for i in range(len(Task.taskName)):
        text = Task.taskName[i] + 
        text_surface = my_font.render(text, False, (255, 255, 255))
        screen.blit(text_surface, (207, 50*(i+1)))
    pygame.display.flip()

pygame.quit()