from settings import *

class Sprite(pygame.sprite.Sprite):
    def __init__(self, pos, surf = pygame.Surface((16,16)), groups = None, z = Z_LAYERS['entity']):
        super().__init__(groups) #adding sprite to group/s
        self.image = surf
        if self.image == None:
            #if sprite has no image, then default to white
            self.image = pygame.Surface((16,16))
            self.image.fill('white')
        self.rect = self.image.get_frect(topleft = pos)
        self.old_rect = self.rect.copy() #gets position of sprites a frame before
        self.z = z #z-layer rendering order of sprites
        
class MovingSprite(Sprite):
    def __init__(self, groups, start_pos, end_pos, move_direction, speed):
        surf = pygame.Surface((200, 20))
        super().__init__(start_pos, surf, groups)
        if move_direction == 'x':
            self.rect.center = start_pos #centre of horizontal movement
        else:
            self.rect.midtop = start_pos #top for vertical movement
        self.start_pos = start_pos
        self.end_pos = end_pos
        
        #movement attributes
        self.moving = True
        self.speed = speed
        self.direction = vector(1,0) if move_direction == 'x' else vector(0, 1)
        self.move_direction = move_direction
        
    def check_movement(self):
        if self.move_direction == 'x':
            #reversing if reaches the end/start positions on x-axis
            if self.rect.right >= self.end_pos[0] and self.direction.x == 1:
                self.direction.x = -1
                self.rect.right = self.end_pos[0]
            if self.rect.left <= self.start_pos[0] and self.direction.x == -1:
                 self.direction.x = 1
                 self.rect.left = self.start_pos[0]
        if self.move_direction == 'y':
            #reversing if reaches the end/start positions on y-axis
            if self.rect.bottom >= self.end_pos[1] and self.direction.y == 1:
                self.direction.y = -1
                self.rect.bottom = self.end_pos[1]
            if self.rect.top <= self.start_pos[1] and self.direction.y == -1:
                self.direction.y = 1
                self.rect.top = self.start_pos[1]        
        
    def update(self, dt):
        #updating position of the moveing sprite
        self.old_rect = self.rect.copy()
        self.rect.topleft += self.direction * self.speed * dt
        self.check_movement()
        
class AnimatedSprite(Sprite):
    def __init__(self, pos, frames, groups, z  = Z_LAYERS['entity'], animation_speed = ANIMATION_SPEED):
        self.frames, self.frame_index = frames, 0
        super().__init__(pos, self.frames[self.frame_index], groups = groups, z = z)
        self.animation_speed = animation_speed
    
    def animate(self, dt):
        #update the animation frames based on time
        self.frame_index += self.animation_speed * dt
        self.animation = self.frames[int(self.frame_index % len(self.frames))]
        
    def update(self, dt):
        self.animate(dt)