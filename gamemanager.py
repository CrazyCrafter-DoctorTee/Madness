import pygame

import iomanager
import gamemap
import enemy
import camera
import player

class GameManager:
    def __init__(self):
        pygame.init()
        self.ioManager = iomanager.IOManager('asserts/game.cfg')
        self.mapDims = (1280, 704)
        self.screen = pygame.display.set_mode(self.graphics['screendims'])
        self.player = player.Player(self.images['player'], self.maps['start'])
        self.enemy = enemy.Enemy(self.images['enemy'], self.maps['start'], self.mapDims)
        self.camera = camera.Camera(self.player, self.maps['start'], self.graphics['screendims'])

    def next_frame(self):
        self.process_input()
        self.camera.find_offset()
        self.enemy.move()
        self.draw()

    def process_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.display.quit()
            if event.type == pygame.KEYDOWN:
                self.player.move(event.key)

    def draw(self):
        self.maps['start'].draw(self.screen, self.camera.offset)
        self.player.draw(self.screen, self.camera.offset)
        self.enemy.draw(self.screen, self.camera.offset)
        pygame.display.flip()
