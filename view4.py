import csv
import os
import sys
from PyQt5.uic.properties import QtCore
from PyQt5 import QtCore
import numpy as np
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
        
        open_action.triggered.connect(self.open_sheet)
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
        AddFile.triggered.connect(self.open_sheet)
        self.toolBar= self.addToolBar('TOOL BAR')
        self.toolBar.addAction(AddFile)
        self.toolBar.setObjectName("toolBar")

        # AddPlot = QAction(QIcon('Scatter.png'),'Scatter',self)
        # AddPlot.triggered.connect(self.Plot)
        # self.toolBar= self.addToolBar('Add plot')
        # self.toolBar.addAction(AddPlot)

    def printDialog(self):
        printer= QPrinter(QPrinter.HighResolution)
        dialog= QPrintDialog(printer, self)

        if dialog.exec_()== QPrinter.Accepted:
            self.graphicsview.print_(printer)

#    def printPreviewDialog(self):
#        printer=QPrinter(QPrinter.HighResolution)
#        previewDialog= QPrintPreviewDialog(printer, self)
#        previewDialog.paintRequested.connect(self.printPreview)
#        previewDialog.exec_()

#   def printPreview(self,printer):
#        self.graphicsview.print_(printer)

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
        self.l1 +=10
        if self.l1 > len(self.x1):
            self.l1 = 10
        


    def open_sheet(self):
        path = QFileDialog.getOpenFileName(self, "Open", "", "CSV Files (*.csv);;All Files (*)")
        if path[0]!='':
            path_a=self.FileN=path[0]
        self.timer.start()
        self.l1= 10
        data=np.genfromtxt(path_a, delimiter = ' ')
        x1=data[: , 0]   
        y1 =data[:,1]     
        #index = int(self.lineEdit.text())
        self.x1= list(x1)
        self.y1= list(y1)
        self.timer.setInterval(10)
        self.timer.timeout.connect(lambda: self.Plot())
        self.timer.start()
#        self.Plot()

    

# class myCanvas(FigureCanvas):
#     def __init__(self):
#         self.fig=Figure()
#         FigureCanvas.__init__(self,self.fig)

#     def plot(self,xarray,yarray):
#         self.fig.clear()
#         self.ax= self.fig.add_subplot(111)
#         self.ax.plot(xarray[1:],yarray[1:])
#         self.ax.set_xlabel(xarray[0])
#         self.ax.set_ylabel(yarray[0])
#         self.draw()
        

app = QApplication(sys.argv)
sheet= mainwind()
sheet.show()
sheet.setWindowTitle("Sigviewer")
sheet.setWindowIcon(QIcon("icon.png"))
sys.exit(app.exec_())

