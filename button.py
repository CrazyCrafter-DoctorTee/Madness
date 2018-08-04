import pygame
class Button:
    def __init__(self, keytype, x, y, height, width):
        sef.keytype = keytype
        self.lx = x
        self.ly = y
        self.ux = x + width
        self.uy = x + height

    def update(self, mx, my):
        if self.lx < mx < self.ux:
            if self.ly < my < self.uy:
                return self.keytype
        return 0
