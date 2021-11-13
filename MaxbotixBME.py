import re
import socket

import numpy
from matplotlib import pyplot
from ReadSettings import SettingsReader

Settings = SettingsReader()

verbose = False

class BMEclient:
    def __init__(self):
        self.ip = Settings.ip
        self.port = Settings.port
        self.sock = None
        self.server_address = None

    def connect(self):
        if verbose: print('Init connection...', end = '')
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_address = (self.ip, self.port)
        self.sock.connect(self.server_address)
        if verbose: print('done')
        
    def disconnect(self):
        self.sock.close()

    def get_data(self, rate, duration):
        if verbose: print('Start get_data...')
        command = str(rate) + ',' + str(duration) + Settings.break_char
        if verbose: print('Command:', command)
        data = self.send_command(command)
        data = re.findall(r'[0-9]+', data)
        data = [int(i) for i in data]
        data = numpy.array(data)
        if verbose: print('Data:', data)
        return data

    def send_command(self, command, expect_answer=True):
        if not command.endswith(Settings.break_char): command += Settings.break_char
        self.sock.send(command.encode())
        data = ''
        if not expect_answer: return data
        while 1:
            packet = self.sock.recv(1024)
            packet = packet.decode()
            data += packet
            if data.endswith(Settings.break_char): break
        data = data.rstrip(Settings.break_char)
        return data


if __name__ == "__main__":
    client = BMEclient()
    client.connect()
    sonar_data = client.get_data(rate=1000, duration=20)
    #pyplot.plot(sonar_data)
    #pyplot.show()
    client.disconnect()
