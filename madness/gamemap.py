class GameMap(object):
    def __init__(self, filename, tileDims=(32, 32)):
        self.tileDims = tileDims
        self.generate_template(filename)

    def generate_template(self, filename):
        lines = []
        with open(filename, 'r') as f:
           for line in f:
               lines.append(line)
        self.dims = tuple(int(d) for d in lines[0].split())
        maxX = self.dims[0]*self.tileDims[0] - self.tileDims[0]
        maxY = self.dims[1]*self.tileDims[1] - self.tileDims[1]
        self.maxDims = (maxX, maxY)
        inverseTiles = []
        for i in range(1, self.dims[0]+1):
            inverseTiles.append(lines[i].split())
        self.tiles = [[] for _ in range(len(inverseTiles[0]))]
        for i in range(len(inverseTiles)):
            for j in range(len(inverseTiles[0])):
                self.tiles[i].append(inverseTiles[j][i])
        

    def get_tile_dims(self, startX, startY, screenDims): # TODO: rename to get_tile_print_range
        x1, y1 = startX//self.tileDims[0], startY//self.tileDims[1]
        x2 = x1 + screenDims[0]//self.tileDims[0] + (1 if startX % self.tileDims[0] else 0)
        y2 = y1 + screenDims[1]//self.tileDims[1] + (1 if startX % self.tileDims[1] else 0)
        return (x1, x2, y1, y2)

    def get_drawing_info(self, screenDims, startCords):
        x1, x2, y1, y2 = self.get_tile_dims(startCords[0], startCords[1], screenDims)
        offsetX = startCords[0] % self.tileDims[0]
        offsetY = startCords[1] % self.tileDims[1]
        mapTiles = [[] for _ in range(x1, x2+1)]
        for i in range(x1, x2+1):
            for j in range(y1, y2+1):
                mapTiles[i-x1].append(self.tiles[i][j])
        return mapTiles, (offsetX, offsetY), self.tileDims

    def impassable(self, x, y):
        if self.tiles[x][y] in ('r','b','t'):
            return True
        return False

    def get_movement(self, cords, move):
        tileX, tileY = cords[0]//self.tileDims[0], cords[1]//self.tileDims[1]
        x, y = cords
        if move == 'l':
            if tileX <= 0 or self.impassable(tileX-1, tileY):
                return 0
            return -self.tileDims[0]
        elif move == 'r':
            if tileX >= (self.maxDims[0]-1)//self.tileDims[0] or self.impassable(tileX+1, tileY):
                return 0
            return self.tileDims[0]
        elif move == 'u':
            if tileY <= 0 or self.impassable(tileX, tileY-1):
                return 0
            return -self.tileDims[1]
        elif move == 'd':
            if tileY >= (self.maxDims[1]-1)//self.tileDims[1] or self.impassable(tileX, tileY+1):
                return 0
            return self.tileDims[1]
