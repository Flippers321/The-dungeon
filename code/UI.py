from settings import *
import json

class Button:
    def __init__(self, pos, image, scale):
        width = image.get_width()
        height = image.get_width()
        #scaling
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect() #getting rect from the image
        self.rect.center = pos
        
    def draw(self, surface):
        surface.blit(self.image, (self.rect.x, self.rect.y))
        return False
    
    def get_click(self):
        #checking if button is clicked
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
        boldness = size[0] * 0.05 #slider thickness
        inner_scale = 2/3 #ratio of inner slider: outer slider rectangles
     
        #making the input pos the centre, calculating slider positions
        self.slider_left_pos = self.pos[0] - (size[0]//2)
        self.slider_right_pos = self.pos[0] + (size[0]//2)
        self.slider_top_pos = self.pos[1] - (size[1]//2)
        
        
        self.min = min
        self.max = max
        print('1',initial_val)
        self.initial_val =(size[0] * (initial_val / 100)) - 16 #initial slider position

        #creating the rectangles for slider
        self.container_rect = pygame.Rect(self.slider_left_pos, self.slider_top_pos, self.size[0], self.size[1])
        self.slider_rect = pygame.Rect(self.slider_left_pos + self.initial_val, self.slider_top_pos, boldness, self.size[1])
        self.slider_rect_inner = pygame.Rect(0, 0, boldness * inner_scale, self.size[1] * inner_scale)
        self.slider_rect_inner.center = self.slider_rect.center
        
    def get_click(self):
        #checking if slider is clicked
        pos = pygame.mouse.get_pos() 
        pressed = pygame.mouse.get_pressed()
        
        #checking if mouse is clicked on the containder
        if self.container_rect.collidepoint(pos):
            if pressed[0] == 1:
                self.move_slider(pos)
                print('clicked')
                return True

    def move_slider(self, mouse_pos):
        #moving slider to new mouse position
        self.slider_rect.centerx = mouse_pos[0]
        self.slider_rect_inner.centerx = mouse_pos[0]
    
    def draw(self, surface):
        pygame.draw.rect(surface, (30, 20, 18), self.container_rect)
        pygame.draw.rect(surface, (45, 35, 33), self.slider_rect)
        pygame.draw.rect(surface, (65, 55, 52), self.slider_rect_inner)
        
    def get_value(self):
        #calculate and return the current value of the slider 
       value_range = self.slider_right_pos - self.slider_left_pos -1 #pixel range, -1 allows user to easily go to lowest/highest value 
       slider_value = self.slider_rect.centerx - self.slider_left_pos #value range
       
       #Calculating value of the slider
       return(slider_value/value_range)*(self.max - self.min) + self.min
   
class InputBox:
    def __init__(self, pos, size, font, pressed_submit = None):
        self.keys = pygame.key.get_just_pressed()
        self.active = False
        self.input = '' #current text inputted
        self.pos = pos
        self.size = size
        self.pressed_submit = pressed_submit
        self.font = font
        
        #calcuating position of input box
        self.left_pos = self.pos[0] - (size[0]//2)
        self.top_pos = self.pos[1] - (size[1]//2)
        self.container_rect = pygame.Rect(self.left_pos, self.top_pos, self.size[0], self.size[1])
    def get_click(self):
        #checking if input box is clicked
        pos = pygame.mouse.get_pos()
        pressed = pygame.mouse.get_just_pressed()
        #checking if mouse is clicked on the containder
        if self.container_rect.collidepoint(pos):
            if pressed[0] == 1:
                self.active = True
                return True
        return False
    
    def update(self):
        #updating the input box, returning the 'input'(username) into the server
        self.get_click() 
        if self.active == True:
            if len(self.input) < 8:
                for i in range(pygame.K_a, pygame.K_z):
                    if pygame.key.get_just_pressed()[i]:
                        self.input += chr(i).upper() #making every letter uppercase
                for i in range (pygame.K_0, pygame.K_9):
                    if pygame.key.get_just_pressed()[i]:
                        self.input += chr(i)
            #allowing player to backspace and deactivate input even if max length is reached
            if pygame.key.get_just_pressed()[pygame.K_BACKSPACE]:
                self.input = self.input[:-1]                        
            if self.keys[pygame.K_RETURN]:
                self.active = False
        return self.input
                    
    def draw(self, screen):
        pygame.draw.rect(screen, (30, 20, 18), self.container_rect)
        text_surface = self.font.render(self.input, True, (255, 255, 255))
        screen.blit(text_surface, (self.left_pos + 5, self.top_pos + 5))                           
            
        
class Menu:
    def __init__(self):
        
        self.font = pygame.font.Font(r'assets\Perfect DOS VGA 437.ttf', 16)

        #menu states and variables
        self.game_paused = False
        self.submit = False
        self.restart = False
        self.reload_scores = False
        self.paused_state = "main"
        self.default_settings = {'volume': 0.5}
        self.new_setting = {'new_volume': 0}
        
        #load images
        self.button_images = {
            'resume': pygame.image.load(r'assets\Buttons\resume.png').convert_alpha(),
            'options': pygame.image.load(r'assets\Buttons\options.png').convert_alpha(),
            'leaderboard': pygame.image.load(r'assets\Buttons\leaderboard.png').convert_alpha(),
            'restart': pygame.image.load(r'assets\Buttons\restart.png').convert_alpha(),
            'quit': pygame.image.load(r'assets\Buttons\quit.png').convert_alpha(),
            'submit': pygame.image.load(r'assets\Buttons\submit.png').convert_alpha()
            }
        
        #UI element instances
        self.buttons_main = [
            Button(((WINDOW_WIDTH / 2), 120), self.button_images['resume'], 5),
            Button(((WINDOW_WIDTH / 2), 270), self.button_images['options'], 5),
            Button(((WINDOW_WIDTH / 2), 420), self.button_images['leaderboard'], 5),
            Button(((WINDOW_WIDTH / 2), 570), self.button_images['restart'], 5),
            Button((WINDOW_WIDTH - 25, 25), self.button_images['quit'], 3)
            ]  
        
        self.buttons_options = [
            Button(((WINDOW_WIDTH / 2), 120), self.button_images['resume'], 5),
            Button((WINDOW_WIDTH - 25, 25), self.button_images['quit'], 3)
            ]
        self.sliders = [
            Slider(((WINDOW_WIDTH / 2), 420), (600, 40), self.load_settings('volume'), 0, 100)
            ]
        
        self.buttons_leaderboard = [
            Button(((WINDOW_WIDTH / 2), 120), self.button_images['resume'], 5),
            Button(((WINDOW_WIDTH - 25), 25), self.button_images['quit'], 3)
            ]
        
        self.buttons_win = [
            Button(((WINDOW_WIDTH - 25), 25), self.button_images['quit'], 3),
            Button(((WINDOW_WIDTH / 2), 150), self.button_images['submit'], 5)
            ]
        
        self.win_input = [
            InputBox(((WINDOW_WIDTH // 2), WINDOW_HEIGHT /2), (100, 25), self.font)
            ]

    def load_settings(self, setting):
        #loading settings from config file
        with open("code\config.json", "r") as c:
            data = json.load(c)
            value = data.get(setting)
            return(value)
                   
    def save_settings(self):
        #saving settings to confi file
        with open("code\config.json", "w") as c:
            value = c.write(json.dumps({'volume': round(self.sliders[0].get_value())}))
            print("SAVING", value)
            print('save', json.dumps({'volume': self.sliders[0].get_value()}))
    
    def menu_state(self, level_count): 
        #handles menu state transitions based on input
        keys = pygame.key.get_just_pressed()
        if level_count != 2:
            if keys[pygame.K_ESCAPE] and self.game_paused == False :
                self.game_paused = True
                print(self.game_paused)
            elif keys[pygame.K_ESCAPE] and self.game_paused == True and self.paused_state == "main":
                self.game_paused = False
                print(self.game_paused) 
            elif keys[pygame.K_ESCAPE] and self.game_paused == True and self.paused_state != "main":
                self.paused_state = "main"
                print('back to main menu')
        if level_count == 2:
            if keys[pygame.K_ESCAPE]:
                self.game_paused = True
                self.paused_state = "win"
            
    def paused_actions(self):
        #handles actions when the game is paused
        if self.game_paused:
            if self.paused_state == "main":
                if self.buttons_main[0].get_click():
                    print('resume')
                    self.game_paused = False
                    print(self.game_paused)       
                elif self.buttons_main[1].get_click():
                    self.paused_state = "options"
                elif self.buttons_main[2].get_click():
                    self.paused_state = "leaderboard"
                elif self.buttons_main[3].get_click():
                    self.restart = True
                    self.game_paused = False
                elif self.buttons_main[4].get_click():
                    pygame.quit()
                    sys.exit()
                
                #state functions
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
        
    def win_actions(self):
        #handles actions when player wins
        self.win_input[0].update()
        if self.game_paused == True:
            if self.paused_state == 'win':
                if self.buttons_win[0].get_click():
                    pygame.quit()
                    sys.exit()
                if self.buttons_win[1].get_click():
                    self.submit = True
                    self.game_paused = False ####
                    
                
    def draw_text(self, text, colour, x, y, surface, size = 16):
        #handles drawing text onto the screen
        self.font = pygame.font.Font(r'assets\Perfect DOS VGA 437.ttf', size)
        text_offset = (len(text)*8 //2) # centering words when more characters are added
        img = self.font.render(text, True, colour)
        surface.blit(img, (x - text_offset,y))
        
    def draw(self, surface, level_count):
        #handles drawing the menu onto the screen
        if level_count !=2:           
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
                for button in self.buttons_leaderboard:
                    button.draw(surface)               
        else:         
            for button in self.buttons_win:
                button.draw(surface)
            for textbox in self.win_input: 
                textbox.draw(surface)                 

                
            

                        

        