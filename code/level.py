from settings import *
from sprites import Sprite
from player import Player

class Level:
    def __init__(self, tmx_map):
        self.display_surface = pygame.display.get_surface()
        
        #groups
        self.all_sprites = pygame.sprite.Group()
        self.collision_sprites = pygame.sprite.Group()
        
        self.setup(tmx_map)
    
    #getting pos of values stored in layer
    def setup(self, tmx_map):
        for x,y,surf in tmx_map.get_layer_by_name('cave').tiles(): #no bg displayed yet
            Sprite((x * TILE_SIZE, y * TILE_SIZE), surf, (self.all_sprites, self.collision_sprites))
            
        for obj in tmx_map.get_layer_by_name('spawn'):
            if obj.name == 'start':
                print('l')
                Player((obj.x, obj.y), self.all_sprites, self.collision_sprites)
            
    def run(self, dt):
        self.display_surface.fill((50, 50, 50))
        self.all_sprites.update(dt)
        self.all_sprites.draw(self.display_surface)