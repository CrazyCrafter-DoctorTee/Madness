import pygame
import configparser
import time

import gamemap
import enemy
import camera
import player

class GameManager:
    def __init__(self):
        self.active = True
        pygame.init()
        self.read_files()
        self.mapDims = (1280, 704)
        self.player = player.Player(self.images['player'], self.maps['start'], 0, 0)
        self.enemy = enemy.Enemy(self.images['enemy'], self.maps['start'], self.mapDims)
        self.camera = camera.Camera(self.player, self.maps['start'], self.graphics['screendims'])

    def read_files(self):
        self.images = {}
        self.maps = {}
        self.graphics = {}
        config = configparser.ConfigParser()
        config.read('assets/game.cfg')
        #initialize graphics settings first
        for key in config['graphics']:
            self.graphics[key] = [int(x) for x in config['graphics'][key].split(',')]
        self.screen = pygame.display.set_mode(self.graphics['screendims'])
        #now we can do the rest of the config reading
        for key in config['images']:
            self.images[key] = pygame.image.load(config['images'][key])
        for key in config['maps']:
            self.maps[key] = gamemap.GameMap(config['maps'][key], self.images, self.screen, self.graphics['tiledims'])


    def next_frame(self):
        self.process_input()
        self.player.move()
        self.camera.find_offset()
        self.enemy.move()
        self.draw()

    def process_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.active = False
            if event.type == pygame.KEYDOWN:
                self.player.key_down(event.key)
            if event.type == pygame.KEYUP:
                self.player.key_up(event.key)

    def draw(self):
        self.maps['start'].draw(self.screen, self.camera.offset)
        self.player.draw(self.screen, self.camera.offset)
        self.enemy.draw(self.screen, self.camera.offset)
        pygame.display.flip()

    def close(self):
        pygame.display.quit()