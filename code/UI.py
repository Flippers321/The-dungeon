from settings import *

class Button:
    def __init__(self, x, y, image, scale):
        width = image.get_width()
        height = image.get_width()
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False
        
    def draw(self, surface):
        
        pos = pygame.mouse.get_pos()
        
        #checking if mouse id on button and the clicked condtion
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                action = True
                
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False
            
        surface.blit(self.image, (self.rect.x, self.rect.y))
        
class Score: 
    pass ## draw text of score
class Menu:
    def __init__(self):
        
        
        self.font = pygame.font.Font(r'assets\Perfect DOS VGA 437.ttf', 16)
        self.game_paused = False
        
        #load images
        self.button_images = {'resume': pygame.image.load(r'assets\Buttons\resume.png').convert_alpha(),
                              'options': pygame.image.load(r'assets\Buttons\options.png').convert_alpha(),
                              'leaderboard': pygame.image.load(r'assets\Buttons\leaderboard.png').convert_alpha(),
                              'restart': pygame.image.load(r'assets\Buttons\restart.png').convert_alpha(),
                              }
        
        #button instances
        self.buttons = [Button(WINDOW_WIDTH / 2, 100, self.button_images['resume'], 5), # scaled so img = 80 x 80
                         Button(WINDOW_WIDTH / 2, 250, self.button_images['options'], 5),
                         Button(WINDOW_WIDTH / 2, 400, self.button_images['leaderboard'], 5),
                         Button(WINDOW_WIDTH / 2, 550, self.button_images['restart'], 5)]
        
        
    def paused(self, surface):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            self.game_paused = True
            print('pressed')
            ##blur screen and make score stop, make player and enemy stop movement.
        if self.game_paused == True:    
            surface = pygame.transform.box_blur(surface, 2) ##???
            
         
    def draw_text(self, text, colour, x, y, surface):
        img = self.font.render(text, True, colour)
        surface.blit(img, (x,y))
        
    def draw(self, surface):
        for button in self.buttons:
            button.draw(surface)
        
    def check_paused(self):
        if self.game_paused:
            print('game paused')
            #display menu
        else:
            self.draw_text('press ESC to pause', self.font, self.text_colour)
            
    ##def actions:: unpause = press resume or press esc when paused = True
            

        