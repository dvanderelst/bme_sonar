# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'bme_sonar_gui.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(983, 799)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("../../../.designer/backup/bat.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setContentsMargins(2, 1, 2, 23)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.graphWidget = PlotWidget(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.graphWidget.sizePolicy().hasHeightForWidth())
        self.graphWidget.setSizePolicy(sizePolicy)
        self.graphWidget.setObjectName("graphWidget")
        self.verticalLayout_2.addWidget(self.graphWidget)
        self.holdMeasurementBox = QtWidgets.QCheckBox(self.centralwidget)
        self.holdMeasurementBox.setObjectName("holdMeasurementBox")
        self.verticalLayout_2.addWidget(self.holdMeasurementBox)
        self.measureButton = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.measureButton.sizePolicy().hasHeightForWidth())
        self.measureButton.setSizePolicy(sizePolicy)
        self.measureButton.setObjectName("measureButton")
        self.verticalLayout_2.addWidget(self.measureButton)
        self.MeasurementName = QtWidgets.QLineEdit(self.centralwidget)
        self.MeasurementName.setObjectName("MeasurementName")
        self.verticalLayout_2.addWidget(self.MeasurementName)
        self.SaveMeasurementButton = QtWidgets.QPushButton(self.centralwidget)
        self.SaveMeasurementButton.setObjectName("SaveMeasurementButton")
        self.verticalLayout_2.addWidget(self.SaveMeasurementButton)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setContentsMargins(4, 4, 4, 4)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.measurementList = QtWidgets.QListWidget(self.centralwidget)
        self.measurementList.setObjectName("measurementList")
        self.verticalLayout_3.addWidget(self.measurementList)
        self.plotDataButton = QtWidgets.QPushButton(self.centralwidget)
        self.plotDataButton.setObjectName("plotDataButton")
        self.verticalLayout_3.addWidget(self.plotDataButton)
        self.deleteDataButton = QtWidgets.QPushButton(self.centralwidget)
        self.deleteDataButton.setObjectName("deleteDataButton")
        self.verticalLayout_3.addWidget(self.deleteDataButton)
        self.horizontalLayout.addLayout(self.verticalLayout_3)
        self.horizontalLayout.setStretch(0, 1)
        self.verticalLayout.addLayout(self.horizontalLayout)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menuBar = QtWidgets.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 983, 20))
        self.menuBar.setObjectName("menuBar")
        self.menuData = QtWidgets.QMenu(self.menuBar)
        self.menuData.setObjectName("menuData")
        MainWindow.setMenuBar(self.menuBar)
        self.actionExport = QtWidgets.QAction(MainWindow)
        self.actionExport.setObjectName("actionExport")
        self.actionRemove = QtWidgets.QAction(MainWindow)
        self.actionRemove.setObjectName("actionRemove")
        self.menuData.addAction(self.actionExport)
        self.menuBar.addAction(self.menuData.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "BmE Sonar"))
        self.holdMeasurementBox.setText(_translate("MainWindow", "Hold measurements"))
        self.measureButton.setText(_translate("MainWindow", "Measure"))
        self.SaveMeasurementButton.setText(_translate("MainWindow", "Save Measurement"))
        self.plotDataButton.setText(_translate("MainWindow", "Plot data"))
        self.deleteDataButton.setText(_translate("MainWindow", "Delete Data"))
        self.menuData.setTitle(_translate("MainWindow", "Data"))
        self.actionExport.setText(_translate("MainWindow", "Export Measurement"))
        self.actionRemove.setText(_translate("MainWindow", "Empty data buffer"))
from pyqtgraph import PlotWidget