from settings import *



class Button:
    def __init__(self, x, y, image, scale):
        width = image.get_width()
        height = image.get_width()
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        
    def draw(self, surface):
        
        pos = pygame.mouse.get_pos()
        
        #checking if mouse id on button and the clicked condtion
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                print('clicked')
                return True
                
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False
            
        surface.blit(self.image, (self.rect.x, self.rect.y))
        return False

class Menu:
    def __init__(self):
        
        
        self.font = pygame.font.Font(r'assets\Perfect DOS VGA 437.ttf', 16)
        self.game_paused = False
        self.menu_butttons_offset_5 = 2.5 * 16
        
        #load images
        self.button_images = {'resume': pygame.image.load(r'assets\Buttons\resume.png').convert_alpha(),
                              'options': pygame.image.load(r'assets\Buttons\options.png').convert_alpha(),
                              'leaderboard': pygame.image.load(r'assets\Buttons\leaderboard.png').convert_alpha(),
                              'restart': pygame.image.load(r'assets\Buttons\restart.png').convert_alpha(),
                              'quit': pygame.image.load(r'assets\Buttons\quit.png').convert_alpha(),
                              }
        
        #button instances
        self.buttons = [Button((WINDOW_WIDTH / 2) - self.menu_butttons_offset_5, 100, self.button_images['resume'], 5), # scaled so img = 80 x 80
                         Button((WINDOW_WIDTH / 2) - self.menu_butttons_offset_5, 250, self.button_images['options'], 5),
                         Button((WINDOW_WIDTH / 2) - self.menu_butttons_offset_5, 400, self.button_images['leaderboard'], 5),
                         Button((WINDOW_WIDTH / 2) - self.menu_butttons_offset_5, 550, self.button_images['restart'], 5),
                         Button(WINDOW_WIDTH - (16 * 3), 0, self.button_images['quit'], 3)]  # scaled so img = 80 x 80]
        
    def menu_state(self, surface): #should i make menu state a dictionary that then uses teh value in the dict to do things
        print('menu state')
        keys = pygame.key.get_just_pressed()
        if keys[pygame.K_ESCAPE] and self.game_paused == False:
            self.game_paused = True
            surface = pygame.transform.box_blur(surface, 2)#bluriong every frame then drawing on top every frame
            print(self.game_paused)
        elif keys[pygame.K_ESCAPE] and self.game_paused == True:
            self.game_paused = False
            print(self.game_paused)
            
            ##blur screen and make score stop, make player and enemy stop movement.
        self.actions(surface)
             
            
    def actions(self, surface):
        print('')
        if self.game_paused == True:
            for button in self.buttons:
                if self.buttons[0].draw(surface):
                    print('resume')
                    self.game_paused = False
                    print(self.game_paused)
                elif self.buttons[1].draw(surface):
                    pass
                elif self.buttons[2].draw(surface):
                    pass
                elif self.buttons[3].draw(surface):
                    pass
                elif self.buttons[4].draw(surface):
                    pygame.quit()
                    sys.exit()
                
    def draw_text(self, text, colour, x, y, surface):
        img = self.font.render(text, True, colour)
        surface.blit(img, (x,y))
        
    def draw(self, surface):
        for button in self.buttons:
            button.draw(surface)
            
            

        