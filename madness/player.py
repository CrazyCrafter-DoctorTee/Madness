import pygame
import random

class Player(object):
    def __init__(self, gameMap, startDims=[0,0]):
        self.map = gameMap
        self.position = list(startDims)
        self.goalDims = list(startDims) # where the player is headed, can you come up with a better name?
        self.currMove = None
        self.lastMove = 0

    def key_down(self, key):
        self.currMove = key

    def key_up(self, key):
        if self.currMove == key:
            self.currMove = None

    def move(self):
        returnState = 'map'
        if self.currMove and self.goalDims[0] == self.position[0] and self.goalDims[1] == self.position[1]:
            self.get_movement()
        if self.position != self.goalDims:
            if self.map.on_exit(self.goalDims):
                returnState = None
            # 4% chance per movement of random encounter
            elif random.randrange(0, 1000) == 0:
                returnState = 'battle'
            
        if self.position[0] < self.goalDims[0]:
            self.position[0] += self.goalDims[0]-self.position[0]
        elif self.position[0] > self.goalDims[0]:
            self.position[0] += self.goalDims[0]-self.position[0]
        elif self.position[1] < self.goalDims[1]:
            self.position[1] += self.goalDims[1]-self.position[1]
        elif self.position[1] > self.goalDims[1]:
            self.position[1] += self.goalDims[1]-self.position[1]
  
        if returnState != 'map':
            # set current move to None, so player doesn't move when state becomes map again
            self.currMove = None
            
        return returnState

    def get_movement(self):
        if self.currMove == pygame.K_LEFT:
            self.goalDims[0] += self.map.get_movement(self.position, 'l')
        elif self.currMove == pygame.K_RIGHT:
            self.goalDims[0] += self.map.get_movement(self.position, 'r')
        elif self.currMove == pygame.K_DOWN:
            self.goalDims[1] += self.map.get_movement(self.position, 'd')
        elif self.currMove == pygame.K_UP:
            self.goalDims[1] +=  self.map.get_movement(self.position, 'u')
