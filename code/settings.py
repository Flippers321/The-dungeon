import pygame, sys 
from pygame.math import Vector2 as vector


WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
FPS = 60
TILE_SIZE = 16
ANIMATION_SPEED = 6
#layers 
Z_LAYERS = {
    'climbing chains': 0,
    'gem' : 1,
    'background obj': 2,
    'chains': 3,
    'spikes': 4,
    'default': 5,
    
}
