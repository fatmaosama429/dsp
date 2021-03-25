import sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import QApplication, QWidget
import pandas as pd
class Canvas(FigureCanvas):
    def __init__(self, parent):
        fig, self.ax = plt.subplots(figsize=(5, 4), dpi=200)
        super().__init__(fig)
        self.setParent(parent)

        """ 
        Matplotlib Script
        """
        t = np.arange(0.0, 2.0, 0.01)
        s = 1 + np.sin(2 * np.pi * t)
        
        self.ax.plot(t, s)

        self.ax.set(xlabel='time (s)', ylabel='voltage (mV)')
        self.ax.grid()
        
 
class AppDemo(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(800, 800)

        chart = Canvas(self)

app = QApplication(sys.argv)        
demo = AppDemo()
demo.show()
sys.exit(app.exec_())
        