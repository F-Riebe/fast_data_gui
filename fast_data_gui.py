import numpy as np
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import *
import matplotlib.pyplot as plt
import os

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class Plotten(FigureCanvas):
    def __init__(self, width=6, height=5, dpi=100):

        self.fig = Figure(figsize=(width, height), dpi=dpi)
        super().__init__(self.fig)

        self.axes = self.fig.add_subplot()
        
    
    def update_figure(self, data_set):
        
        
        self.axes.cla()
        variables = data_set[0]
        units = data_set[1]
        results = data_set[2]
        
        x_axis_num = 0
        y_axis_num = 10
        
        label_x = str(variables[x_axis_num] + ' ' + units[x_axis_num])
        label_y = str(variables[y_axis_num] + ' ' + units[y_axis_num])
        
        self.axes.set_xlabel(label_x)
        self.axes.set_ylabel(label_y)
        self.axes.plot(results[:, x_axis_num], results[:, y_axis_num])
        self.draw()
        

        


class MainClassAsGUI(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        
        #Create Window
        mainLayout = QtWidgets.QGridLayout()
        
        self.setWindowTitle('Fast Data Plot')
        self.label=QLabel(self)
        
        #Set Window Size
        width = 600
        height = 600
        self.resize(width, height)
        
        #SubLayout for File Selection
        subLayout1 = QtWidgets.QVBoxLayout()
                
        #Create Button for File Selection
        self.selectFileButton = QtWidgets.QPushButton('Select Fast output File')
        self.selectFileButton.clicked.connect(self.selectAndReadFile)
        subLayout1.addWidget(self.selectFileButton)
        
        #Create Text Field for File Name
        self.fileNameLineEdit = QtWidgets.QLineEdit()
        subLayout1.addWidget(self.fileNameLineEdit)
    
        subLayout1.addStretch()
        
        self.plotWidget = Plotten()
        
        subLayout2 = QtWidgets.QVBoxLayout()
        subLayout2.addWidget(self.plotWidget)
        
        #Adding all SubLayouts to MainLayout
        mainLayout.addLayout(subLayout1, 1,1)
        mainLayout.addLayout(subLayout2, 2,1)
        self.setLayout(mainLayout)
        
       
    def readLineEdit(self):
        self.fileNameReadIn = self.fileNameLineEdit.text()
    
    def selectAndReadFile(self):
        
        fname = QFileDialog.getOpenFileName(self, 'Open Fast Output file', 
         'c:\\',"Fast Output files (*.out)")
        self.fileNameLineEdit.setText(str(fname[0]))
        
        
        with open(fname[0]) as file_in:
            lines = []
            for line in file_in:
                lines.append(line)
            file_in.close()

            analysis_info1 = lines[1]
            analysis_info1 = str(analysis_info1[0])  

            analysis_info2 = [s for s in lines if "Description from the FAST input file:" in s]
            analysis_info2 = str(analysis_info2[0])
            analysis_info2 = analysis_info2.strip("Description from the FAST input file: ")

            line_index_info1 = 1
            
            line_index_info2 = [i for i, s in enumerate(lines) if "Description from the FAST input file:" in s]

            if len(line_index_info2) == 1:
                line_index_info2 = int(line_index_info2[0])
            else:
                print("Wrong format")
                exit() 

            line_index_data_variables = line_index_info2 + 2
            line_index_data_units = line_index_data_variables + 1
            line_index_data_start = line_index_data_units + 1
            
            data_variables = []
            data_variables = lines[line_index_data_variables].split("\t")
            data_variables_array = np.array(data_variables)
            
            tmp_variables = []
            for element in data_variables:
                tmp_variables.append(element.strip())
            data_variables = tmp_variables
            
            data_units = []
            data_units = lines[line_index_data_units].split("\t") 
            
            tmp_units = []
            for element in data_units:
                tmp_units.append(element.strip())
            data_units = tmp_units
            data_units_array = np.array(data_units, dtype=str)
            
            num_timesteps = int (len(lines) - line_index_data_start) 
            num_variables = int(len(data_variables))
            
            data_array = np.zeros((num_timesteps, num_variables))
            
            for i in range(line_index_data_start, num_timesteps+line_index_data_start):
                data_array[(i-line_index_data_start)] = lines[i].split("\t")
                
            list_of_data_arrays = []
            list_of_data_arrays.append(data_variables_array)
            list_of_data_arrays.append(data_units_array)
            list_of_data_arrays.append(data_array)
            
            self.plotWidget.update_figure(list_of_data_arrays)
            
            
            
                 
    
        
        
if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    gui = MainClassAsGUI()
    gui.show()
    app.exec_()