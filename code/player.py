from settings import *
from timer import Timer

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, collision_sprites):
        super().__init__(groups)
        self.image = pygame.Surface((16,16))
        self.image.fill('blue')

        #rects
        self.rect = self.image.get_frect(topleft = pos)
        self.old_rect = self.rect.copy()

        #movement
        self.direction = vector()
        self.speed = 575
        self.drag_coefficient = 0.30
        self.gravity = 12
        self.jump = False
        self.jump_height = 4.6
        self.bonus_jumps = 1
        self.dash = False
        self.dashx_multi = 9.9
        self.dashy_multi = 1.3
        self.dash_num = 1

        #collision detection
        self.collision_sprites = collision_sprites
        self.on_surface = {'floor': False, 'left': False, 'right': False, 'roof': False}

        #timer
        self.timers = {
            'wall jump': Timer(400),
            'wall slide': Timer(250)
        }

    def input(self):
        keys = pygame.key.get_pressed()
        input_vector = vector(0, 0)
        key_down = pygame.key.get_just_pressed()

        #horizontal
        if not self.timers['wall jump'].active:
            if keys[pygame.K_a]:
                input_vector.x += -1 #move left
            if keys[pygame.K_d]:
                input_vector.x += 1 #move right
            #if opposite keys (a , d) are simultaniously pressed, vector movement = 0
            if abs(input_vector.x) > 0:
                self.direction.x = input_vector.normalize().x if input_vector else input_vector.x #making vector always equal 1, or if 0, just the input
            #print(self.direction)

        #dash activation
        if key_down[pygame.K_LSHIFT] and self.dash_num >= 1: #dashing in x plane is wrong?
            self.dash = True
        
        #downward dash
        if keys[pygame.K_s] and self.dash == True:
            self.dash_num -= 1 
            self.direction.y = self.jump_height * self.dashy_multi

        #jumping
        if keys[pygame.K_SPACE]:
            self.jump = True
            if self.on_surface['floor']:
                self.direction.y = -self.jump_height
                self.timers['wall slide'].activate()
                
       
        if key_down[pygame.K_SPACE] and self.bonus_jumps > 0 and not self.on_surface['floor']:
            self.direction.y = -self.jump_height
            self.bonus_jumps -= 1
        if keys[pygame.K_SPACE] and self.dash == True:
            self.dash_num -= 1
            self.direction.y = -self.jump_height * self.dashy_multi

    def add_drag(self, dt):
        self.direction.x *= self.drag_coefficient ## make it self.drag? do one for both x and y to impliment into move? - update() only changes max, not acceleration??
        #preventing speed being too slow, so drag stops when player is moving slow enough
        #print(self.direction.x * self.drag_coefficient)
        #print(self.direction.x)
        if -0.01 < self.direction.x and self.direction.x < 0.01: self.direction.x = 0
        if -0.01 < self.direction.y and self.direction.y < 0.01: self.direction.y = 0

    def move(self, dt):
        self.add_drag(dt)
        #horizontal
        if self.dash == True:
            self.rect.x += self.direction.x * self.speed * self.dashx_multi * dt
            self.dash = False
            self.dash_num -= 1
        self.rect.x += self.direction.x * self.speed * dt ## make it self.drag? do one for both x and
        
        self.collision('horizontal')

        #vertical
        if not self.on_surface['floor'] and any((self.on_surface['left'], self.on_surface['right'])) and not self.timers['wall jump'].active:
            self.direction.y = 0
            self.rect.y += self.gravity * 5 * dt
        else:
            self.direction.y += self.gravity / 2 * dt  #dividing by two and then putting it twice to make sure it is fps independant
            self.rect.y += self.direction.y
            self.direction.y += self.gravity / 2 * dt
            
        if self.jump: #wall jumps -TODO!- jumping while holding direction of wall, only slide if y direction is down(pos) only slide if holding into wall - redo whole wall slide                
            if any((self.on_surface['left'], self.on_surface['right'])) and not self.timers['wall slide'].active:
                #if self.bonus_jumps < 1:
                #    self.bonus_jumps += 1
                self.direction.y = -self.jump_height
                self.direction.x = 1 if self.on_surface['left'] else -1
            self.jump = False
            
        self.collision('vert')

        #checking if player has collided with a cieling
        if self.on_surface['roof']:
            self.direction.y = 0.6

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
            if sprite.rect.colliderect(self.rect):
                if axis == 'horizontal':
                    # left
                    if self.rect.left <= sprite.rect.right and self.old_rect.left >= sprite.old_rect.right:
                        self.rect.left = sprite.rect.right
                    # right
                    if self.rect.right >= sprite.rect.left and self.old_rect.right <= sprite.old_rect.left:
                        self.rect.right = sprite.rect.left

                else: #vertical

                    #top
                    if self.rect.top <= sprite.rect.bottom and self.old_rect.top >= sprite.old_rect.bottom:
                        self.rect.top = sprite.rect.bottom
                    #bottom
                    if self.rect.bottom >= sprite.rect.top and self.old_rect.bottom <= sprite.old_rect.top:
                        self.rect.bottom = sprite.rect.top
                        self.direction.y = 0

    def update_timers(self):
        for timer in self.timers.values():
            timer.update()

    def update(self, dt):
        self.old_rect = self.rect.copy()
        self.update_timers()
        self.input()
        if self.on_surface['floor']:
            self.bonus_jumps = 1
            self.dash_num = 1
        self.move(dt)
        #self.dash_timer(dt)
        self.check_contacts()
        #print(self.timers['wall jump'].active)




