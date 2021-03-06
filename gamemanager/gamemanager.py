import pygame

from gamemanager import iomanager
from madness import mapstate
from madness import fighter
from madness import battlestate

class GameManager(object):
    
    def __init__(self):
        self.active = True
        pygame.init()
        pygame.font.init()
        self.ioManager = iomanager.IOManager('assets/config.cfg')
        #self.screenDims = (pygame.display.Info().current_w, pygame.display.Info().current_h)
        ## TODO: fix drawing so that it works at other resolultions
        self.screenDims = (1280,640)
        self.screen = pygame.display.set_mode(self.screenDims)
        self.gameStates = {'map' : mapstate.MapState(self.ioManager, self.screen)}
        self.fighter = fighter.Fighter(self.ioManager)
        self.state = 'map'

    def next_frame(self):
        self.gameStates[self.state].process_input()
        newState = self.gameStates[self.state].make_actions()
        self.gameStates[self.state].draw()
        if newState != self.state:
            self.state = newState
            if self.state == 'battle':
                self.gameStates['battle'] = battlestate.BattleState(self.screen, self.screenDims, self.ioManager, self.fighter)

    def close(self):
        pygame.display.quit()
