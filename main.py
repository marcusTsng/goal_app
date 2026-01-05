import pygame
import random
import math

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
BG_COLOUR = (0,0,0)
sprite = Sprite("placeholder.png", 100, 200)

### MAIN GAME LOOP
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(BG_COLOUR)
    Sprite.displaySprites()

    pygame.display.flip()
pygame.quit()