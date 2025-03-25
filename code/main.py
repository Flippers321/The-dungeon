from settings import *
from level import Level
from pytmx.util_pygame import load_pygame
from os.path import join
from functions import *

class Game:
    def __init__(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('platformer game')
        self.clock = pygame.time.Clock()
        self.import_sprites()
        
        self.tmx_maps = [load_pygame('data/levels/tutorial.tmx'),
                         load_pygame('data/levels/level2.tmx')]
        self.level_count = 0
        self.score = 0
        self.current_stage = Level(self.tmx_maps[self.level_count], self.obj_frames, self.score)
        
        
        
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
                    
            self.current_score = self.current_stage.update_score()
            #print(self.current_score)

            self.current_stage.run(dt)
            if self.current_stage.check_win():
                print('win')
                if self.current_stage == 0:
                    self.level_count += 1
                    self.current_stage = Level(self.tmx_maps[self.level_count], self.obj_frames, self.current_score)
                else:
                    self.level_count +=0
                    

            
            pygame.display.update()
            
if __name__ == '__main__':
    game = Game()
    game.run()