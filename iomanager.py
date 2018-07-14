import configparser

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
                data[s][key] = self.process_value(value)
        if 'config' in data.keys():
           for name, filename in data['config'].items():
               newConfig = configparser.ConfigParser()
               newConfig.read(filename)
               data[name] = self.parse_file(newConfig)
        return data

    def process_value(self, value):
        if ',' in value:
            valueList = [v.strip() for v in value.split(',')]
            for i in range(len(valueList)):
                if valueList[i].isdigit():
                    valueList[i] = int(valueList[i])
            return valueList
        elif value.isdigit():
            return int(value)
        else:
            return value
            
    
    def get_data(self, *sections):
        subData = self.data
        for s in sections:
            subData = subData[s]
        try:
            return subData.copy()
        except:
            return subData