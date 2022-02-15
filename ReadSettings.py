import configparser

class SettingsReader:
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read('settings.ini')

        self.dummy_data = self.config['DEFAULT']['dummy_data']
        if self.dummy_data == 'True':
            self.dummy_data = True
        else:
            self.dummy_data = False

        self.colors = self.config['DEFAULT']['colors']
        self.colors = self.colors.split(',')
        
        self.buffer_dir = self.config['DEFAULT']['buffer_dir']
        
        self.ip = self.config['DEFAULT']['ip']
        
        self.port = int(self.config['DEFAULT']['port'])
        
        self.rate = int(self.config['DEFAULT']['rate'])
  
        self.duration = int(self.config['DEFAULT']['duration'])
        
        self.baseline = int(self.config['DEFAULT']['baseline'])
        self.signal_threshold = int(self.config['DEFAULT']['signal_threshold'])
        
        self.break_char = self.config['DEFAULT']['break_char']

        self.raw_data = self.config['DEFAULT']['raw_data']
        if self.raw_data == 'True':
            self.raw_data = True
        else:
            self.raw_data = False

    def print_settings(self):
        print('SETTINGS')
        print('dummy_data', self.dummy_data, type(self.dummy_data))
        print('colors', self.colors, type(self.colors))
        print('buffer_dir', self.buffer_dir, type(self.buffer_dir))
        print('ip', self.ip, type(self.ip))
        print('port', self.port, type(self.port))
        print('rate', self.rate, type(self.rate))
        print('duration', self.duration, type(self.duration))
        print('baseline', self.baseline, type(self.baseline))
        print('signal_threshold', self.signal_threshold, type(self.signal_threshold))
        print('break_char', self.break_char, type(self.break_char))
        print('raw_data', self.raw_data, type(self.raw_data))


        
    

        