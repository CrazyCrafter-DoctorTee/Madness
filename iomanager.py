import configparser
import pygame

class IOManager(object):
    
    def __init__(self, configFile):
        self.masterConfig = configparser.ConfigParser()
        self.masterConfig.read(configFile)
        self.data = self.parse_file(self.masterConfig)
        
    def parse_file(self, config):
        data = {}
        for s in config.sections():
            data[s] = {}
            for key, value in config[s].items():
                data[s][key] = value
        if 'config' in data.items():
           for name, filename in data['config']:
               newConfig = configparser.ConfigParser()
               newConfig.read(filename)
               data[name] = self.parse_file(newConfig)
        return data
    
    def get_data(self, *sections):
        subData = self.data
        for s in sections:
            subData = subData[s]
        return dict(subData)
    
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
