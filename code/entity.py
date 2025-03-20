from settings import *
from timer import Timer

class Entity(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(groups)
        #movement
        # self.direction = vector() 
        self.speed = 50
    #     self.drag_coefficient = 0.30
    #     self.gravity = 13
    #     self.jump = False
    #     self.jump_height = 5
    #     self.input_vector = vector()

    #     #collision detection
    #     self.on_surface = {'floor': False, 'left': False, 'right': False, 'roof': False}


    # def check_contacts(self):
    #     floor_rect = pygame.Rect(self.rect.bottomleft,(self.rect.width, 1))
    #     roof_rect = pygame.Rect(self.rect.topleft, (self.rect.width, 1))
    #     #strange collision thingy
    #     roof_rect.bottom = self.rect.top
    #     collide_rects = [sprite.rect for sprite in self.collision_sprites]

    #     right_rect = pygame.Rect(self.rect.topright + vector(0, self.rect.height / 4), (1, self.rect.height / 2))
    #     left_rect = pygame.Rect(self.rect.topleft + vector(0, self.rect.width / 4), (-1, self.rect.height / 2))

    #     #pygame.draw.rect(self.display_surface, 'yellow', floor_rect)
    #     #pygame.draw.rect(self.display_surface, 'yellow', roof_rect)


    #     self.on_surface['floor'] = True if floor_rect.collidelist(collide_rects) >= 0 else False
    #     self.on_surface['roof'] = True if roof_rect.collidelist(collide_rects) >= 0 else False
    #     self.on_surface['left'] = True if left_rect.collidelist(collide_rects) >= 0 else False
    #     self.on_surface['right'] = True if right_rect.collidelist(collide_rects) >= 0 else False

    # def collision(self, axis):
    #     for sprite in self.collision_sprites:
    #         #collision of walls and platforms
    #         if sprite.rect.colliderect(self.rect):
    #             if axis == 'horizontal':
    #                 # left
    #                 if self.rect.left <= sprite.rect.right and int(self.old_rect.left) >= int(sprite.old_rect.right):
    #                     self.rect.left = sprite.rect.right
    #                 # right
    #                 if self.rect.right >= sprite.rect.left and int(self.old_rect.right) <= int(sprite.old_rect.left):
    #                     self.rect.right = sprite.rect.left

    #             else: #vertical

    #                 #top
    #                 if self.rect.top <= sprite.rect.bottom and int(self.old_rect.top) >= int(sprite.old_rect.bottom):
    #                     self.rect.top = sprite.rect.bottom
    #                 #bottom
    #                 if self.rect.bottom >= sprite.rect.top and int(self.old_rect.bottom) <= int(sprite.old_rect.top):
    #                     self.rect.bottom = sprite.rect.top
    #                     self.direction.y = 0

    #     for sprite in self.damage_sprites:
    #         if sprite.rect.colliderect(self.rect) and not self.timers['damage'].active:
    #             self.health -= 1
    #             self.timers['damage'].activate()
    #             print(self.health)
    #             if self.health <= 0:
    #                 self.death()
