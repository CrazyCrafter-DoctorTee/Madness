import pygame

class GameState(object):
    
    def load_image(self, image, cords):
        if len(cords) == 2:
            self.screen.blit(image, cords)
        else:
            x1, x2 = int(cords[0] * self.screenDims[0]), int(cords[1] * self.screenDims[0])
            y1, y2 = int(cords[2] * self.screenDims[1]), int(cords[3] * self.screenDims[1])
            scaledImg = pygame.transform.scale(image, (x2-x1, y2-y1))
            self.screen.blit(scaledImg, (x1, y1))
                
    def create_images(self, imageFiles):
        if type(imageFiles) == dict:
            images = {}
            for sec, value in imageFiles.items():
                images[sec] = self.create_images(value)
            return images
        else: 
            return pygame.image.load(imageFiles) # *should only be one file
        
    def print_words(self, words, cords):
        x1, x2 = int(cords[0] * self.screenDims[0]), int(cords[1] * self.screenDims[0])
        y1, y2 = int(cords[2] * self.screenDims[1]), int(cords[3] * self.screenDims[1])
        height = 3 * (y2 - y1)
        size = int(height//5)
        wordFont = pygame.font.SysFont('Comic Sans MS', size) # :)
        print(words)
        wordSurface = wordFont.render(words, 1, (255,255,255))
        self.screen.blit(wordSurface, (x1, y1))

    def process_input(self): # must return new gamestate
        raise NotImplementedError
        
    def make_actions(self):
        raise NotImplementedError

    def draw(self):
        raise NotImplementedError