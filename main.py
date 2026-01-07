import pygame
import random
import math
import time

from pygame_objs import *

pygame.init()
pygame.display.set_caption("VOYAGE")

class Task:
    tasks = []
    completedTasks = []
    lastIndex = 0
    def __init__(self, name):
        self.name = name
        self.index = Task.lastIndex
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
    def __init__(self, name, frequency):
        super().__init__(name)

class Project(Task):
    def __init__(self, name, duration):
        super().__init__(name)

# test
Task.printTasks()
task = Task("task")
task2 = Task("task2")
task3= Task("task3")
Task.printTasks()
task2.complete()
Task.printTasks()

### SPRITES AND OTHER VARIABLES

sprite = RectSprite((255,255,255), 100, 100, 0, 0, priority=1)
img = ImageSprite("placeholder.png", 300, 300, (255,0,0,100))
# button = Button((200,200,200), 100, 50, 200, 100)
button = Button("placeholder.png", 150, 150, priority=1)

center_tile = Tile(color=(255,255,255))
# tile1 = Tile(0, 1)
# tile2 = Tile(0, -1)
# tile3 = Tile(1, 0)
# tile4 = Tile(-1, 0)

def addTile():
    x,y = Tile.get_random_placement() 
    Tile(x,y)
for _ in range(5): addTile()

button.set_function(addTile)

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
    pygame.display.flip()

pygame.quit()