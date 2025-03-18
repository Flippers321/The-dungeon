from settings import *



class Button:
    def __init__(self, pos, image, scale):
        width = image.get_width()
        height = image.get_width()
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.center = pos
        
    def draw(self, surface):
            
        surface.blit(self.image, (self.rect.x, self.rect.y))
        return False
    
    def get_click(self):
                
        pos = pygame.mouse.get_pos()
        
        #checking if mouse id on button and the clicked condtion
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_just_pressed()[0] == 1:
                print('clicked')
                return True
            
class slider:
    def __init__(self, pos, size, initial_val, min, max):
        self.pos = pos
        self.size = size
        
        self.slider_left_pos = self.pos[0] - (size[0]//2)
        self.slider_rigt_pos = self.pos[0] + (size[0]//2)
        self.slider_top_pos = self.pos[1] - (size[1]//2)
        
        self.min = min
        self.max = max
        self.initial_val = (self.slider_right_pos - self.slider_left_pos) * initial_val # percentage        
class Menu:
    def __init__(self):
        
        
        self.font = pygame.font.Font(r'assets\Perfect DOS VGA 437.ttf', 16)

        #menu states
        self.game_paused = False
        self.paused_state = "main"

        
        #load images
        self.button_images = {'resume': pygame.image.load(r'assets\Buttons\resume.png').convert_alpha(),
                              'options': pygame.image.load(r'assets\Buttons\options.png').convert_alpha(),
                              'leaderboard': pygame.image.load(r'assets\Buttons\leaderboard.png').convert_alpha(),
                              'restart': pygame.image.load(r'assets\Buttons\restart.png').convert_alpha(),
                              'quit': pygame.image.load(r'assets\Buttons\quit.png').convert_alpha(),
                              }
        
        #button instances
        self.buttons_main = [Button(((WINDOW_WIDTH / 2), 120), self.button_images['resume'], 5), # scaled so img = 80 x 80
                         Button(((WINDOW_WIDTH / 2), 270), self.button_images['options'], 5),
                         Button(((WINDOW_WIDTH / 2), 420), self.button_images['leaderboard'], 5),
                         Button(((WINDOW_WIDTH / 2), 570), self.button_images['restart'], 5),
                         Button((WINDOW_WIDTH - 25, 25), self.button_images['quit'], 3)]  # scaled so img = 80 x 80]
        
        self.buttons_options = [Button(((WINDOW_WIDTH / 2), 120), self.button_images['resume'], 5)]
        
    def menu_state(self, surface): #should i make menu state a dictionary that then uses teh value in the dict to do things
        keys = pygame.key.get_just_pressed()
        if keys[pygame.K_ESCAPE] and self.game_paused == False :
            self.game_paused = True
            surface = pygame.transform.box_blur(surface, 2)#bluriong every frame then drawing on top every frame
            print(self.game_paused)
        elif keys[pygame.K_ESCAPE] and self.game_paused == True and self.paused_state == "main":
            self.game_paused = False
            print(self.game_paused) 
        elif keys[pygame.K_ESCAPE] and self.game_paused == True and self.paused_state != "main":
            self.paused_state = "main"
            print('back to main menu')
            print(self.paused_state)
            
            ##blur screen and make score stop, make player and enemy stop movement.
        self.actions()
             
            
    def actions(self):
        if self.game_paused == True:
            if self.paused_state == "main":
                if self.buttons_main[0].get_click():
                    print('resume')
                    self.game_paused = False
                    print(self.game_paused)
                    
                elif self.buttons_main[1].get_click():
                    self.paused_state = "options"
                    print(self.paused_state)
                    
                elif self.buttons_main[2].get_click():
                    self.paused_state = "leaderboard"
                    
                elif self.buttons_main[3].get_click():
                    pass #"restart"
                
                elif self.buttons_main[4].get_click():
                    pygame.quit()
                    sys.exit()

            else:
                pass

            if self.paused_state == "options":
                if self.buttons_main[0].get_click():
                    self.game_paused = False
                #slider for volume//input box


                
    def draw_text(self, text, colour, x, y, surface):
        img = self.font.render(text, True, colour)
        surface.blit(img, (x,y))
        
    def draw(self, surface):
        if self.paused_state == "main":
            for button in self.buttons_main:
                button.draw(surface)
        if self.paused_state == "options":
            for button in self.buttons_options:
                button.draw(surface)
                

    def clear(self, surface):
        pass
            
            

        