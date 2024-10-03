from settings import *

#recreating drawing logic (sprite group) to make it more customisable 
class AllSprites(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surf = pygame.display.get_surface()
        self.offset = vector(0, 0)
        
class CameraGroup(AllSprites):
    def __init__(self):
        # camera offset 
        super().__init__()
        self.offset = vector()
        self.half_w = self.display_surf.get_size()[0] // 2
        self.half_h = self.display_surf.get_size()[1] // 2

        # box setup
        self.camera_borders = {'left': 400, 'right': 400, 'top': 250, 'bottom': 250}
        l = self.camera_borders['left']
        t = self.camera_borders['top']
        w = self.display_surf.get_size()[0]  - (self.camera_borders['left'] + self.camera_borders['right'])
        h = self.display_surf.get_size()[1]  - (self.camera_borders['top'] + self.camera_borders['bottom'])
        self.camera_rect = pygame.Rect(l,t,w,h)

    def box_camera(self,target):

        if target.rect.left < self.camera_rect.left:
            self.camera_rect.left = target.rect.left
        if target.rect.right < self.camera_rect.right:
            self.camera_rect.right = target.rect.right
        if target.rect.top > self.camera_rect.top:
            self.camera_rect.top = target.rect.top
        if target.rect.bottom < self.camera_rect.bottom:
            self.camera_rect.bottom = target.rect.bottom

        self.offset.x = self.camera_rect.left - self.camera_borders['left']
        self.offset.y = self.camera_rect.top - self.camera_borders['top']

    def draw(self, player):
        self.box_camera(player)

        #active screen elements
        for sprite in self:
            offset_pos = sprite.rect.topleft + self.offset
            print(self.display_surf)
            self.display_surf.blit(sprite.image, offset_pos)

    #def draw(self, target_pos):
        #camera pos
        #self.offset.x = -(target_pos[0] - WINDOW_WIDTH / 2)
        #self.offset.y = -(target_pos[1] - WINDOW_HEIGHT / 2)
        
