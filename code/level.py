from settings import *
from sprites import Sprite
from player import Player
from enemy import Slime
from groups import CameraGroup
from UI import Menu

class Level():
    def __init__(self, tmx_map, obj_frames):
        self.display_surface = pygame.display.get_surface()
        pygame.mixer.init()
        
        #groups
        self.all_sprites = CameraGroup()
        self.collision_sprites = pygame.sprite.Group()
        self.damage_sprites = pygame.sprite.Group()
        self.enemy_sprites = pygame.sprite.Group()
        
        self.menu = Menu()

        #audio
        self.audio = {'jump': pygame.mixer.Sound('assets\MP3\sound1.mp3'),
                      'dash': pygame.mixer.Sound('assets\MP3\Retro10.mp3'),
                      'kill': pygame.mixer.Sound('assets\MP3\Retro7.mp3'),
                      'death': pygame.mixer.Sound('assets\MP3\death.mp3'),
                      'dash': pygame.mixer.Sound('assets\MP3\dash.mp3')}
        #self.audio_volume = round(self.menu.volume)

        self.setup(tmx_map, obj_frames)    
    #getting pos of values stored in layer
    def setup(self, tmx_map, obj_frames):
        #tiles
        for layer in ['spikes', 'platforms', 'cave', 'climbing chains', 'background obj']:
            for x,y,surf in tmx_map.get_layer_by_name(layer).tiles():
                #layer object now contains numbers instead of names, get the names 
                groups = [self.all_sprites]
                if layer == 'cave': groups.append(self.collision_sprites)
                if layer == 'platforms': groups.append(self.collision_sprites)
                if layer == 'spikes': groups.append(self.damage_sprites)
                z = Z_LAYERS['climbing chains']
                Sprite((x * TILE_SIZE, y * TILE_SIZE), surf, groups, z)

        #for enemy in Slime : groups.append(self.enemy_sprites)
        
        #spawn objects
        for obj in tmx_map.get_layer_by_name('spawn'):
            if obj.name == 'end':
                self.player.end_pos = pygame.Rect(obj.x, obj.y, obj.width, obj.height)
                
            if obj.name == 'start':
                self.player = Player(
                    pos = (obj.x, obj.y),
                    groups = self.all_sprites, 
                    collision_sprites = self.collision_sprites,
                    damage_sprites = self.damage_sprites,
                    enemy_sprites = self.enemy_sprites,
                    health = 3,
                    frames = obj_frames['player'],
                    audio = self.audio)
                    #volume = self.audio_volume)       
                             
            if obj.name == 'enemy':
                self.enemy = Slime(
                    pos = (obj.x, obj.y),
                    groups = [self.all_sprites, self.enemy_sprites],
                    collision_sprites = self.collision_sprites, 
                    damage_sprites = self.damage_sprites,
                    player_sprite = self.player,
                    frames = obj_frames['enemy'],)
                    #player_pos = self.player.rect)
                    
                groups.append(self.enemy_sprites)                
                
    def enemy_removal(self):
        if self.enemy.death() == True:
            self.enemy.rect.x = 260
            self.enemy.rect.y = 420


                    
    #def check_kill(self):
            
    def score(self):
        pass
        #if player movement start score, only increase score if paused = False
    def check_win(self):
        if self.player.rect.colliderect(self.player.end_pos):
            print('win')
            return True
            
            self.rect = self.image.get_frect(topleft = self.respawn)
            
    def draw_menu(self):
        if self.menu.game_paused == True:
            self.menu.draw(self.display_surface)
            if self.menu.paused_state == 'options':
               print(self.menu.volume)
               self.menu.draw_text(f'Volume: {round(self.menu.volume)}', (100, 100, 100), (WINDOW_WIDTH / 2) - 16, 450, self.display_surface)

        else:
            self.menu.draw_text('Press ESC to pause', (100, 100, 100), 20, 20, self.display_surface)
     

           
    def run(self, dt):
        self.display_surface.fill(BACKGROUND_COLOUR)
        self.all_sprites.update(dt)
        self.enemy_removal()
        self.check_win()
        self.all_sprites.draw(self.player)
        self.draw_menu()
        self.menu.menu_state(self.display_surface)
        self.menu.actions()