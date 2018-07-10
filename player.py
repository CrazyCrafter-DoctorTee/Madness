import pygame

import gameutils

class Player:
    def __init__(self, image, maxRow, maxCol):
        self.image = image
        self.maxRow = maxRow
        self.maxCol = maxCol
        self.row = 0
        self.col = 0        
    
    def move(self, key):
        if key == pygame.K_LEFT:
            self.col -= 1 if self.col != 0 else 0
        if key == pygame.K_RIGHT:
            self.col += 1 if self.col < self.maxCol - 1 else 0
        if key == pygame.K_DOWN:
            self.row += 1 if self.row < self.maxRow - 1 else 0
        if key == pygame.K_UP:
            self.row -= 1 if self.row != 0 else 0
            
    def draw(self, screen):
        gameutils.load_image(screen, self.image, self.row, self.col)