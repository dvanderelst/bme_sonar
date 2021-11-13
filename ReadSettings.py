import configparser

class SettingsReader:
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read('settings.ini')
        
        self.colors = self.config['DEFAULT']['colors']
        self.colors = self.colors.split(',')
        
        self.buffer_dir = self.config['DEFAULT']['buffer_dir']
        
        self.ip = self.config['DEFAULT']['ip']
        
        self.port = int(self.config['DEFAULT']['port'])
        
        self.rate = int(self.config['DEFAULT']['rate'])
  
        self.duration = int(self.config['DEFAULT']['duration'])
        
        self.baseline = int(self.config['DEFAULT']['baseline'])
        
        self.break_char = self.config['DEFAULT']['break_char']
        
    

        