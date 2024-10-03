from settings import *
from sprites import Sprite
from player import Player
from groups import CameraGroup

##level 2 moving platforms?

class Level:
    def __init__(self, tmx_map):
        self.display_surface = pygame.display.get_surface()
        
        #groups
        self.all_sprites = CameraGroup()
        self.collision_sprites = pygame.sprite.Group()
        
        self.setup(tmx_map)
    
    #getting pos of values stored in layer
    def setup(self, tmx_map):
        #tiles
        for layer in ['gem', 'spikes', 'platforms', 'cave', 'climbing chains', 'background obj']:
            for x,y,surf in (tmx_map.get_layer_by_name(layer).tiles()):
                groups = [self.all_sprites]
                if layer == 'cave': groups.append(self.collision_sprites)
                if layer == 'platforms': groups.append(self.collision_sprites)
                z = Z_LAYERS['climbing chains']
                Sprite((x * TILE_SIZE, y * TILE_SIZE), surf, groups, z)

        
        #spawn objects
        for obj in tmx_map.get_layer_by_name('spawn'):
            if obj.name == 'start':
                self.player = Player((obj.x, obj.y), self.all_sprites, self.collision_sprites)
        
        #no bg displayed yet
        #moving objects?
            
            
    def run(self, dt):
        self.display_surface.fill((38, 28, 26))
        self.all_sprites.update(dt)
        self.all_sprites.draw(self.player)