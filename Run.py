import os
import subprocess
import sys
from os import path

import natsort
import numpy
import pandas
import pyqtgraph
from PyQt5 import QtWidgets

from MaxbotixBME import BMEclient
from ReadSettings import SettingsReader

Settings = SettingsReader()
Settings.print_settings()

pyqtgraph.setConfigOption('background', 'w')
pyqtgraph.setConfigOption('foreground', 'k')

# See for embedding QT PLOT
# https://www.pythonguis.com/tutorials/embed-pyqtgraph-custom-widgets-qt-app/

try:
    subprocess.Popen(['pyuic5', 'bme_sonar_gui.ui', '-o', 'bme_sonar_gui.py'])
    print('converted ui to py')
except:
    print('could not convert ui to py')

import bme_sonar_gui


class Application(bme_sonar_gui.Ui_MainWindow):
    def __init__(self):
        self.MainWindow = QtWidgets.QMainWindow()
        self.setupUi(self.MainWindow)
        self.MainWindow.show()
        
        self.data = None
        self.data_saved = False
        self.client = BMEclient()

        exists = os.path.exists(Settings.buffer_dir)
        if not exists: os.makedirs(Settings.buffer_dir)

        self.line_index = 0
        self.measureButton.clicked.connect(self.handle_measure_button)
        self.SaveMeasurementButton.clicked.connect(self.handle_save_measurement_button)
        self.plotDataButton.clicked.connect(self.handle_plot_data_button)
        self.deleteDataButton.clicked.connect(self.handle_delete_data_button)
        self.actionExport.triggered.connect(self.export)
        self.update_measurement_list()

        self.set_status('Ready')

    def update_measurement_list(self):
        self.measurementList.clear()
        existing_files = os.listdir(Settings.buffer_dir)
        existing_files = natsort.natsorted(existing_files)
        self.measurementList.insertItems(0, existing_files)

    def plot_data(self, data, legend_name=''):
        distance = numpy.linspace(0, Settings.duration, len(self.data)) * 17
        colors = Settings.colors
        if not self.holdMeasurementBox.isChecked():
            self.graphWidget.clear()
            self.line_index = -1

        self.line_index = self.line_index + 1
        if self.line_index > len(colors) -1 : self.line_index = 0
        current_color = colors[self.line_index]
        self.graphWidget.setLimits(xMin=0, xMax=2000, yMin=0, yMax=5000)
        self.graphWidget.addLegend()
        if legend_name == '': legend_name = str(self.line_index)
        self.graphWidget.plot(distance, data, pen=pyqtgraph.mkPen(current_color, width=2), name=legend_name)
        self.graphWidget.setLimits(xMin=0, xMax=2000, yMin=0, yMax=5000)


    def set_status(self, text):
        text = str(text)
        self.statusbar.showMessage(text)

    def handle_measure_button(self):
        measurement_name = self.MeasurementName.text()
        if not Settings.dummy_data:
            print('Performing measurement...')
            self.client.connect()
            self.data = self.client.get_data(rate=Settings.rate, duration=Settings.duration, raw=Settings.raw_data)

        else:
            print('Generating dummy data ...')
            self.data = numpy.random.random(100) * 3000 + Settings.baseline

        if not Settings.raw_data: self.data = self.data - Settings.baseline
        self.plot_data(self.data, measurement_name)
        self.data_saved = False
        self.set_status('Measurement %s Completed' % measurement_name)

    def handle_delete_data_button(self):
        current_item = self.measurementList.currentItem()

        if current_item is None:
            self.set_status('Select data to delete')
            return

        current_item = current_item.text()
        full_file_name = path.join(Settings.buffer_dir, current_item)
        os.remove(full_file_name)
        self.update_measurement_list()
        self.set_status('Deleted %s' % full_file_name)


    def handle_plot_data_button(self):
        current_item = self.measurementList.currentItem()

        if current_item is None:
            self.set_status('Select data to plot')
            return

        current_item = current_item.text()
        full_file_name = path.join(Settings.buffer_dir, current_item)
        data = numpy.loadtxt(full_file_name)
        legend_name = current_item.replace('.txt', '')
        self.plot_data(data, legend_name)
        self.set_status('Plotted %s' % full_file_name)

    def handle_save_measurement_button(self):
        measurement_name = self.MeasurementName.text()

        if measurement_name == '':
            self.set_status('Provide a name before saving')
            return

        if self.data_saved:
            self.set_status('Data was already saved')
            return

        if self.data is None:
            self.set_status('No data to save')
            return

        existing_files = os.listdir(Settings.buffer_dir)
        new_index = len(existing_files)
        file_name = 'measurement_%04i_%s' % (new_index, measurement_name)
        full_file_name = path.join(Settings.buffer_dir, file_name + '.txt')
        numpy.savetxt(full_file_name, self.data)
        self.data_saved = True
        self.update_measurement_list()
        self.set_status('Measurement saved to %s' % full_file_name)

    def export(self):
        existing_files = os.listdir(Settings.buffer_dir)
        existing_files = natsort.natsorted(existing_files)
        all_data = {}
        for current_item in existing_files:
            full_file_name = path.join(Settings.buffer_dir, current_item)
            column = current_item.replace('.txt', '')
            data = numpy.loadtxt(full_file_name)
            all_data[column] = data
        all_data = pandas.DataFrame(all_data)
        result = QtWidgets.QFileDialog.getSaveFileName(self.MainWindow, 'Save File')
        save_name = result[0]
        all_data.to_csv(save_name)
        self.set_status('Data exported to %s' % save_name)


app = QtWidgets.QApplication(sys.argv)
app.setStyle('Fusion')
ui = Application()
sys.exit(app.exec_())
