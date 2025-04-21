from settings import *
from sprites import Sprite, MovingSprite
from player import Player
from enemy import Slime
from groups import CameraGroup
from UI import Menu
import requests, json

class Level():
    def __init__(self, tmx_map, obj_frames, score, level_num):
        self.display_surface = pygame.display.get_surface()
        pygame.mixer.init()
        
        #groups
        self.all_sprites = CameraGroup()
        self.collision_sprites = pygame.sprite.Group()
        self.damage_sprites = pygame.sprite.Group()
        self.enemy_sprites = pygame.sprite.Group()
        
        self.level_count = level_num
        self.score = score
        self.menu = Menu()
        #audio
        self.audio = {'jump': pygame.mixer.Sound('assets\MP3\sound1.mp3'),
                      'dash': pygame.mixer.Sound('assets\MP3\Retro10.mp3'),
                      'kill': pygame.mixer.Sound('assets\MP3\Retro7.mp3'),
                      'death': pygame.mixer.Sound('assets\MP3\death.mp3'),
                      'dash': pygame.mixer.Sound('assets\MP3\dash.mp3'),
                      'hit': pygame.mixer.Sound('assets\MP3\hit.mp3')}
        self.platform_speed = 100
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
                    health = 10,
                    frames = obj_frames['player'],
                    audio = self.audio,
                    level_count = self.level_count)    
                             
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
                
        for obj in tmx_map.get_layer_by_name('Moving_objects'):
            if obj.name == 'moving wall left':
                move_direction = 'x'
                start_pos = (obj.x - 32, obj.y + obj.height/2)
                end_pos = (obj.x + obj.width, obj.y + obj.height/2)
                MovingSprite((self.all_sprites, self.collision_sprites), start_pos, end_pos, move_direction, self.platform_speed)  
    def enemy_removal(self, level_count):
        if self.enemy.death() == True:
            if level_count == 0:
                #amount of tiles (using the tmx file) for position of enemy cage
                self.enemy.rect.x = 16 * TILE_SIZE
                self.enemy.rect.y = 26 * TILE_SIZE
            if level_count == 1:
                self.enemy.rect.x = 33 * TILE_SIZE 
                self.enemy.rect.y = 66 * TILE_SIZE 
            self.score -= 500

    def update_score(self, level_count):
        if level_count != 2:
            self.score += 1
            #making sure score doesnt go negative (as killing an enemy decreases score)
            #This also makes it so the lowesr score (the best one) can only be 0
            if self.score < 0:
                self.score = 0        
            return(self.score)


        # if self.menu.restart():
        #     self.score = 0
            

        #if player movement start score, only increase score if paused = False
    def check_win(self):
        if self.player.rect.colliderect(self.player.end_pos):
            return True
        return False
    
    def check_restart(self):
        if self.menu.restart == True:
            print('1 restart')
            self.menu.restart = False
            return True
            
    def post_score(self, score):    
        if self.menu.submit == True and self.menu.win_input[0].input != '':
            try:
                print('this pont')
                request = requests.post("http://127.0.0.1:5000/leaderboard", json = json.dumps({ "data": [self.menu.win_input[0].input, score]}))
                self.menu.submit = False
            except:
                print("ERROR SENDING TO SERVER")
        
    def draw_highscores(self, num_offset, centre_offset_score, centre_offset_user, text_size = 28):
        try:
            highscores = requests.get("http://127.0.0.1:5000/SERVER") #TODO
        except:
            self.menu.draw_text(f'FAILED TO LOAD CONNECT TO SERVER', (100, 100, 100), ((WINDOW_WIDTH//2) - centre_offset_user),(250 + 24), self.display_surface, size = 32)
        
        for i,score in enumerate(highscores.json()):
            self.menu.draw_text(f'{i + 1}.', (100, 100, 100), ((WINDOW_WIDTH//2) - num_offset),(250 + 24*i), self.display_surface, size = text_size)
            self.menu.draw_text(f'{score[0]}', (100, 100, 100), ((WINDOW_WIDTH//2) - centre_offset_user),(250 + 24*i), self.display_surface, size = text_size) #(instead of print do draw_text? just callk it on line 150)
            self.menu.draw_text(f'{score[1]}', (100, 100, 100), ((WINDOW_WIDTH//2) + centre_offset_score),(250 + 24*i), self.display_surface, size = text_size)
        
    #displaying the menus
    def draw_menu(self, level_count):
        self.previous_scores = True
        
        if level_count != 2:
            if self.menu.game_paused == True:
                self.menu.draw(self.display_surface, level_count)
                if self.menu.paused_state == 'options':
                #print(self.menu.volume)
                    self.menu.draw_text(f'Volume: {round(self.menu.volume)}', (100, 100, 100), (WINDOW_WIDTH / 2) - 16, 450, self.display_surface)
                
                
                if self.menu.paused_state == 'win':
                    print('/////////////\n///////////\nshould be printing')
                    self.menu.draw_text('Congratulations!', (100, 100, 100), 100, 20, self.display_surface)
                    self.menu.draw_text(f'Your Score: {round(self.score)}', (100, 100, 100), 100, 50, self.display_surface)
                    self.menu.draw_text('Press ENTER to return', (100, 100, 100), 100, WINDOW_HEIGHT - 40, self.display_surface)
                self.menu.draw_text(f'score: {round(self.score)}', (100, 100, 100), 80, WINDOW_HEIGHT - 40, self.display_surface)

                
                if self.menu.paused_state == 'leaderboard':
                    self.menu.draw_text('user', (100, 200, 100), ((WINDOW_WIDTH//2) - 150), 200, self.display_surface, size = 30)
                    self.menu.draw_text('score', (100, 200, 100), ((WINDOW_WIDTH//2) + 150), 200, self.display_surface, size = 30)
                    self.draw_highscores(200, 150, 150) #setting the users, scores, and positions of the leaderboards offsets from the centre of the screen (same as the 'user','score' text offsets)


            else:
                self.menu.draw_text('Press ESC to Pause', (100, 100, 100), 100, 20, self.display_surface)
                self.menu.draw_text('Press LSHIFT to Dash', (100, 100, 100), 100, 50, self.display_surface)
                self.menu.draw_text(f'score: {round(self.score)}', (100, 100, 100), 80, WINDOW_HEIGHT - 40, self.display_surface)
                self.menu.draw_text(f'Lives: {round(self.player.health)}', (100, 100, 100), 200, WINDOW_HEIGHT - 40, self.display_surface)

        else:
            self.menu.draw_text(f'Your Score: {round(self.score)}', (255, 255, 255), (WINDOW_WIDTH / 2), 50, self.display_surface)
            self.menu.draw_text('Congratulations!', (255, 255, 255), 950, 455, self.display_surface)
            if self.menu.game_paused == False and self.menu.submit == False:
                self.menu.draw_text('press ESC to submit score!', (255, 255, 255), (WINDOW_WIDTH / 2), 70, self.display_surface)
            if self.menu.game_paused == True:
                self.menu.draw_text('username:', (255, 255, 255), (WINDOW_WIDTH / 2), 320, self.display_surface)
                self.menu.draw(self.display_surface, level_count)

            self.menu.draw_text('Previous Highscores', (150, 150, 150), ((WINDOW_WIDTH//2) - 400), 180, self.display_surface, size = 15)
            self.menu.draw_text('user', (100, 200, 100), ((WINDOW_WIDTH//2) - 440), 220, self.display_surface, size = 15)
            self.menu.draw_text('score', (100, 200, 100), ((WINDOW_WIDTH//2) - 340), 220, self.display_surface, size = 15)
            self.draw_highscores(500, -350, 450, 20)                    
                    
                

           
    def run(self, dt, level_count):
        self.display_surface.fill(BACKGROUND_COLOUR)
        self.all_sprites.update(dt)
        self.enemy_removal(level_count)
        self.check_win()
        self.check_restart()
        self.update_score(level_count)
        self.post_score(self.score)
        self.all_sprites.draw(self.player)
        self.draw_menu(level_count)
        self.menu.menu_state(level_count)
        self.menu.paused_actions()
        self.menu.win_actions()