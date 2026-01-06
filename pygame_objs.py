import pygame 

screen = pygame.display.set_mode((414, 896))

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
    def __init__(self, path, x=0, y=0):
        super().__init__(0, 0, x, y)
        try:
            self.img = pygame.image.load(f"Assets/{path}").convert_alpha()
        except pygame.error as e: 
            self.img = pygame.image.load(f"Assets/placeholder.png").convert_alpha()
        self.rect = self.img.get_rect(center=(x,y))  
    def display(self):
        screen.blit(self.img, self.rect)

class RectSprite(Sprite):
    def __init__(self, fill, w, l, x=0, y=0):
        super().__init__(w, l, x, y)
        self.fill = fill
    def display(self):
        pygame.draw.rect(screen, self.fill, self.rect)