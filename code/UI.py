from settings import *
import json

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
        pressed = pygame.mouse.get_just_pressed()
        
        #checking if mouse is clicked on a button
        if self.rect.collidepoint(pos):
            if pressed[0] == 1:
                return True
            

class Slider:
    def __init__(self, pos, size, initial_val, min, max):
        self.pos = pos
        self.size = size
        boldness = size[0] * 0.05
        inner_scale = 2/3
     
        #making the input pos the centre
        self.slider_left_pos = self.pos[0] - (size[0]//2)
        self.slider_right_pos = self.pos[0] + (size[0]//2)
        self.slider_top_pos = self.pos[1] - (size[1]//2)
        
        self.min = min
        self.max = max
        print('1',initial_val)
        self.initial_val =(size[0] * (initial_val / 100)) - 16
        print('3', self.initial_val)

        
        self.container_rect = pygame.Rect(self.slider_left_pos, self.slider_top_pos, self.size[0], self.size[1])
        self.slider_rect = pygame.Rect(self.slider_left_pos + self.initial_val, self.slider_top_pos, boldness, self.size[1])
        self.slider_rect_inner = pygame.Rect(0, 0, boldness * inner_scale, self.size[1] * inner_scale)
        self.slider_rect_inner.center = self.slider_rect.center
        
    def get_click(self):
        pos = pygame.mouse.get_pos()
        pressed = pygame.mouse.get_pressed()
        
        #checking if mouse is clicked on the containder
        if self.container_rect.collidepoint(pos):
            if pressed[0] == 1:
                self.move_slider(pos)
                print('clicked')
                return True

    def move_slider(self, mouse_pos):
        self.slider_rect.centerx = mouse_pos[0]
        self.slider_rect_inner.centerx = mouse_pos[0]
    
    def draw(self, surface):
        pygame.draw.rect(surface, (30, 20, 18), self.container_rect)
        pygame.draw.rect(surface, (45, 35, 33), self.slider_rect)
        pygame.draw.rect(surface, (65, 55, 52), self.slider_rect_inner)
        
    def get_value(self):
       value_range = self.slider_right_pos - self.slider_left_pos -1 #pixel range, -1 allows user to easily go to lowest/highest value 
       slider_value = self.slider_rect.centerx - self.slider_left_pos #value range
       
       #getting value of the slider
       return(slider_value/value_range)*(self.max - self.min) + self.min
   
class InputBox:
    def __init__(self, pos, size, font, pressed_submit = None):
        #self.keys = pygame.key.get_just_pressed()
        self.active = False
        self.input = ''
        self.pos = pos
        self.size = size
        self.pressed_submit = pressed_submit
        self.font = font
        
        self.left_pos = self.pos[0] - (size[0]//2)
        self.top_pos = self.pos[1] - (size[1]//2)
        
    def get_click(self):
        pos = pygame.mouse.get_pos()
        pressed = pygame.mouse.get_pressed()
        
        #checking if mouse is clicked on the containder
        if self.container_rect.collidepoint(pos):
            if pressed[0] == 1:
                self.active = True
        else:
            self.active = False
    
    def update(self):
        if self.active:
            for i in range(pygame.K_a, pygame.K_z):
                if pygame.key.get_just_pressed()[i]:
                    self.input += chr(i).upper()
            for i in range (pygame.K_0, pygame.K_9):
                if pygame.key.get_just_pressed()[i]:
                    self.input += chr(i)
            if self.keys[pygame.K_SPACE]:
                self.input += ' '
            if self.keys[pygame.K_BACKSPACE]:
                self.input = self.input[:-1]
            if self.keys[pygame.K_RETURN]:
                self.active = False
                if self.pressed_submit:
                    self.pressed_submit(self.input)
                    
    def draw(self, screen):
        self.container_rect = pygame.Rect(self.left_pos, self.top_pos, self.size[0], self.size[1])
        pygame.draw.rect(screen, (30, 20, 18), self.container_rect)
        
        text_surface = self.font.render(self.input, True, (255, 255, 255))
        screen.blit(text_surface, (self.left_pos + 5, self.top_pos + 5))                    
                                   
   
class Highscore:
    def __init__(self, user, score):
        pass
            #         #leaderboard functions
            # if self.paused_state == "leaderboard":
            #     if self.buttons_leaderboard[0].get_click():
            #         self.paused_state = "main"
            #         self.game_paused = False
            #         print(self.paused_state)
            #     if self.buttons_leaderboard[1].get_click():
            #         pygame.quit()
            #         sys.exit()
                
                
            #     #submitting highscore
            # if self.win_input[0].input!= '' and self.win_input[0].input.isalpha():       
            
        
class Menu:
    def __init__(self):
        
        
        self.font = pygame.font.Font(r'assets\Perfect DOS VGA 437.ttf', 16)

        #menu states
        self.game_paused = False
        self.submition_level = False
        self.paused_state = "main"
        self.default_settings = {'volume': 0.5}
        self.new_setting = {'new_volume': 0}
        
        #load images
        self.button_images = {'resume': pygame.image.load(r'assets\Buttons\resume.png').convert_alpha(),
                              'options': pygame.image.load(r'assets\Buttons\options.png').convert_alpha(),
                              'leaderboard': pygame.image.load(r'assets\Buttons\leaderboard.png').convert_alpha(),
                              'restart': pygame.image.load(r'assets\Buttons\restart.png').convert_alpha(),
                              'quit': pygame.image.load(r'assets\Buttons\quit.png').convert_alpha(),
                              'submit': pygame.image.load(r'assets\Buttons\submit.png').convert_alpha()
                              }
        
        #button instances
        self.buttons_main = [Button(((WINDOW_WIDTH / 2), 120), self.button_images['resume'], 5), # scaled so img = 80 x 80
                         Button(((WINDOW_WIDTH / 2), 270), self.button_images['options'], 5),
                         Button(((WINDOW_WIDTH / 2), 420), self.button_images['leaderboard'], 5),
                         Button(((WINDOW_WIDTH / 2), 570), self.button_images['restart'], 5),
                         Button((WINDOW_WIDTH - 25, 25), self.button_images['quit'], 3)]  # scaled so img = 80 x 80]
        
        self.buttons_options = [Button(((WINDOW_WIDTH / 2), 120), self.button_images['resume'], 5),
                                Button((WINDOW_WIDTH - 25, 25), self.button_images['quit'], 3)]
        self.sliders = [Slider(((WINDOW_WIDTH / 2), 420), (600, 40), self.load_settings('volume'), 0, 100)]
        
        self.buttons_leaderboard = [Button(((WINDOW_WIDTH / 2), 120), self.button_images['resume'], 5),
                                    Button(((WINDOW_WIDTH - 25), 25), self.button_images['quit'], 3)]
        self.buttons_win = [Button(((WINDOW_WIDTH - 25), 25), self.button_images['quit'], 3),
                            Button(((WINDOW_WIDTH / 2), 120), self.button_images['submit'], 5)]
        
        self.win_input = [InputBox(((WINDOW_WIDTH // 2), WINDOW_HEIGHT /2), (100, 50), self.font)]
                                    
                ##maybe add an altering to SCREEN_WIDTH/HEIGHT
        ## top fo vertical, just make taller than wide and change y to be mouse y instead
        ## write to a file with last value ad make that the initial value nect time func


    def load_settings(self, setting): #will be used in level.py
          
         with open("code\config.json", "r") as c:
             data = json.load(c)
             #if data == '':
             #    self(self.default_settings)
             value = data.get(setting)
             #print('val', value)S
             return(value)
                   
    def save_settings(self):
         with open("code\config.json", "w") as c:
             value = c.write(json.dumps({'volume': round(self.sliders[0].get_value())}))
             print("SAVING", value)
             print('save', json.dumps({'volume': self.sliders[0].get_value()}))
             
        
        
    def menu_state(self): #should i make menu state a dictionary that then uses teh value in the dict to do things
        keys = pygame.key.get_just_pressed()
        if keys[pygame.K_ESCAPE] and self.game_paused == False :
            self.game_paused = True
            print(self.game_paused)
        elif keys[pygame.K_ESCAPE] and self.game_paused == True and self.paused_state == "main":
            self.game_paused = False
            print(self.game_paused) 
        elif keys[pygame.K_ESCAPE] and self.game_paused == True and self.paused_state != "main":
            self.paused_state = "main"
            print('back to main menu')
             
    def check_final_level(self):
        print('should be true')
        self.game_paused = True #this not pausing game???
        print(self.game_paused) 
        return True
        
    ##maybe do another function for the win state
            
    def actions(self):
        if self.game_paused == True:
            print(self.sliders[0].get_value())
            if self.paused_state == "main":
                if self.buttons_main[0].get_click():
                    print('resume')
                    self.game_paused = False
                    print(self.game_paused)
                    
                elif self.buttons_main[1].get_click():
                    self.paused_state = "options"
                    #print(self.paused_state)
               
                    
                elif self.buttons_main[2].get_click():
                    self.paused_state = "leaderboard"
                    
                elif self.buttons_main[3].get_click():
                    self.game_paused = False
                    #self.paused_state = "main"
                
                elif self.buttons_main[4].get_click():
                    pygame.quit()
                    sys.exit()
                
                #options functions
            if self.paused_state == "options":
                if self.buttons_options[0].get_click():
                    self.paused_state = "main"
                    self.game_paused = False
                if self.buttons_options[1].get_click():
                    pygame.quit()
                    sys.exit()   
                self.sliders[0].get_click()
                self.save_settings()
                self.volume = self.sliders[0].get_value()
                
            if self.paused_state == "leaderboard":
                if self.buttons_leaderboard[0].get_click():
                    self.paused_state = "main"
                if self.buttons_leaderboard[1].get_click():
                    pygame.quit()
                    sys.exit()  
        
            if self.paused_state == 'win':
                print('here')
                if self.buttons_win[0].get_click():
                    pygame.quit()
                    sys.exit()
                if self.buttons_win[1].get_click():
                    pass
        
        #print(self.paused_state)
                    ##Highscore.submit
                
    def draw_text(self, text, colour, x, y, surface):
        text_offset = (len(text)*8 //2) # centering words when more characters are added
        img = self.font.render(text, True, colour)
        surface.blit(img, (x - text_offset,y))
        
    def draw(self, surface):           
        if self.game_paused == True:
            surface.fill(BACKGROUND_COLOUR)
        if self.paused_state == "main":
            for button in self.buttons_main:
                button.draw(surface)
        if self.paused_state == "options":
            for button in self.buttons_options:
                button.draw(surface)
            for slider in self.sliders:
                slider.draw(surface)
        if self.paused_state == 'leaderboard':
            for button in self.buttons_leaderboard: #sharing a button with 'main'
                button.draw(surface)
            for textbox in self.win_input: #thsi becoms a table of highscores
                textbox.draw(surface)               
                
        if self.paused_state == 'win':
            surface.fill(BACKGROUND_COLOUR)
            print('should be filling')            
            for button in self.buttons_win:
                button.draw(surface)
            for textbox in self.win_input: #sharing a text
                textbox.draw(surface)                 

                
            

                        

        