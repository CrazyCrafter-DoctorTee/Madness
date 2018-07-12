import pygame

import gamemap
import gameutils

class Player:
    def __init__(self, image, gameMap, x=0, y=0):
        self.image = image
        self.map = gameMap
        self.x = x
        self.y = y

    def move(self, key):
        if key == pygame.K_LEFT:
            self.x += self.map.get_movement(self.x, self.y, 'l')
        elif key == pygame.K_RIGHT:
            self.x += self.map.get_movement(self.x, self.y, 'r')
        elif key == pygame.K_DOWN:
            self.y += self.map.get_movement(self.x, self.y, 'd')
        elif key == pygame.K_UP:
            self.y +=  self.map.get_movement(self.x, self.y, 'u')
        print(self.x, self.y)

    def draw(self, screen, offset):
        x, y = self.x-offset[0], self.y-offset[1]
        gameutils.load_image(screen, self.image, x, y)
