import pygame

class Player(object):
    def __init__(self, gameMap, startDims=(0,0)):
        self.map = gameMap
        self.dims = startDims
        self.goalDims = startDims # where the player is headed, can you come up with a better name?
        self.currMove = None
        self.lastMove = 0
        self.speed = 20 # px/frame

    def key_down(self, key):
        self.currMove = key
        
    def key_up(self, key):
        if self.currMove == key:
            self.currMove = None
        
    def move(self):
        if self.currMove and self.goalDims[0] == self.dims[0] and self.goalDims[1] == self.dims[1]:
            self.get_movement()
        if self.dims[0] < self.goalDims[0]:
            self.dims[0] += min(self.speed, self.goalDims[0]-self.dims[0])
        elif self.dims[0] > self.goalDims[0]:
            self.dims[0] += max(-self.speed, self.goalDims[0]-self.dims[0])
        elif self.dims[1] < self.goalDims[1]:
            self.dims[1] += min(self.speed, self.goalDims[1]-self.dims[1])
        elif self.dims[1] > self.goalDims[1]:
            self.dims[1] += max(-self.speed, self.goalDims[1]-self.dims[1])
  
    def get_movement(self):
        if self.currMove == pygame.K_LEFT:
            self.goalDims[0] += self.map.get_movement(self.dims, 'l')
        elif self.currMove == pygame.K_RIGHT:
            self.goalDims[0] += self.map.get_movement(self.dims, 'r')
        elif self.currMove == pygame.K_DOWN:
            self.goalDims[1] += self.map.get_movement(self.dims, 'd')
        elif self.currMove == pygame.K_UP:
            self.goalDims[1] +=  self.map.get_movement(self.dims, 'u')