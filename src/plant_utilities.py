import pygame
from math import sqrt
from enum import Enum

class mode(Enum):
    LIGHT = 0
    WATER = 1
    VOC = 2

# define colors
BLACK = 0,0,0
WHITE = 255,255,255
GRAY = 100,100,100
BLUE = 0,0,255
CYAN = 0,255,255
RED = 255,0,0
ORANGE = 255,165,0
PURPLE = 128,0,128

def world_to_screen(x, y, MAX_X, MAX_Y, SCREEN_SIZE):
    """
        convert a set of x and y coordinates relative to the world
        into a set of x and y coordinates relative to the screen

        Args:
            x, y (floats): coordinates relative to the world
            MAX_X, MAX_Y (floats): Top bound to world coordinate system
            SCREEN_SIZE (tuple): Size of screen being drawn to
        
        Returns:
            x_draw, y_draw (tuple: int): coordinates relative to the screen 
        """
    x_draw = int((x/MAX_X)*SCREEN_SIZE[0])
    y_draw = int((y/MAX_Y)*SCREEN_SIZE[1])
    return [x_draw, y_draw]

def tint(sprite, tint_color):
    cp = sprite.copy()
    cp.fill(tint_color, special_flags=pygame.BLEND_ADD)
    return cp

def dist(x1, y1, x2, y2):
    return sqrt((x1-x2)**2 + (y1-y2)**2)

