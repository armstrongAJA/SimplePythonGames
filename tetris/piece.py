import sys
import pygame
import random
import globalVariables as mn

class piece():
    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = random.choice(mn.COLORS)
        self.rotation = 0
