import pygame

import battlestate
import fighter
import mapstate
import iomanager

class GameManager(object):
    def __init__(self):
        self.active = True
        pygame.init()
        self.ioManager = iomanager.IOManager('assets/config.cfg')
        self.screenDims = self.ioManager.get_data('game', 'graphics', 'screendims')
        self.screen = pygame.display.set_mode(self.screenDims)
        self.fighter = fighter.Fighter(self.ioManager)
        self.gameStates = {'map' : mapstate.MapState(self.ioManager, self.screen)}
        self.state = 'map'

    def next_frame(self):
        state = self.gameStates[self.state].process_input()
        self.gameStates[self.state].make_actions()
        self.gameStates[self.state].draw()
        if state != self.state:
            self.state = state
            if self.state == 'battle':
                self.gameStates['battle'] == battlestate.BattleState(self.screen, self.fighter, None)

    def draw(self):
        self.maps['start'].draw(self.screen, self.camera.offset)
        self.player.draw(self.screen, self.camera.offset)
        self.enemy.draw(self.screen, self.camera.offset)
        pygame.display.flip()

    def close(self):
        pygame.display.quit()