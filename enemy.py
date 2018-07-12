import random
import time

import gameutils

class Enemy:
    def __init__(self, image, gameMap, startCords):
        self.image = image
        self.map = gameMap
        self.x = startCords[0]
        self.y = startCords[1]
        self.lastMove = time.time()

    def move(self):
        if time.time() > self.lastMove + 0.6:
            possibleMoves = ['l', 'r', 'u', 'd']
            for i in range(16): # 1% when one possible move
                choice = random.choice(possibleMoves)
                dist = self.map.get_movement(self.x, self.y, choice)
                if dist != 0:
                    if  choice == 'l' or choice == 'r':
                        self.x += dist
                    elif choice == 'u' or choice == 'd':
                        self.y += dist
                    break
            self.lastMove = time.time()


    def draw(self, screen, offset):
        x, y = self.x-offset[0], self.y-offset[1]
        gameutils.load_image(screen, self.image, x, y)
