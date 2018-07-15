import pygame

import mapstate
import iomanager

class GameManager(object):
    def __init__(self):
        self.active = True
        pygame.init()
        self.ioManager = iomanager.IOManager('assets/config.cfg')
        self.screenDims = self.ioManager.get_data('game', 'graphics', 'screendims')
        self.screen = pygame.display.set_mode(self.screenDims)
        self.gameState = mapstate.MapState(self.ioManager, self.screen)

    def next_frame(self):
        self.active = self.gameState.process_input()
        self.gameState.make_actions()
        self.gameState.draw()

    def draw(self):
        self.maps['start'].draw(self.screen, self.camera.offset)
        self.player.draw(self.screen, self.camera.offset)
        self.enemy.draw(self.screen, self.camera.offset)
        pygame.display.flip()

    def close(self):
        pygame.display.quit()