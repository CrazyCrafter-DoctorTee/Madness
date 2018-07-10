import random

from gameutils import *

class Enemy:
    def __init__(self, image, maxRow, maxCol):
        self.image = image
        self.maxRow = maxRow
        self.maxCol = maxCol
        self.row = random.randrange(1,15)
        self.col = random.randrange(1,15)
        
    def move(self):
        possibleMoves = []
        if self.row > 0:
            possibleMoves.append('u')
        if self.row < self.maxRow - 1:
            possibleMoves.append('d')
        if self.col > 0:
            possibleMoves.append('l')
        if self.col < self.maxCol - 1:
            possibleMoves.append('r')
        move = random.choice(possibleMoves)
        if move == 'u':
            self.row -= 1
        if move == 'd':
            self.row += 1
        if move == 'l':
            self.col -= 1
        if move == 'r':
            self.col += 1
            
    def draw(self, screen):
        load_image(screen, self.image, self.row, self.col)