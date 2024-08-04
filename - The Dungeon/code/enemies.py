from settings import *

class slime(pygame.sprite.Sprite):
    def __init__(self, pos, groups, collision_sprites):
        super().__init__(groups)
        self.image = pygame.Surface((16,16))
        self.image.fill('green')

        self.rect = self.image.get_frect(topleft = pos)
        self.old_rect = self.rect.copy()