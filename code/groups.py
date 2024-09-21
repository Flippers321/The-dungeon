from settings import *

#recreating drawing logic (sprite group) to make it more customisable 
class AllSprites(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surf = pygame.display.get_surface()
        self.offset = vector(0, 0)
        
    def draw(self, target_pos):
        #camera pos
        self.offset.x = -(target_pos[0] - WINDOW_WIDTH / 2)
        self.offset.y = -(target_pos[1] - WINDOW_HEIGHT / 2)
        
        for sprite in self:
            offset_pos = sprite.rect.topleft + self.offset
            self.display_surf.blit(sprite.image, offset_pos)