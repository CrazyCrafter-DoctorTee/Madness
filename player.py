import pygame
import time

import gamemap
import gameutils

class Player:
    def __init__(self, image, gameMap, x=0, y=0):
        self.image = image
        self.map = gameMap
        self.x = x
        self.y = y
        self.currMove = None
        self.lastMove = 0

    def key_down(self, key):
        self.currMove = key
        
    def move(self):
        if time.time() > self.lastMove + 0.3:
            print(self.currMove)
            if self.currMove == pygame.K_LEFT:
                self.x += self.map.get_movement(self.x, self.y, 'l')
            elif self.currMove == pygame.K_RIGHT:
                self.x += self.map.get_movement(self.x, self.y, 'r')
            elif self.currMove == pygame.K_DOWN:
                self.y += self.map.get_movement(self.x, self.y, 'd')
            elif self.currMove == pygame.K_UP:
                self.y +=  self.map.get_movement(self.x, self.y, 'u')
            self.lastMove = time.time()
            
    def key_up(self, key):
        if self.currMove == key:
            self.currMove = None

    def draw(self, screen, offset):
        x, y = self.x-offset[0], self.y-offset[1]
        gameutils.load_image(screen, self.image, x, y)
