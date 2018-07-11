import pygame
import configparser
import time

import gamemap
import enemy
import player

class GameManager:
    def __init__(self):
        pygame.init()
        self.enemyLastMove = time.time()
        self.screen = pygame.display.set_mode((1280, 704))
        self.read_files()
        self.mapDims = (1280, 704)
        self.player = player.Player(self.images['player'], self.mapDims[0], self.mapDims[1])
        self.enemy = enemy.Enemy(self.images['enemy'], self.mapDims[0], self.mapDims[1])

    def read_files(self):
        self.images = {}
        self.maps = {}
        self.screen = pygame.display.set_mode((1280, 704))
        config = configparser.ConfigParser()
        config.read('assets/game.cfg')
        for key in config['images']:
            self.images[key] = pygame.image.load(config['images'][key])

        for key in config['maps']:
            self.maps[key] = gamemap.GameMap(config['maps'][key], self.images)

    def next_frame(self):
        self.process_input()
        if self.enemyLastMove // 1 != time.time() // 1:
            self.enemyLastMove = time.time()
            self.enemy.move()
        self.draw()

    def process_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.display.quit()
            if event.type == pygame.KEYDOWN:
                self.player.move(event.key)

    def draw(self):
        self.maps['start'].draw(self.screen, 0, 0, 40, 40) # TODO: make map move
        self.player.draw(self.screen)
        self.enemy.draw(self.screen)
        pygame.display.flip()
