import pygame
import configparser

import gamemap

def init_madness():
    images = {}
    maps = {}
    pygame.init()
    screen = pygame.display.set_mode((1280, 704))
    config = configparser.ConfigParser()
    config.read('game.cfg')
    for key in config['images']:
        print('Image:', key)
        images[key] = pygame.image.load(config['images'][key])

    for key in config['maps']:
        print('Map:', key)
        mapname = config['maps'][key]
        print(mapname)
        maps[key] = gamemap.GameMap(mapname, images)

    return screen, images, maps

def load_image(screen, image, row, col, scale=True):
    if scale:
        screen.blit(image, (col * 32, row * 32))
    else:
        screen.blit(image, (col, row))
