import pygame

class Button:
    def __init__(self, keytype, x1, x2, y1, y2):
        sef.keytype = keytype
        self.lx = x1
        self.ly = y1
        self.ux = x2
        self.uy = y2

    def update(self, mx, my):
        if self.lx < mx < self.ux:
            if self.ly < my < self.uy:
                return self.keytype
        return 0
