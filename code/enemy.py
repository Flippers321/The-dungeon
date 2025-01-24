from settings import *
from timer import Timer

class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos, groups, collision_sprites, health, frames):
        super().__init__(groups)
        self.z = Z_LAYERS['entity']

        self.frames, self.frame_index = frames, 0
        self.image = self.frames['idle'][self.frame_index]

        self.jumps = 1

        #TODO -- set an entity class to inherit 
