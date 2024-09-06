from settings import *

class Sprite(pygame.sprite.Sprite):
    def __init__(self, pos, surf = pygame.Surface((16,16)), groups = None):
        super().__init__(groups) #adding sprite to group/s
        self.image = surf
        if self.image == None:
            self.image = pygame.Surface((16,16))
            self.image.fill('white')
        self.rect = self.image.get_frect(topleft = pos)
        self.old_rect = self.rect.copy() #gets position of sprites a frame before
    