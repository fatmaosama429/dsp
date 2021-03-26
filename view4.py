import csv
import os
import sys
from os.path import dirname, realpath,join
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow,QVBoxLayout,QAction,QFileDialog
from PyQt5.uic import  loadUiType
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PyQt5.QtWidgets import QMenu

scriptDir=dirname(realpath(__file__))
From_Main,_= loadUiType(join(dirname(__file__),"main.ui"))

class mainwind(QMainWindow,From_Main):
    def __init__(self):
        super(mainwind, self).__init__()
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.ToolBar()
        self.create_MenuBar()
        self.sc =myCanvas()
        self.l=QVBoxLayout(self.graphicsView)
        self.l.addWidget(self.sc)
    
    def create_MenuBar(self):
        menuBar = self.menuBar()
        self.setMenuBar(menuBar)
        #        menubar file
        file_menu = menuBar.addMenu('file')

        open_action = file_menu.addAction('open file')
        # plot_action = file_menu.addAction('plot')
        quit= file_menu.addAction('Quit',self.close)
        quit.setShortcut("Ctrl+Q")
        
        open_action.triggered.connect(self.open_sheet)
        open_action.setShortcut("Ctrl+O")
        # plot_action.triggered.connect(self.Plot)
        
        # menubar  edit
        edit_menu = menuBar.addMenu('edit')
        edit_menu.addAction('Quit',self.close)
        
        # menubar  mode
        mode_menu = menuBar.addMenu('mode')
        mode_menu.addAction('Quit',self.close)	
        
        # menubar  view
        view_menu = menuBar.addMenu('view')
        view_menu.addAction('Quit',self.close)
        
        # menubar  tools
        tools_menu = menuBar.addMenu('tools')
        tools_menu.addAction('Quit',self.close)
        
        # menubar  help
        help_menu = menuBar.addMenu('help')
        help_menu.addAction('Quit',self.close)       


    def ToolBar(self):
        AddFile = QAction(QIcon('images.png'),'Open File',self)
        AddFile.triggered.connect(self.open_sheet)
        self.toolBar= self.addToolBar('TOOL BAR')
        self.toolBar.addAction(AddFile)
        self.toolBar.setObjectName("toolBar")
        
        # AddPlot = QAction(QIcon('Scatter.png'),'Scatter',self)
        # AddPlot.triggered.connect(self.Plot)
        # self.toolBar= self.addToolBar('Add plot')
        # self.toolBar.addAction(AddPlot)
        

    def open_sheet(self):
        path = QFileDialog.getOpenFileName(self, "Open", "", "CSV Files (*.csv);;All Files (*)")
        if path[0]!='':
            self.FileN=path[0]
        self.Plot()

    def Plot(self):
        f=self.FileN
        #index = int(self.lineEdit.text())
        x= []
        y=[]
        with open(f, newline = '') as csv_file:
            my_file = csv.reader(csv_file, delimiter = ',')
            for row in my_file:
                x.append(str(row[0]))
                y.append(str(row[1]))
        self.sc.plot(x, y)
        



class myCanvas(FigureCanvas):
    def __init__(self):
        self.fig=Figure()
        FigureCanvas.__init__(self,self.fig)

    def plot(self,xarray,yarray):
        self.fig.clear()
        self.ax= self.fig.add_subplot(111)
        self.ax.plot(xarray[1:],yarray[1:])
        self.ax.set_xlabel(xarray[0])
        self.ax.set_ylabel(yarray[0])
        self.draw()
        

app = QApplication(sys.argv)
sheet= mainwind()
sheet.show()
sheet.setWindowTitle("Sigviewer")
sheet.setWindowIcon(QIcon("icon.png"))
sys.exit(app.exec_())

