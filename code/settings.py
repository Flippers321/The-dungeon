import pygame, sys
from pygame.math import Vector2 as vector
import pygame.geometry


WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
FPS = 60
TILE_SIZE = 16
ANIMATION_SPEED = 6
BACKGROUND_COLOUR = (38, 28, 26)
#layers 
Z_LAYERS = {
    'climbing chains': 0,
    'gem' : 1,
    'background obj': 2,
    'chains': 3,
    'spikes': 4,
    'entity': 5,
}
