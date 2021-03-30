import csv
import os
import sys
from PyQt5.uic.properties import QtCore
from PyQt5 import QtCore,QtWidgets
import numpy as np
import pandas as pd
import pyqtgraph as pg 
from os.path import dirname, realpath,join
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow,QVBoxLayout,QAction,QFileDialog
from PyQt5.uic import  loadUiType
# from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
# from matplotlib.figure import Figure
from PyQt5.QtWidgets import QMenu
from PyQt5.QtPrintSupport import QPrinter, QPrintDialog, QPrintPreviewDialog
from PyQt5.QtCore import QAbstractEventDispatcher, QFileInfo
from PyQt5 import QtWidgets, QtCore, uic,QtGui
from PyQt5.QtWidgets import * 
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.uic import loadUiType
import pyqtgraph as pg
from pyqtgraph import PlotWidget, plot
import numpy as np
from random import randint
import csv 
import pandas as pd
import os
from os import path
import sys

scriptDir=dirname(realpath(__file__))
From_Main,_= loadUiType(join(dirname(__file__),"main.ui"))

class mainwind(QMainWindow,From_Main):
    def __init__(self):
        super(mainwind, self).__init__()
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.ToolBar()
        self.create_MenuBar()
        self.sc =pg.PlotWidget()
        self.timer = QtCore.QTimer()
        self.l=QVBoxLayout(self.graphicsView)
        self.l.addWidget(self.sc)
        

    def create_MenuBar(self):
        menuBar = self.menuBar()
        self.setMenuBar(menuBar)
        #        menubar file
        file_menu = menuBar.addMenu('file')
        
        open_action= QAction(QIcon("open.png"),"open File", self)
        file_menu.addAction(open_action)

        saveAction= QAction(QIcon("save.png"), "save", self)
        file_menu.addAction(saveAction)
        saveAction.setShortcut("Ctrl+S")

        printAction= QAction(QIcon("print.png"),"Print", self)
        printAction.triggered.connect(self.printDialog)
        file_menu.addAction(printAction)

        printPreviewAction=QAction("print preview", self)
        #        printPreviewAction.triggered.connect(self.printPreviewDialog)
        file_menu.addAction(printPreviewAction)
        
        pdfAction=QAction(QIcon("export.png"), "Export PDF...", self)
        pdfAction.triggered.connect(self.pdfExport)
        file_menu.addAction(pdfAction)

        gdfAction=QAction("Export GDF...", self)
        file_menu.addAction(gdfAction)

        eventsAction=QAction("Export Events...", self)
        file_menu.addAction(eventsAction)

        importAction=QAction("Import Events...", self)
        file_menu.addAction(importAction)

        infoAction=QAction(QIcon("info.png"), "Info...", self)
        file_menu.addAction(infoAction)

        closeAction=QAction(QIcon("close.png"), "Close", self)
        file_menu.addAction(closeAction)
        closeAction.setShortcut("Ctrl+f4")

        
        # plot_action = file_menu.addAction('plot')
        exitAction=QAction(QIcon("exit.png"), "Exit", self)
        file_menu.addAction(exitAction)
        exitAction.setShortcut("Ctrl+Q")

        
        open_action.triggered.connect(self.OpenBrowse)
        open_action.setShortcut("Ctrl+O")
        # plot_action.triggered.connect(self.Plot)
        
        # menubar  edit
        edit_menu = menuBar.addMenu('edit')
                
        undoAction=QAction(QIcon("undo.png"), "Undo", self)
        edit_menu.addAction(undoAction)
        undoAction.setShortcut("Ctrl+Z")

        redoAction =QAction(QIcon("redo.png"), "Redo", self)
        edit_menu.addAction(redoAction)
        redoAction.setShortcut("Ctrl+Y")

        toallAction =QAction(QIcon("to_all.png"), "to All Channels", self)
        edit_menu.addAction(toallAction)
                
        copyAction =QAction(QIcon("copy.png"), "Copy to Channels...", self)
        edit_menu.addAction(copyAction)

        deleteAction =QAction(QIcon("delete.png"), "Delete", self)
        edit_menu.addAction(deleteAction)
        deleteAction.setShortcut("Del")
        
        changeAction =QAction(QIcon("change.png"), "Change Channel...", self)
        edit_menu.addAction(changeAction)

        typeAction =QAction(QIcon("color.png"), "Change Type", self)
        edit_menu.addAction(typeAction)

        insertAction =QAction(QIcon("add.png"), "Insert Over", self)
        edit_menu.addAction(insertAction)
        insertAction.setShortcut("Ctrl+l")        

        edit_menu.addAction('Quit',self.close)
                
        # menubar  mode
        mode_menu = menuBar.addMenu('mode')

        newAction =QAction(QIcon("new event.png"), "New Event", self)
        mode_menu.addAction(newAction)
        redoAction.setShortcut("Ctrl+1")

        editAction =QAction(QIcon("edit.png"), "Edit Event", self)
        mode_menu.addAction(editAction)
        redoAction.setShortcut("Ctrl+2")

        scrollAction =QAction(QIcon("scroll.png"), "Scroll", self)
        mode_menu.addAction(scrollAction)
        redoAction.setShortcut("Ctrl+3")

        viewAction =QAction(QIcon("view.png"), "View Options", self)
        mode_menu.addAction(viewAction)
        redoAction.setShortcut("Ctrl+4")

        
        # menubar  view
        view_menu = menuBar.addMenu('view')

        toolbarAction =QAction("Toolbars", self)
        view_menu.addAction(toolbarAction)
        
        statusAction =QAction( "Statusbar", self)
        view_menu.addAction(statusAction)

        animationAction =QAction( "Animation", self)
        view_menu.addAction(animationAction)

        eveAction =QAction(QIcon("favourite.png"), "Events...", self)
        view_menu.addAction(eveAction)

        channAction =QAction(QIcon("channels.png"), "Channels...", self)
        view_menu.addAction(channAction)
        
        scaleAction =QAction("Scale All", self)
        view_menu.addAction(scaleAction)

        zoominvAction =QAction(QIcon("zoomin.png"), "Zoom In Vertical", self)
        view_menu.addAction(zoominvAction)
        redoAction.setShortcut("Ctrl+ +")

        zoomoutvAction =QAction(QIcon("zoom out.png"), "Zoom Out Vertical", self)
        view_menu.addAction(zoomoutvAction)
        redoAction.setShortcut("Ctrl+ -")

        zoominhAction =QAction(QIcon("zoomin.png"), "Zoom In Horizontal", self)
        view_menu.addAction(zoominhAction)
        redoAction.setShortcut("Alt+ +")

        zoomouthAction =QAction(QIcon("zoom out.png"), "Zoom Out Horizontal", self)
        view_menu.addAction(zoomouthAction)
        redoAction.setShortcut("Alt+ -")

        gotoAction =QAction(QIcon("goto.png"), "Go to...", self)
        view_menu.addAction(gotoAction)

        gonextAction =QAction( "Goto and Select Next Event", self)
        view_menu.addAction(gonextAction)
        redoAction.setShortcut("Ctrl+ Right")

        goprevAction =QAction("Goto and Select Previos Evenet", self)
        view_menu.addAction(goprevAction)
        redoAction.setShortcut("Ctrl+ Left")

        fitAction =QAction("Fit View to selected Event", self)
        view_menu.addAction(fitAction)

        hideAction =QAction("Hide Events of Other Type", self)
        view_menu.addAction(hideAction)

        showAction =QAction("Show All Events", self)
        view_menu.addAction(showAction)    

        #       view_menu.addAction('Quit',self.close)
        
        # menubar  tools
        tools_menu = menuBar.addMenu('tools')
        
        calcAction =QAction("Calculate Mean...", self)
        tools_menu.addAction(calcAction)

        powerAction =QAction("Power Spectrum...", self)
        tools_menu.addAction(powerAction)

        #        tools_menu.addAction('Quit',self.close)
        
        # menubar  help
        help_menu = menuBar.addMenu('help')
        help_menu.addAction('Quit',self.close)       


    def ToolBar(self):
        AddFile = QAction(QIcon('images.png'),'Open File',self)
        AddFile.triggered.connect(self.OpenBrowse)
        self.toolBar= self.addToolBar('TOOL BAR')
        self.toolBar.addAction(AddFile)
        self.toolBar.setObjectName("toolBar")

        Addplay = QAction(QIcon('play.png'),'play',self)
        Addplay.triggered.connect(self.dynamicSig)
        self.toolBar= self.addToolBar('play')
        self.toolBar.addAction(Addplay)
        Addplay.setShortcut("Ctrl+p")

        Addpause = QAction(QIcon('pause.jpg'),'pause',self)
        Addpause.triggered.connect(self.pauseSignal)
        self.toolBar= self.addToolBar('pause')
        self.toolBar.addAction(Addpause)
        Addpause.setShortcut("Ctrl+shift+p")

        Addclear = QAction(QIcon('clear.jpg'),'clear',self)
        Addclear.triggered.connect(self.clear)
        self.toolBar= self.addToolBar('clear')
        self.toolBar.addAction(Addclear)
        Addclear.setShortcut("Ctrl+i")
        
        Addzoomin = QAction(QIcon('zoomin.png'),'zoomin',self)
        Addzoomin.triggered.connect(self.zoom_in)
        self.toolBar= self.addToolBar('zoomin')
        self.toolBar.addAction(Addzoomin)
        Addzoomin.setShortcut("Ctrl+T")

        Addzoomout = QAction(QIcon('zoomout.jpg'),'zoomout',self)
        Addzoomout.triggered.connect(self.zoom_out)
        self.toolBar= self.addToolBar('zoomout')
        self.toolBar.addAction(Addzoomout)
        Addzoomout.setShortcut("Ctrl+H")

        AddscrollR = QAction(QIcon('arrowrjpg.jpg'),'scroll Right',self)
        AddscrollR.triggered.connect(self.scrollR)
        self.toolBar= self.addToolBar('scroll Right')
        self.toolBar.addAction(AddscrollR)
        AddscrollR.setShortcut("Ctrl+R")

        AddscrollL = QAction(QIcon('arrowl.png'),'scroll left',self)
        AddscrollL.triggered.connect(self.scrollL)
        self.toolBar= self.addToolBar('scroll Right')
        self.toolBar.addAction(AddscrollL)
        Addzoomout.setShortcut("Ctrl+D")

    def scrollR(self):
        xrange, yrange = self.sc.viewRange()
        scrollvalue = (xrange[1] - xrange[0])/10
        self.sc.setXRange(xrange[0]+scrollvalue, xrange[1]+scrollvalue, padding=0)
        self.sc.setYrange(yrange[0],yrange[1], padding=0)


    def scrollL(self):
        xrange, yrange = self.sc.viewRange()
        scrollvalue = (xrange[1] - xrange[0])/10
        self.sc.setXRange(xrange[0]-scrollvalue, xrange[1]-scrollvalue, padding=0)
        self.sc.setYrange(yrange[0],yrange[1], padding=0)

    def zoom_in(self):
        xrange, yrange = self.sc.viewRange()
        self.sc.setYRange(yrange[0]/2, yrange[1]/2, padding=0)
        self.sc.setXRange(xrange[0]/2, xrange[1]/2, padding=0)

    

    def zoom_out(self):
        xrange, yrange = self.sc.viewRange()
        self.sc.setYRange(yrange[0]*2, yrange[1]*2, padding=0)
        self.sc.setXRange(xrange[0]*2, xrange[1]*2, padding=0)
    # def spectro(self):
        # self.frequencies = np.arange(5,105,5)

    def printDialog(self):
        printer= QPrinter(QPrinter.HighResolution)
        dialog= QPrintDialog(printer, self)

        if dialog.exec_()== QPrinter.Accepted:
            self.graphicsview.print_(printer)



    def pdfExport(self):
        fn, _= QFileDialog.getSaveFileName(self, "Export PDF", None, "PDF files (.pdf);;All Files()" )
        
        if fn !='':

            if QFileInfo(fn).suffix() == "" :fn += '.pdf'

            printer = QPrinter(QPrinter.HighResolution)
            printer.setOutputFormat(QPrinter.PdfFormat)
            printer.setOutputFileName(fn)
            self.graphicsview.document().print_(printer)

    def Plot(self):
        self.sc.plot(self.x1[: self.l1], self.y1[: self.l1])
        # self.sc.plot.setLabel('bottom', 'time in sec')
        # self.sc.plot.setLabel('left', 'volt in mv')

        self.l1 +=10
        if self.l1 > len(self.x1):
            self.l1 = 10
        


    def OpenBrowse(self):
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","CSV Files (*.csv)")
        if fileName: 
            df=pd.read_csv(fileName,header=None)
            # df=pd.read_csv("ECG22 CSV.csv",header=None,nrows=10000)
            self.x=np.array(df[0])
            # self.x1=self.x.tolist() #list
            self.y=np.array(df[1]) 
            # self.y1=self.y.tolist() #list
            # self.y2=[self.y1[i] for i in range (len(self.y1))]
            # self.z=[self.b[i] for i in range (10000)]
            # self.i = 0
            xrange, yrange = self.sc.viewRange()
            self.sc.setXRange(xrange[0]/5, xrange[1]/5, padding=0)
            # self.sc.setYRange(yrange[0]/100, yrange[1]/100, padding=0)
            pen = pg.mkPen(color=(50, 50, 250))
            self.data_line =  self.sc.plot(self.x, self.y, pen=pen)
#        self.Plot()
    def clear(self):
        self.sc.clear()
    def dynamicSig(self):
        # self.clear()
        self.timer = QtCore.QTimer()
        self.timer.setInterval(5)
        self.timer.timeout.connect(self.dynamicSig)
        self.timer.start()
        xrange, yrange = self.sc.viewRange()
        scrollvalue = (xrange[1] - xrange[0])/500
        self.sc.setXRange(xrange[0]+scrollvalue, xrange[1]+scrollvalue, padding=0)


        # self.x1 = self.x1[1:]
        # self.x1.append(self.x1[-1] + 1)

        # self.y2 = self.y2[1:]
       
        # self.y2.append(self.y[self.i]) 
        # self.i = self.i + 1 
        # self.sc.plot(self.x1[0:self.i], self.y2[0:self.i])
    def pauseSignal(self):
        self.timer.stop()


app = QApplication(sys.argv)
sheet= mainwind()
sheet.show()
sheet.setWindowTitle("Sigviewer")
sheet.setWindowIcon(QIcon("icon.png"))
sys.exit(app.exec_())

