from settings import *
from level import Level
from pytmx.util_pygame import load_pygame

#lolololololololololol
class Game:
    def __init__(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('platformer game')
        self.clock = pygame.time.Clock()
        
        self.tmx_maps = {0: load_pygame('data/levels/tutorial.tmx')} #!!
        self.current_stage = Level(self.tmx_maps[0])
        
    def run(self):
        while True:
            dt = self.clock.tick(FPS) / 1000 #getting the time between frames in seconds
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            
            self.current_stage.run(dt)
            
            pygame.display.update()
            
if __name__ == '__main__':
    game = Game()
    game.run()