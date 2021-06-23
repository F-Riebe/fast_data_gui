import numpy as np
import matplotlib.pyplot as plt

from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import *

from pyFAST.input_output import FASTOutputFile

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

import pandas as pd

class Plotten(FigureCanvas):
    def __init__(self, width=6, height=5, dpi=100):

        self.fig = Figure(figsize=(width, height), dpi=dpi)
        super().__init__(self.fig)

        self.axes = self.fig.add_subplot()
        
    
    def update_figure(self, data_set, plot_data):
        
        
        self.axes.cla()
        
        #self.axes.set_xlabel(label_x)
        #self.axes.set_ylabel(label_y)
        if data_set.empty is not True:    
            self.axes.plot(data_set['Time_[s]'], data_set[plot_data])
            self.draw()
        

    #def save_figure(self, figureToSave, pathToSave):



class DataHandler():
    def __init__(self):
        self.df = pd.DataFrame({'A' : []})
        self.df_variables = np.array
        
    def importResults(self, dataFile):
        
        del self.df
        self.df = FASTOutputFile(dataFile).toDataFrame()
        del self.df_variables
        self.df_variables = self.df.columns.to_numpy()

    #def storeResults(self, pathToStore, list_of_entries):
           




class MainClassAsGUI(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        
        #Create Window
        mainLayout = QtWidgets.QGridLayout()
        
        self.setWindowTitle('Fast Data Plot')
        self.label=QLabel(self)

        self.dataHandler = DataHandler()

        self.plotWidget = Plotten()
        
        #Set Window Size
        width = 600
        height = 600
        self.resize(width, height)
        
        #SubLayout for File Selection
        subLayout1 = QtWidgets.QVBoxLayout()
                
        #Create Button for File Selection
        self.selectFileButton = QtWidgets.QPushButton('Select Fast output File')
        self.selectFileButton.clicked.connect(self.selectFile)
        subLayout1.addWidget(self.selectFileButton)
        
        #Create Text Field for File Name
        self.fileNameLineEdit = QtWidgets.QLineEdit()
        subLayout1.addWidget(self.fileNameLineEdit)

        self.comboBoxSelection = QtWidgets.QComboBox()
        subLayout1.addWidget(self.comboBoxSelection)
        self.comboBoxSelection.currentIndexChanged.connect(self.plotFigure)

        
    
        subLayout1.addStretch()
        
        self.plotWidget = Plotten()
        
        subLayout2 = QtWidgets.QVBoxLayout()
        subLayout2.addWidget(self.plotWidget)
        
        #Adding all SubLayouts to MainLayout
        mainLayout.addLayout(subLayout1, 1,1)
        mainLayout.addLayout(subLayout2, 2,1)
        self.setLayout(mainLayout)

    def plotFigure(self):
        self.plotWidget.update_figure(self.dataHandler.df, self.comboBoxSelection.currentText())
        
    def updateComboBox(self, dataFrame):
        self.comboBoxSelection.clear()
        self.comboBoxSelection.addItems(dataFrame[1:])


    def readLineEdit(self, lineEditToRead):
        return lineEditToRead.text()
    
    
    def selectFile(self):
        
        fname = QFileDialog.getOpenFileName(self, 'Open Fast Output file', 
         'c:\\',"Fast Output files (*.out)")
        self.fileNameLineEdit.setText(str(fname[0]))
        
        lineEdit_fileName = self.readLineEdit(self.fileNameLineEdit)
        
        self.dataHandler.importResults(lineEdit_fileName)
        
        self.updateComboBox(self.dataHandler.df_variables)
        



if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    gui = MainClassAsGUI()
    gui.show()
    app.exec_()