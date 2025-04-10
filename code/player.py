from settings import *
from timer import Timer
from os.path import join 
import json
from UI import Menu

class Player(pygame.sprite.Sprite):
    def __init__(self, pos,  groups, collision_sprites, damage_sprites, enemy_sprites, health, frames, audio):
        super().__init__(groups)
        self.z = Z_LAYERS['entity']

        self.frames, self.frame_index = frames, 0
        self.state, self.facing_right = 'idle', True
        self.image = self.frames[self.state][self.frame_index]
        
        self.menu = Menu() # can not get menu to pause player movement and know when player is win
        
        
        #image
        self.respawn = pos
        self.end_pos = (0,0)
        #rects
        self.rect = self.image.get_frect(topleft = pos)
        self.old_rect = self.rect.copy()

        #movement
        self.direction = vector() 
        self.speed = 50
        self.drag_coefficient = 0.30
        self.gravity = 13
        self.jump = False
        self.jump_height = 5
        self.bonus_jumps = 1
        self.dash = False
        self.dashx_multi = 3
        self.dashy_multi = 1.6
        self.dash_num = 1
        self.health = self.max_health = health
        self.input_vector = vector()

        #collision detection
        self.collision_sprites = collision_sprites
        self.damage_sprites = damage_sprites
        self.enemy_sprites = enemy_sprites
        self.on_surface = {'floor': False, 'left': False, 'right': False, 'roof': False}
        self.on_enemy = False
        self.platform = False

        #timer
        self.timers = {
            'wall jump': Timer(400),
            'dash': Timer(5),
            'damage': Timer(300)
        }

        #audio
        self.jump_sound = audio['jump']
        self.dash_sound = audio['dash']
        self.kill_sound = audio['kill']
        self.death_sound = audio['death'] 
        self.hit_sound = audio['hit']
        
        self.score = 0

    def get_volume(self, volume):    
         with open("code\config.json", "r") as c:
             data = json.load(c)
             #if data == '':
             #    self(self.default_settings)
             value = data.get(volume)
             #print('val', value)
             self.new_volume = (value / 100)
             #print('new_val', self.new_volume)

             return(self.new_volume)
    def input(self):

        keys = pygame.key.get_pressed()
        self.input_vector = vector(0, 0)
        key_down = pygame.key.get_just_pressed()

        if keys[pygame.K_s]:
            self.input_vector.y += 1
        if keys[pygame.K_w]:
            self.input_vector.y += -1
        #horizontal
        if not self.timers['wall jump'].active:
            if keys[pygame.K_a]:
                self.input_vector.x += -1 #move left
                self.facing_right = False
            if keys[pygame.K_d]:
                self.input_vector.x += 1 #move right
                self.facing_right = True
            #if opposite keys (a , d) are simultaniously pressed, vector movement = 0
            
        #jumping
        if key_down[pygame.K_SPACE]:
            self.jump = True
        else:
            self.jump = False
                
        if key_down[pygame.K_SPACE] and self.bonus_jumps > 0 and not any((self.on_surface['left'], self.on_surface['right'], self.on_surface['floor'])):
            self.direction.y = -self.jump_height
            self.bonus_jumps -= 1
            
        if key_down[pygame.K_LSHIFT] and self.dash_num > 0:
            self.timers['dash'].activate()
            self.dash_sound.play()
            self.dash_sound.set_volume(self.get_volume('volume'))


    def move(self, dt):
        
        #print(self.input_vector)
        #horizontal
        self.direction.x += self.input_vector.x * self.speed

        if self.timers['dash'].active:
            self.dash_num -= 1
            self.direction.x = self.direction.x * self.speed * self.dashx_multi * dt
            self.direction.y = self.direction.y * self.speed * self.dashy_multi * dt
            
        if self.timers['damage'].active:
            self.direction.x = self.direction.x / 1.15
            self.direction.y = self.direction.y / 1.15
            
        #drag
        self.direction.x *= 0.80

        self.rect.x += self.direction.x * dt ## make it self.drag? do one for both x and
        self.collision('horizontal')  
        
        #veritcal
        if self.jump:
            self.jump_sound.play()
            self.jump_sound.set_volume(self.get_volume('volume'))
            print(self.get_volume('volume'))
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
        
    def move_platform(self, dt):
        if self.platform:
            self.rect.x += self.platform.direction.x * self.platform.speed * dt
    def animate(self, dt):
        
        self.frame_index += ANIMATION_SPEED * dt
        self.image = self.frames[self.state][int(self.frame_index % len(self.frames[self.state]))]
        self.image = self.image if self.facing_right else pygame.transform.flip(self.image, True, False)

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
        self.platform = None
        for sprite in [sprite for sprite in self.collision_sprites.sprites() if hasattr(sprite, 'moving')]:
            if sprite.rect.colliderect(floor_rect):
                print('player , on platform')
                self.platform = sprite

        self.on_surface['floor'] = True if floor_rect.collidelist(collide_rects) >= 0 else False
        self.on_surface['roof'] = True if roof_rect.collidelist(collide_rects) >= 0 else False
        self.on_surface['left'] = True if left_rect.collidelist(collide_rects) >= 0 else False
        self.on_surface['right'] = True if right_rect.collidelist(collide_rects) >= 0 else False

        #getting if the player is on a moving platform


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
            if sprite.rect.colliderect(self.rect) and not self.timers['damage'].active:
                self.health -= 1
                self.hit_sound.play()
                self.hit_sound.set_volume(self.get_volume('volume'))
                self.timers['damage'].activate()
                if self.health <= 0:
                    self.death()
                    
    def check_enemy_hit(self):
        for sprite in self.enemy_sprites:
            if sprite.rect.colliderect(self.rect) and not self.timers['damage'].active:
                self.health -= 1
                self.hit_sound.play()
                self.hit_sound.set_volume(self.get_volume('volume'))
                self.timers['damage'].activate()
                print('enemies hurt')
                if self.health <= 0:
                    self.death()
     
            if sprite.rect.colliderect(self.rect):
                if self.rect.bottom >= (sprite.rect.top - 1) and int(self.old_rect.bottom) <= int(sprite.old_rect.top):
                    print('enemy felled')
                    self.kill_sound.play()
                    self.kill_sound.set_volume(self.get_volume('volume'))
                    return True               
                
    def check_ifdead(self):
        if self.health <= 0:
            self.death

    def death(self):
        self.rect = self.image.get_frect(topleft = self.respawn)
        self.health = self.max_health
        self.death_sound.play()
        self.death_sound.set_volume(self.get_volume('volume'))


    def update_timers(self):
        for timer in self.timers.values():
            timer.update()

    def update(self, dt):
        self.old_rect = self.rect.copy()
        self.update_timers()
        self.get_volume('volume')
        self.input()
        #update drag
        if self.on_surface['floor']:
            self.bonus_jumps = 1
            self.dash_num = 1
        self.move(dt)
        self.move_platform(dt)
        self.animate(dt)
        #self.dash_timer(dt)
        self.check_contacts()
        self.check_enemy_hit()
        #print(self.timers['wall jump'].active)
