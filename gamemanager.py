import pygame

import mapstate
import iomanager
import fighter
import battlestate

class GameManager(object):
    def __init__(self):
        self.active = True
        pygame.init()
        pygame.font.init()
        self.ioManager = iomanager.IOManager('assets/config.cfg')
        #self.screenDims = (pygame.display.Info().current_w, pygame.display.Info().current_h)
        ## TODO: fix drawing so that it works at other resolultiojs
        self.screenDims = (1270,695)
        self.screen = pygame.display.set_mode(self.screenDims)
        self.gameStates = {'map' : mapstate.MapState(self.ioManager, self.screen)}
        self.fighter = fighter.Fighter(self.ioManager)
        self.state = 'map'

    def next_frame(self):
        state = self.gameStates[self.state].process_input()
        self.gameStates[self.state].make_actions()
        self.gameStates[self.state].draw()
        if state != self.state:
            self.state = state
            if self.state == 'battle':
                self.gameStates['battle'] = battlestate.BattleState(self.screen, self.screenDims, self.ioManager, self.fighter)

    def draw(self):
        self.maps['start'].draw(self.screen, self.camera.offset)
        self.player.draw(self.screen, self.camera.offset)
        self.enemy.draw(self.screen, self.camera.offset)
        pygame.display.flip()

    def close(self):
        pygame.display.quit()
