from settings import *
from timer import Timer
from player import Player

class Slime(pygame.sprite.Sprite):
    def __init__(self, pos, groups, collision_sprites, damage_sprites, player_sprite, frames):
        super().__init__(groups)
        self.z = Z_LAYERS['entity']

        self.frames, self.frame_index = frames, 0
        self.image = self.frames['idle'][self.frame_index]
        self.player = player_sprite

        self.jumps = 1

        self.rect = self.image.get_frect(topleft = pos)
        self.old_rect = self.rect.copy()
        
        #movement
        self.direction = vector() 
        self.speed = 50
        self.drag_coefficient = 0.30
        self.gravity = 13
        self.jump = False
        self.jump_height = 5
        self.detect_vector = vector()
        self.health = 1
        self.playerx = 0
        self.playery = 0
        
        #collisions
        self.collision_sprites = collision_sprites
        self.damage_sprites = damage_sprites
        self.on_surface = {'floor': False, 'left': False, 'right': False, 'roof': False}
        
        
        
    def detection(self):
        #player detection
        self.detect_vector = (0, 0)
        print(self.rect.x)
        #horizontal pathing
        if self.player.rect.x > self.rect.x:
            print('pleyer is on the right')
            self.detection_vector.x += 1
        if Player.x < self.rect.x:
            self.detection_vector -= 1
            
        if Player.rect.y > self.rect.y:
            self.jump = True
        else:
            self.jump = False
            
    def movement(self, dt):
        
        self.direction.x = self.detect_vector.x *  self.speed
        self.direction.x *= 0.8
        self.rect.x += self.direction.x * dt
        self.collision('horizontal')
        
        if self.jump:
            if self.on_surface['floor']:
                self.direction.y = -self.jump_height
            elif self.on_surface['left']:
                self.direction.y = -self.jump_height
                self.direction.x = 200
            elif self.on_surface['right']:
                self.direction.y = -self.jump_height
                self.direction.x = -200               
        if self.on_surface['roof']:
            self.direction.y = 0

        self.direction.y += self.gravity * dt
        if self.on_surface['left'] or self.on_surface['right']:
            if self.direction.y > 1:
                self.direction.y = 1

        self.rect.y += self.direction.y
        self.collision('vert')            
         
    def check_contacts(self):
        floor_rect = pygame.Rect(self.rect.bottomleft,(self.rect.width, 1))
        roof_rect = pygame.Rect(self.rect.topleft, (self.rect.width, 1))
        #strange collision thingy
        roof_rect.bottom = self.rect.top
        collide_rects = [sprite.rect for sprite in self.collision_sprites]

        right_rect = pygame.Rect(self.rect.topright + vector(0, self.rect.height / 4), (1, self.rect.height / 2))
        left_rect = pygame.Rect(self.rect.topleft + vector(0, self.rect.width / 4), (-1, self.rect.height / 2))

        #pygame.draw.rect(self.display_surface, 'yellow', floor_rect)
        #pygame.draw.rect(self.display_surface, 'yellow', roof_rect)


        self.on_surface['floor'] = True if floor_rect.collidelist(collide_rects) >= 0 else False
        self.on_surface['roof'] = True if roof_rect.collidelist(collide_rects) >= 0 else False
        self.on_surface['left'] = True if left_rect.collidelist(collide_rects) >= 0 else False
        self.on_surface['right'] = True if right_rect.collidelist(collide_rects) >= 0 else False

    def collision(self, axis):
        for sprite in self.collision_sprites:
            #collision of walls and platforms
            if sprite.rect.colliderect(self.rect):
                if axis == 'horizontal':
                    # left
                    if self.rect.left <= sprite.rect.right and int(self.old_rect.left) >= int(sprite.old_rect.right):
                        self.rect.left = sprite.rect.right
                    # right
                    if self.rect.right >= sprite.rect.left and int(self.old_rect.right) <= int(sprite.old_rect.left):
                        self.rect.right = sprite.rect.left

                else: #vertical

                    #top
                    if self.rect.top <= sprite.rect.bottom and int(self.old_rect.top) >= int(sprite.old_rect.bottom):
                        self.rect.top = sprite.rect.bottom
                    #bottom
                    if self.rect.bottom >= sprite.rect.top and int(self.old_rect.bottom) <= int(sprite.old_rect.top):
                        self.rect.bottom = sprite.rect.top
                        self.direction.y = 0

        for sprite in self.damage_sprites:
            if sprite.rect.colliderect(self.rect):
                self.health -= 1
                if self.health <= 0:
                    self.death()
                    
    def death(self):
        if self.player.check_enemy_hit():
            return True

    def update(self, dt):
        self.old_rect = self.rect.copy()
        #update drag
        self.movement(dt)
        self.check_contacts()
        self.death()
