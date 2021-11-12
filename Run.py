import os
import shutil
import subprocess
import sys
import time
import settings
import PyQt5.QtWidgets
import easygui
import numpy
from PyQt5 import QtWidgets
from PyQt5.QtGui import QPixmap
from matplotlib import pyplot
import matplotlib
from pyqtgraph import PlotWidget, mkPen
import pyqtgraph
import os
from os import path
import natsort
import pandas
from MaxbotixBME import BMEclient

pyqtgraph.setConfigOption('background', 'w')
pyqtgraph.setConfigOption('foreground', 'k')

# See for embedding QT PLOT
# https://www.pythonguis.com/tutorials/embed-pyqtgraph-custom-widgets-qt-app/

subprocess.Popen(['pyuic5', 'bme_sonar_gui.ui', '-o', 'bme_sonar_gui.py'])

import bme_sonar_gui


class Application(bme_sonar_gui.Ui_MainWindow):
    def __init__(self):
        self.MainWindow = QtWidgets.QMainWindow()
        self.setupUi(self.MainWindow)
        self.MainWindow.show()

        self.data = None
        self.data_saved = False
        self.client = BMEclient()

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
        existing_files = os.listdir(settings.buffer_dir)
        existing_files = natsort.natsorted(existing_files)
        self.measurementList.insertItems(0, existing_files)

    def plot_data(self, data, legend_name=''):
        distance = numpy.linspace(0, settings.duration, len(self.data)) * 17
        colors = settings.colors
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


    def set_status(self, text):
        text = str(text)
        self.statusbar.showMessage(text)

    def handle_measure_button(self):
        measurement_name = self.MeasurementName.text()

        self.client.connect()
        self.data = self.client.get_data(rate=settings.rate, duration=settings.duration)


        self.data = self.data - settings.baseline
        #self.data = numpy.random.random(200) * 2500

        self.plot_data(self.data, measurement_name)
        self.data_saved = False
        self.set_status('Measurement %s Completed' % measurement_name)

    def handle_delete_data_button(self):
        current_item = self.measurementList.currentItem()

        if current_item is None:
            self.set_status('Select data to delete')
            return

        current_item = current_item.text()
        full_file_name = path.join(settings.buffer_dir, current_item)
        os.remove(full_file_name)
        self.update_measurement_list()
        self.set_status('Deleted %s' % full_file_name)


    def handle_plot_data_button(self):
        current_item = self.measurementList.currentItem()

        if current_item is None:
            self.set_status('Select data to plot')
            return

        current_item = current_item.text()
        full_file_name = path.join(settings.buffer_dir, current_item)
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

        existing_files = os.listdir(settings.buffer_dir)
        new_index = len(existing_files)
        file_name = 'measurement_%04i_%s' % (new_index, measurement_name)
        full_file_name = path.join(settings.buffer_dir, file_name + '.txt')
        numpy.savetxt(full_file_name, self.data)
        self.data_saved = True
        self.update_measurement_list()
        self.set_status('Measurement saved to %s' % full_file_name)

    def export(self):
        existing_files = os.listdir(settings.buffer_dir)
        existing_files = natsort.natsorted(existing_files)
        all_data = {}
        for current_item in existing_files:
            full_file_name = path.join(settings.buffer_dir, current_item)
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
