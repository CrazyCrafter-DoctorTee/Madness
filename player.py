import pygame
import time

import gamemap
import gameutils

class Player:
    def __init__(self, image, gameMap, x=0, y=0):
        self.image = image
        self.map = gameMap
        self.x, self.y = x, y
        self.goalX, self.goalY = x, y # where the player is headed, can you come up with a better name?
        self.currMove = None
        self.lastMove = 0
        self.speed = 5 # px/frame

    def key_down(self, key):
        self.currMove = key
        
    def key_up(self, key):
        if self.currMove == key:
            self.currMove = None
        
    def move(self):
        if self.currMove and self.goalX == self.x and self.goalY == self.y:
            self.get_movement()
        if self.x < self.goalX:
            self.x += min(self.speed, self.goalX-self.x)
        elif self.x > self.goalX:
            self.x += max(-self.speed, self.goalX-self.x)
        elif self.y < self.goalY:
            self.y += min(self.speed, self.goalY-self.y)
        elif self.y > self.goalY:
            self.y += max(-self.speed, self.goalY-self.y)
  
    def get_movement(self):
        if self.currMove == pygame.K_LEFT:
            self.goalX += self.map.get_movement(self.x, self.y, 'l')
        elif self.currMove == pygame.K_RIGHT:
            self.goalX += self.map.get_movement(self.x, self.y, 'r')
        elif self.currMove == pygame.K_DOWN:
            self.goalY += self.map.get_movement(self.x, self.y, 'd')
        elif self.currMove == pygame.K_UP:
            self.goalY +=  self.map.get_movement(self.x, self.y, 'u')

    def draw(self, screen, offset):
        x, y = self.x-offset[0], self.y-offset[1]
        gameutils.load_image(screen, self.image, x, y)
