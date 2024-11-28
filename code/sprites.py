from settings import *

class Sprite(pygame.sprite.Sprite):
    def __init__(self, pos, surf = pygame.Surface((16,16)), groups = None, z = Z_LAYERS['entity']):
        super().__init__(groups) #adding sprite to group/s
        self.image = surf
        if self.image == None:
            self.image = pygame.Surface((16,16))
            self.image.fill('white')
        self.rect = self.image.get_frect(topleft = pos)
        self.old_rect = self.rect.copy() #gets position of sprites a frame before
        self.z = z
        
class AnimatedSprite(Sprite):
    def __init__(self, pos, frames, groups, z  = Z_LAYERS['entity'], animation_speed = ANIMATION_SPEED):
        self.frames, self.frame_index = frames, 0
        super().__init__(pos, self.frames[self.frame_index], groups = groups, z = z)
        self.animation_speed = animation_speed
    
    def animate(self, dt):
        self.frame_index += self.animation_speed * dt
        self.animation = self.frames[int(self.frame_index % len(self.frames))]
        
    def update(self, dt):
        self.animate(dt)