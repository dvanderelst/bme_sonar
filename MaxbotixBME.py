import re
import socket

import numpy
from matplotlib import pyplot

break_char = '*'


class BMEclient:
    def __init__(self, ip='192.168.4.1', port=1000):
        self.ip = ip
        self.port = port
        self.sock = None
        self.server_address = None

    def connect(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_address = (self.ip, self.port)
        self.sock.connect(self.server_address)

    def disconnect(self):
        self.sock.close()

    def get_data(self, rate, duration):
        command = str(rate) + ',' + str(duration) + break_char
        data = self.send_command(command)
        data = re.findall(r'[0-9]+', data)
        data = [int(i) for i in data]
        data = numpy.array(data)
        return data

    def send_command(self, command, expect_answer=True):
        if not command.endswith(break_char): command += break_char
        self.sock.send(command.encode())
        data = ''
        if not expect_answer: return data
        while 1:
            packet = self.sock.recv(1024)
            packet = packet.decode()
            data += packet
            if data.endswith(break_char): break
        data = data.rstrip(break_char)
        return data


if __name__ == "__main__":
    client = BMEclient()
    client.connect()
    data = client.get_data(rate=10000, duration=20)
    pyplot.plot(data)
    pyplot.show()

# def get_files(location):
#     all_files = os.listdir(location)
#     csv_files = []
#     for x in all_files:
#         if x.endswith('.csv'): csv_files.append(x)
#     return csv_files
#
#
# def process_timestamp(time_stamp):
#     time_parts = time_stamp.split('_')
#     day = int(time_parts[0])
#     month = int(time_parts[1])
#     year = int(time_parts[2])
#     hour = int(time_parts[3])
#     minute = int(time_parts[4])
#     second = int(time_parts[5])
#     time_label = datetime.datetime(day=day, month=month, year=year, hour=hour, minute=minute, second=second)
#     return time_label
#
#
# def process_file(location, file_name):
#     f = open(os.path.join(location, file_name), 'r')
#     lines = f.readlines()
#     f.close()
#
#     top_line = lines[0]
#     top_line = top_line.split(',')
#     label = top_line[0]
#     label = label.rstrip(' ')
#     label = label.lstrip(' ')
#     label = label.lower()
#     comment = top_line[1]
#     time_stamp = top_line[2]
#
#     all_data = []
#     servo_positions = []
#     for line in lines:
#         line = line.split(',')
#         line = line[3:]
#         line = [int(i) for i in line]
#         servo_position = line.pop(0)
#         servo_positions.append(servo_position)
#         all_data.append(line)
#     all_data = numpy.array(all_data)
#     all_data = numpy.transpose(all_data)
#     time = process_timestamp(time_stamp)
#     time_string = time.strftime("%c")
#     result = {}
#     result['label'] = label
#     result['comment'] = comment
#     result['time'] = time
#     result['time_string'] = time_string
#     result['data'] = all_data
#     result['servo_positions'] = servo_positions
#     result['basename'] = file_name.rstrip('.csv')
#     return result
#
#
# def lst2line(lst):
#     line = ''
#     for x in lst:
#         x = str(x)
#         x = x.replace(',', ' ')
#         line = line + x + ','
#     line = line.rstrip(',')
#     return line
#
#
# def process_files(location, output_folder='output'):
#     files = get_files(location)
#     report_name = os.path.join(output_folder, 'report.csv')
#     report = open(report_name, 'w')
#     for file in files:
#         print(file)
#         result = process_file(location, file)
#         basename = result['basename']
#         data = result['data']
#
#         csv_name = os.path.join(output_folder, 'csv', basename + '.csv')
#         pck_name = os.path.join(output_folder, 'pck', basename + '.pck')
#         numpy.savetxt(csv_name, data, delimiter=",")
#
#         file_pi = open(pck_name, 'wb')
#         pickle.dump(result, file_pi)
#         file_pi.close()
#
#         shape = data.shape
#         time = result['time']
#         label = result['label']
#
#         report_line = [label, time, shape]
#         s = lst2line(report_line)
#         report.write(s + '\n')
#     report.close()
#
#
# def read_processed_csv(datset, output_folder='output'):
#     datset = datset.rstrip('.csv')
#     filename = os.path.join(output_folder, 'csv', datset + '.csv')
#     data = numpy.genfromtxt(filename, delimiter=',')
#     return data
#
#
# def read_processed_pck(datset, output_folder='output'):
#     datset = datset.rstrip('.pck')
#     filename = os.path.join(output_folder, 'pck', datset + '.pck')
#     data = SaveLoad.pickle_load(filename)
#     return data
