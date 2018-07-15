class GameMap(object):
    def __init__(self, filename, tileDims=(32, 32)):
        self.tileDims = tileDims
        self.template = self.generate_template(filename)

    def generate_template(self, filename):
        lines = []
        self.tiles = []
        with open(filename, 'r') as f:
           for line in f:
               lines.append(line)
        self.dims = tuple(int(d) for d in lines[0].split())
        maxX = self.dims[0]*self.tileDims[0] - self.tileDims[0]
        maxY = self.dims[1]*self.tileDims[1] - self.tileDims[1]
        self.maxDims = (maxX, maxY)
        for i in range(1, self.dims[0]+1):
            self.tiles.append(lines[i].split())

    def get_tile_dims(self, startX, startY, screenDims):
        x1, y1 = startX//self.tileDims[0], startY//self.tileDims[1]
        x2 = x1 + screenDims[0]//self.tileDims[0] + (1 if startX % self.tileDims[0] else 0)
        y2 = y1 + screenDims[1]//self.tileDims[1] + (1 if startX % self.tileDims[1] else 0)
        return (x1, x2, y1, y2)

    def get_drawing_info(self, screenDims, startCords):
        x1, x2, y1, y2 = self.get_tile_dims(startCords[0], startCords[1], screenDims)
        offsetX = startCords[0] % self.tileDims[0]
        offsetY = startCords[1] % self.tileDims[1]
        mapTiles = []
        for i in range(x1, x2+1):
            mapTiles.append(self.tiles[i][y1:y2+1])
        return mapTiles, (offsetX, offsetY), self.tileDims

    def tile_speed(self, x, y):
        # TODO: will determine if player can walk on tile
        return 1

    def get_movement(self, cords, move): # TODO: can we clean this up?
        tileX, tileY = cords[0]//self.tileDims[0], cords[1]//self.tileDims[1]
        x, y = cords
        if move == 'l':
            if tileX <= 0:
                return 0
            return self.tile_speed(x-1, y) * -self.tileDims[0]
        elif move == 'r':
            if tileX >= (self.maxDims[0]-1)//self.tileDims[0]:
                return 0
            return self.tile_speed(x+1, y) * self.tileDims[0]
        elif move == 'u':
            if tileY <= 0:
                return 0
            return self.tile_speed(x, y-1) * -self.tileDims[1]
        elif move == 'd':
            if tileY >= (self.maxDims[1]-1)//self.tileDims[1]:
                return 0
            return self.tile_speed(x-1, y+1) * self.tileDims[1]
