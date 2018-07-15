import pygame

class GameState(object):
    
    def load_image(self, image, cords):
        self.screen.blit(image, cords)
                
    def create_images(self, imageFiles):
        if type(imageFiles) == dict:
            images = {}
            for sec, value in imageFiles.items():
                images[sec] = self.create_images(value)
            return images
        else: 
            return pygame.image.load(imageFiles) # * should only be one file
        
    def process_input(self):
        raise NotImplementedError
        
    def make_actions(self):
        raise NotImplementedError

    def draw(self):
        raise NotImplementedError