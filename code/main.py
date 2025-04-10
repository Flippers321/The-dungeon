from settings import *
from level import Level
from UI import Menu
from pytmx.util_pygame import load_pygame
from os.path import join
from functions import *

## Game Engine + timers inspired by ClearCode: https://www.youtube.com/@ClearCode

class Game:
    def __init__(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('platformer game')
        self.clock = pygame.time.Clock()
        self.import_sprites()
        
        self.tmx_maps = [load_pygame('data/levels/level1.tmx'),
                         load_pygame('data/levels/level2.tmx'),
                         load_pygame('data/levels/level3.tmx')]
        self.level_count = 1
        self.score = 0
        self.current_stage = Level(self.tmx_maps[self.level_count], self.obj_frames, self.score)
        self.menu = Menu()
        
        
        
    def import_sprites(self):
        self.obj_frames = {
            'player': import_sub_folders('assets/Miner'),
            'enemy': import_sub_folders('assets/Slime')
        }
        
    def run(self):
        while True:  
            dt = self.clock.tick(FPS) / 1000 #getting the time between frames in seconds
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                    
            self.current_score = self.current_stage.update_score(self.level_count)
            #print(self.current_score)

            self.current_stage.run(dt, self.level_count)
            
                
            if self.current_stage.check_win():
                print('win')
                #if self.level_count == 0:
                self.level_count += 1
                self.current_stage = Level(self.tmx_maps[self.level_count], self.obj_frames, self.current_score)

            if self.current_stage.check_restart():
                print('2 restart')
                self.level_count = 0
                self.current_score = 0
                self.current_stage = Level(self.tmx_maps[self.level_count], self.obj_frames, self.current_score)
            # if self.level_count == 2:
            #     self.menu.check_final_level()
            
            # if self.menu.restart():
            #     self.level_count = 0 

            
            pygame.display.update()
            
if __name__ == '__main__':
    game = Game()
    game.run()