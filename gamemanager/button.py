class Button:
    def __init__(self, image, words, dims, keytype):
        self.image = image
        self.words = words
        self.keytype = keytype
        self.x1 = dims[0]
        self.x2 = dims[1]
        self.y1 = dims[2]
        self.y2 = dims[3]

    def update(self, mx, my):
        if self.x1 <= mx <= self.x2:
            if self.y1 <= my <= self.y2:
                return self.keytype
        return None

    def get_drawing_info(self):
        image = (self.image, (self.x1, self.x2, self.y1, self.y2))
        font = (self.words, (self.x1+0.01, self.x2-0.01, self.y1+0.01, self.y2-0.01))
        return image, font