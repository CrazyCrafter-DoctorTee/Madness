import pygame
import time

from gameutils import *
from player import Player
from enemy import Enemy
from math import floor
from gamemap import GameMap

if __name__ == '__main__':

    lastMove = floor(time.time())
    screen, images, maps = init_madness()
    player = Player(images['player'], 16, 16)
    enemy = Enemy(images['enemy'], 16, 16)

    while 'gary':
        maps['start'].draw(screen)
        player.draw(screen)
        enemy.draw(screen)
        if lastMove != floor(time.time()):
            enemy.move()
            lastMove = floor(time.time())
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.display.quit()
            if event.type == pygame.KEYDOWN:
                player.move(event.key)
