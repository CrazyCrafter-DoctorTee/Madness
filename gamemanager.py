import pygame

import iomanager
import gamemap
import enemy
import camera
import player

class GameManager(object):
    def __init__(self):
        self.active = True
        pygame.init()
        self.ioManager = iomanager.IOManager('assets/config.cfg')
        self.screenDims = self.ioManager.get_data('game', 'graphics', 'screendims')
        self.screen = pygame.display.set_mode(self.screenDims)
        self.init()
        self.player = player.Player(self.images['character']['player'], self.maps['start'])
        self.enemy = enemy.Enemy(self.images['character']['enemy'], self.maps['start'], self.screenDims)
        self.camera = camera.Camera(self.player, self.maps['start'], self.screenDims)

    def init(self):
        self.images = self.create_images(self.ioManager.get_data('images'))
        maps = self.ioManager.get_data('maps')
        self.maps = {}
        for name, attribs in maps.items():
            self.maps[name] = gamemap.GameMap(attribs['filename'],
                     self.images['map'], self.screen, attribs['tiledims'])
        
    def create_images(self, imageFiles):
        if type(imageFiles) == dict:
            images = {}
            for sec, value in imageFiles.items():
                images[sec] = self.create_images(value)
            return images
        else: 
            return pygame.image.load(imageFiles) # should only be one file

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