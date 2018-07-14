import configparser
import pygame

class IOManager(object):
    
    def __init__(self, configFile):
        self.masterConfig = configparser.ConfigParser()
        self.masterConfig.read(configFile)
        self.generalParams = self.parse_file(self.masterConfig)
        self.otherParams ={}
        if 'configs' in self.generalParams:
            for c in self.generalParams['configs']:
                parser = configparser.ConfigParser()
                parser.read(c)
                self.otherParams[c] = self.parse_file(parser)
        
    def parse_file(self, config):
        data = {}
        for s in config.sections[]:
            data[s] = {}
            for key, value in config[s].items:
                data[s][key] = value
        return data
    
    def read_files(self):
        self.images = {}
        self.maps = {}
        self.graphics = {}
        #initialize graphics settings first
        for key in config['graphics']:
            self.graphics[key] = [int(x) for x in config['graphics'][key].split(',')]
        #now we can do the rest of the config reading
        for key in config['images']:
            self.images[key] = pygame.image.load(config['images'][key])
        for key in config['maps']:
            self.maps[key] = gamemap.GameMap(config['maps'][key], self.images, self.screen, self.graphics['tiledims'])
