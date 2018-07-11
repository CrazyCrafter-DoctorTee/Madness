def load_image(screen, image, row, col, scale=True):
    if scale:
        screen.blit(image, (col * 32, row * 32))
    else:
        screen.blit(image, (col, row)) 

class GameMap:
    def __init__(self, filename, images, screenDims=None):
        self.filename = filename
        self.images = images
        self.screenDims = screenDims
        self.generate_template()
        
    def generate_template(self):
        lines = []
        self.tiles = []
        with open(self.filename, 'r') as f:
           for line in f:
               lines.append(line)
        self.dims = tuple(int(d) for d in lines[0].split())
        for i in range(1, self.dims[0]+1):
            self.tiles.append(lines[i].split())

    def draw(self, screen, sRow, sCol, nRows, nCols):
        for i in range(nRows):
            for j in range(nCols):
                load_image(screen, self.images[self.tiles[sRow+i][sCol+j]], i, j)