from settings import pygame
from pygame.time import get_ticks

class Timer:
    def __init__(self, duration, func = None, repeat = False):
        self.duration = duration
        self.func = func
        self.start_time = 0
        self.active = False
        self.repeat = repeat

    def activate(self):
        #activate timer at start time
        self.active = True
        self.start_time = get_ticks()

    def deactivate(self):
        #deactivate timer, reset start time
        self.active = False
        self.start_time = 0
        if self.repeat:
            self.activate()

    def update(self):
        #update timer based on time elapsed
        current_time = get_ticks()
        if current_time - self.start_time >= self.duration:
            #check if the elapsed time is greater than or equal to teh duration
            if self.func and self.start_time != 0:
                self.func()
            self.deactivate()
