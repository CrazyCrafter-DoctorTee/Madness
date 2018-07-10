from gameutils import *

class Map:
    def __init__(self, filename, images):
        self.filename = filename
        self.images = images
        self.generate_template()
        
    def generate_template(self):
        lines = []
        self.mapTiles = []
        with open(self.filename, 'r') as f:
           for line in f:
               lines.append(line)
        self.dims = tuple(int(d) for d in lines[0].split())
        for i in range(1, self.dims[0]+1):
            self.mapTiles.append(lines[i].split())

    def draw(self, screen):
        print_row, print_col = 0, 0
        for row in self.mapTiles:
            for col in row:
                load_image(screen, images[col], print_row, print_col)
                print_col += 1
            print_col = 0
            print_row += 1