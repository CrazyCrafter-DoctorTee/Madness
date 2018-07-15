import random
import time

class Enemy:
    def __init__(self, image, gameMap, startCords):
        self.image = image
        self.map = gameMap
        self.cords = startCords
        self.lastMove = time.time()

    def move(self):
        if time.time() > self.lastMove + 0.6:
            possibleMoves = ['l', 'r', 'u', 'd']
            for i in range(16): # 1% when one possible move
                choice = random.choice(possibleMoves)
                dist = self.map.get_movement(self.cords, choice)
                if dist != 0:
                    if  choice == 'l' or choice == 'r':
                        self.cords[0] += dist
                    elif choice == 'u' or choice == 'd':
                        self.cords[1] += dist
                    break
            self.lastMove = time.time()
