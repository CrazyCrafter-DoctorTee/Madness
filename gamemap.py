import pygame

import gameutils

class GameMap:
    def __init__(self, filename, images, screen, tileDims=(32, 32)):
        self.filename = filename
        self.images = images
        self.screen = screen
        self.screenDims = pygame.display.get_surface().get_size()
        self.tileDims = tileDims
        self.generate_template()

    def generate_template(self):
        lines = []
        self.tiles = []
        with open(self.filename, 'r') as f:
           for line in f:
               lines.append(line)
        self.dims = tuple(int(d) for d in lines[0].split())
        self.maxX = self.dims[0] * self.tileDims[0]-self.tileDims[0] # add one tile buffer
        self.maxY = self.dims[1] * self.tileDims[1]-self.tileDims[1]
        for i in range(1, self.dims[0]+1):
            self.tiles.append(lines[i].split())

    def get_tile_dims(self, offset):
        x1 = offset[0]//self.tileDims[0]
        x2 = offset[0]//self.tileDims[0] + self.screenDims[0]//self.tileDims[0] + 1
        y1 = offset[1]//self.tileDims[1]
        y2 = offset[1]//self.tileDims[1] + self.screenDims[1]//self.tileDims[1] + 1
        return (x1, x2, y1, y2)

    def draw(self, screen, offset):
        # Arrays start at 1?
        x1, x2, y1, y2 = self.get_tile_dims(offset)
        startX = 0#(offset[0] // self.tileDims[0]) * self.tileDims[0]
        startY = 0#(offset[1] // self.tileDims[1]) * self.tileDims[1]
        printX  = startX-self.tileDims[0] # minus to cancel for later plus
        for i in range(x1, x2):
            printX += self.tileDims[0]
            printY = startY-self.tileDims[1]
            for j in range(y1, y2):
                printY += self.tileDims[1]
                gameutils.load_image(self.screen, self.images[self.tiles[j][i]],
                                     printX, printY)

    def can_move(self, x, y):
        # TODO: will determine if player can walk on tile
        return 1

    def get_movement(self, x, y, move):
        tileX, tileY = x//self.tileDims[0], y//self.tileDims[1]
        if move == 'l':
            if tileX <= 0:
                return 0
            return self.can_move(x-1, y) * -self.tileDims[0]
        elif move == 'r':
            if tileX >= (self.maxX-1)//self.tileDims[0]:
                return 0
            return self.can_move(x+1, y) * self.tileDims[0]
        elif move == 'u':
            if tileY <= 0:
                return 0
            return self.can_move(x, y-1) * -self.tileDims[1]
        elif move == 'd':
            if tileY >= (self.maxY-1)//self.tileDims[1]:
                return 0
            return self.can_move(x-1, y+1) * self.tileDims[1]
