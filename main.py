import sys
from PyQt5 import QtCore, QtPrintSupport, QtGui
from PyQt5.QtWidgets import *
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from lib.utils import calculateMakespan
from lib.CDS import CDS
from lib.Td2 import Td2H1, Td2H2, Td2H3

tabColors = [
    "tab:blue",
    "tab:orange",
    "tab:green",
    "tab:red",
    "tab:purple",
    "tab:brown",
    "tab:pink",
    "tab:gray",
    "tab:olive",
    "tab:cyan",
]

class Window(QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle(self.tr("MES Project By Reda Zitouni"))
        self.initUI()
        self.stackedWidget.currentChanged.connect(self.SetButtonState)
        self.next_button.clicked.connect(self.gotoNextPage)
        self.prev_button.clicked.connect(self.gotoPrevPage)
    

    def SetButtonState(self, index):
        self.prev_button.setEnabled(index > 0)
        nPages = len(self.stackedWidget)
        self.next_button.setEnabled( index % nPages < nPages - 1)


    def insertPage(self, widget, index=-1):
        self.stackedWidget.insertWidget(index, widget)
        self.SetButtonState(self.stackedWidget.currentIndex())


    def gotoNextPage(self):
        newIndex = self.stackedWidget.currentIndex() + 1
        if newIndex < len(self.stackedWidget):
            self.stackedWidget.setCurrentIndex(newIndex)


    def gotoPrevPage(self):
        newIndex = self.stackedWidget.currentIndex()-1
        if newIndex >= 0:
            self.stackedWidget.setCurrentIndex(newIndex)


    def initUI(self):
        self.next_button = QPushButton('Next')
        self.prev_button = QPushButton('Previous')
        self.next_button.setEnabled(False)
        self.prev_button.setEnabled(False)
        self.stackedWidget = QStackedWidget()

        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(self.prev_button)
        hbox.addWidget(self.next_button)

        vbox = QVBoxLayout()
        vbox.addWidget(self.stackedWidget)
        vbox.addLayout(hbox)

        self.testWindow = QWidget()
        self.firstPageGrid = QGridLayout(self)

        self.mainTable = QTableWidget(2, 4, self)
        self.fillTableWithZeros(self.mainTable)
        self.setHeaders(self.mainTable)

        self.buttonAddRow = QPushButton("Add a line", self)
        self.buttonRemoveRow = QPushButton("Delete a line", self)
        self.buttonAddColumn = QPushButton("Add a Column", self)
        self.buttonRemoveColumn = QPushButton("Delete a Column", self)

        self.delayCheckbox = QCheckBox("Deadlines", self)
        # self.preparationCheckbox = QCheckBox("Preparation", self)

        self.dropdownMenu = QComboBox()
        self.dropdownMenu.addItem("CDS")
        self.dropdownMenu.addItem("Td2H1")

        self.buttonSolve = QPushButton("Solve", self)

        self.testWindow.setLayout(self.firstPageGrid)

        self.firstPageGrid.addWidget(self.buttonAddRow, 0, 0, 1, 2)
        self.firstPageGrid.addWidget(self.buttonRemoveRow, 0, 2, 1, 2)
        self.firstPageGrid.addWidget(self.buttonAddColumn, 0, 4, 1, 2)
        self.firstPageGrid.addWidget(self.buttonRemoveColumn, 0, 6, 1, 2)
        self.firstPageGrid.addWidget(self.mainTable, 1, 0, 3, 8)
        self.firstPageGrid.addWidget(self.delayCheckbox, 4, 0, 1, 8)
        # self.firstPageGrid.addWidget(self.preparationCheckbox, 6, 0, 1, 8)
        self.firstPageGrid.addWidget(self.dropdownMenu, 8, 0, 1, 4)
        self.firstPageGrid.addWidget(self.buttonSolve, 8, 4, 1, 4)

        self.buttonAddRow.clicked.connect(self.addRow)
        self.buttonRemoveRow.clicked.connect(self.removeRow)
        self.buttonAddColumn.clicked.connect(self.addColumn)
        self.buttonRemoveColumn.clicked.connect(self.removeColumn)
        self.delayCheckbox.stateChanged.connect(self.toggleDelayTable)
        # self.preparationCheckbox.stateChanged.connect(self.togglePreparationTable)
        self.buttonSolve.clicked.connect(self.solve)

        self.stackedWidget.insertWidget(0, self.testWindow)

        self.setLayout(vbox)


    def addRow(self):
        self.mainTable.insertRow(self.mainTable.rowCount())
        for col in range(self.mainTable.columnCount()):
            item = QTableWidgetItem('0')
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            self.mainTable.setItem(self.mainTable.rowCount() - 1, col, item)
        self.setHeaders(self.mainTable)


    def removeRow(self):
        if self.mainTable.rowCount() > 0:
            self.mainTable.removeRow(self.mainTable.rowCount() - 1)
        self.setHeaders(self.mainTable)


    def addColumn(self):
        self.mainTable.insertColumn(self.mainTable.columnCount())
        for row in range(self.mainTable.rowCount()):
            item = QTableWidgetItem('0')
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            self.mainTable.setItem(row, self.mainTable.columnCount() - 1, item)
        self.setHeaders(self.mainTable)


    def removeColumn(self):
        if self.mainTable.columnCount() > 0:
            self.mainTable.removeColumn(self.mainTable.columnCount() - 1)
        self.setHeaders(self.mainTable)

    
    def fillTableWithZeros(self, table):
        for row in range(table.rowCount()):
            for col in range(table.columnCount()):
                item = QTableWidgetItem("0")
                item.setTextAlignment(QtCore.Qt.AlignCenter)
                table.setItem(row, col, item)


    def setHeaders(self, table):
        columnsHeaders = "|".join(
            f"J{column+1}" for column in range(table.columnCount())
        )
        rowsHeaders = "|".join(
            f"M{row+1}" for row in range(table.rowCount())
        )
        table.setHorizontalHeaderLabels(
            columnsHeaders.split("|")
        )
        table.setVerticalHeaderLabels(
            rowsHeaders.split("|")
        )


    def toggleDelayTable(self):
        if self.delayCheckbox.isChecked():
            self.dropdownMenu.addItem("Td2H2")
            self.dropdownMenu.addItem("Td2H3")

            nColumns = self.mainTable.columnCount()
            self.delayTable = QTableWidget(1, nColumns, self)
            self.fillTableWithZeros(self.delayTable)

            columnsHeaders = '|'.join(
                f"J{column+1}" for column in range(self.delayTable.columnCount())
            )
            self.delayTable.setHorizontalHeaderLabels(
                columnsHeaders.split('|')
            )
            self.delayTable.setVerticalHeaderLabels(
                ['']
            )
            self.firstPageGrid.addWidget(self.delayTable, 5, 0, 1, 8)
        else:
            for _ in range(2):
                self.dropdownMenu.removeItem(self.dropdownMenu.count() - 1)
            self.firstPageGrid.removeWidget(self.delayTable)
            self.delayTable.deleteLater()
            # self.delayTable = None


    # def togglePreparationTable(self):
    #     if self.preparationCheckbox.isChecked():
    #         self.preparationTable = QTableWidget(1, 4, self)
    #         self.fillTableWithZeros(self.preparationTable)
    #         self.firstPageGrid.addWidget(self.preparationTable, 7, 0, 1, 8)
    #     else:
    #         self.firstPageGrid.removeWidget(self.preparationTable)
    #         self.preparationTable.deleteLater()
    #         # self.preparationTable = None


    def readInputs(self, table):
        nRows = table.rowCount()
        nColumns = table.columnCount()
        machines = []

        for row in range(nRows):
            d = []
            for col in range(nColumns):
                item = table.item(row, col)
                d += int(item.text()),
            if nRows == 1:
                machines = d
            else:
                machines += d,

        return machines

    
    def orderMachines(self):
        nRows = self.mainTable.rowCount()

        orderedMachines = []
        for i in range(nRows):
            lst = []
            for j in self.solution.order:
                lst += self.machines[i][j],
            orderedMachines += lst,
        return orderedMachines


    def calculateTotalMakespans(self):
        nRows = self.mainTable.rowCount()
        nColumns = self.mainTable.columnCount()
        makespans = []

        for i in range(nRows):
            result = []
            for j in range(nColumns):
                result += (calculateMakespan(self.orderedMachines, i, j), self.orderedMachines[i][j]),
            makespans += result,
        cMax = makespans[-1][-1][0] + makespans[-1][-1][1]

        return makespans, cMax


    def drawGanttChart(self):
        # Set the figure size
        plt.rcParams["figure.figsize"] = [7.50, 3.50]
        plt.rcParams["figure.autolayout"] = True

        # Figure and set of subplots
        self.ganttFigure, self.ganttAx = plt.subplots()

        # Horizontal sequence of rectangles
        startIndex = 5
        for index, makespan in enumerate(self.makespans[::-1]):
            color = tabColors[index % len(tabColors)]
            self.ganttAx.broken_barh(makespan, (startIndex, 9), facecolors=color, edgecolor="black")
            
            self.ganttAx.text(
                x = -1.5, 
                y = startIndex + 4.5,
                s = f"M{len(self.makespans) - index}", 
                ha = "center", 
                va = "center",
                color = "black",
            )
    
            for order, (x1, x2) in enumerate(makespan):
                self.ganttAx.text(
                    x = x1 + x2 / 2, 
                    y = startIndex + 4.5,
                    s = f"J{self.solution.order[order] + 1}", 
                    ha = "center", 
                    va = "center",
                    color = "black",
                )
                
            startIndex += 10

        # ylim and xlim of the axes
        self.ganttAx.set_ylim(0, startIndex + 5)
        self.ganttAx.set_yticks([])
        
        self.ganttAx.set_xlim(0, self.makespans[-1][-1][0] + self.makespans[-1][-1][1] + 5)

        self.canvas = FigureCanvas(self.ganttFigure)
        self.toolbar = NavigationToolbar(self.canvas, self)
        
        # Show the plot
        # plt.show()
    

    def drawTfrChart(self):
        self.tfrFigure, self.tfrAx = plt.subplots()
        # self.tfrAx = self.tfrFigure.add_axes([0,0,1,1])
        machines = [f"M{i + 1}" for i in range(len(self.machines))]
        tfrList = [sum(machine) / self.cMax for machine in self.machines]
        # tfrList = [round(sum(machine) / self.cMax, 2) for machine in self.machines]
        self.tfrAx.bar(machines, tfrList)
        for index, value in enumerate(tfrList):
            label = f"{round(value * 100, 2)}%"
            plt.text(index - len(label) / (2 * 100), value + .03, label)
        self.tfrAx.set_ylim(0, 1)
        # self.ax.set_xlim(0, len(self.machines))
        self.tfrFigure.set_tight_layout(False)
        self.canvas2 = FigureCanvas(self.tfrFigure)
        self.toolbar2 = NavigationToolbar(self.canvas2, self)


    def drawTarChart(self):
        self.tarFigure, self.tarAx = plt.subplots()
        # self.tarAx = self.tarFigure.add_axes([0,0,1,1])
        machines = [f"M{i + 1}" for i in range(len(self.machines))]
        tarList = [ 1 - sum(machine) / self.cMax for machine in self.machines]
        # tarList = [round(sum(machine) / self.cMax, 2) for machine in self.machines]
        self.tarAx.bar(machines, tarList)
        for index, value in enumerate(tarList):
            label = f"{round(value * 100, 2)}%"
            plt.text(index - len(label) / (2 * 100), value + .03, label)
        self.tarAx.set_ylim(0, 1)
        # self.ax.set_xlim(0, len(self.machines))
        self.tarFigure.set_tight_layout(False)
        self.canvas3 = FigureCanvas(self.tarFigure)
        self.toolbar3 = NavigationToolbar(self.canvas3, self)
    

    def addChartToChartsStack(self, stack, toolbar, canvas):
        chartWidget = QWidget()
        chartGrid = QGridLayout()
        chartGrid.addWidget(toolbar, 0, 1, 1, 8)
        chartGrid.addWidget(canvas, 1, 1, 1, 8)

        chartWidget.setLayout(chartGrid)

        # stack.insertWidget(len(chartslist) - 1, chartWidget)
        stack.addWidget(chartWidget)
    

    def displayCharts(self):
        try:
            self.stackedWidget.removeWidget(self.chartsWindow)
        except:
            pass

        # closing figures to avoid memory consumption
        try:
            plt.close(self.ganttFigure)
            plt.close(self.tfrFigure)
            plt.close(self.tarFigure)
        except:
            pass

        self.drawGanttChart()
        self.drawTfrChart()
        self.drawTarChart()

        self.chartsWindow = QWidget()
        self.chartsLayout = QGridLayout()
        
        self.chartsWindow.setLayout(self.chartsLayout)

        self.ganttChartButton = QPushButton("Gantt", self)
        self.tfrChartButton = QPushButton("TFR", self)
        self.tarChartButton = QPushButton("TAR", self)

        self.sequence = ", ".join(f"J{x + 1}" for x in self.solution.order)
        sequenceText = f"σ = [{self.sequence}]"
        cMaxButtonText = f"Cmax = {self.cMax}" 
        self.sequenceButton = QPushButton(sequenceText, self)
        self.cMaxButton = QPushButton(cMaxButtonText, self)

        self.ChartsStack = QStackedWidget()
        # self.charts = []
        self.addChartToChartsStack(self.ChartsStack, self.toolbar, self.canvas)
        self.addChartToChartsStack(self.ChartsStack, self.toolbar2, self.canvas2)
        self.addChartToChartsStack(self.ChartsStack, self.toolbar3, self.canvas3)

        self.chartsLayout.addWidget(self.ganttChartButton, 0, 2, 1, 2)
        self.chartsLayout.addWidget(self.tfrChartButton, 0, 4, 1, 2)
        self.chartsLayout.addWidget(self.tarChartButton, 0, 6, 1, 2)
        self.chartsLayout.addWidget(self.ChartsStack, 1, 1, 1, 8)
        self.chartsLayout.addWidget(self.sequenceButton, 2, 1, 1, 8)
        self.chartsLayout.addWidget(self.cMaxButton, 3, 1, 1, 8)

        self.ganttChartButton.clicked.connect(self.ffffff)
        self.tfrChartButton.clicked.connect(self.tttttt)
        self.tarChartButton.clicked.connect(self.vvvvvv)

        self.insertPage(self.chartsWindow, 1)
        self.stackedWidget.setCurrentIndex(1)


    def ffffff(self):
        self.ChartsStack.setCurrentIndex(0)


    def tttttt(self):
        self.ChartsStack.setCurrentIndex(1)


    def vvvvvv(self):
        self.ChartsStack.setCurrentIndex(2)


    def printResults(self):
        self.orderedMachines = self.orderMachines()
        self.makespans, self.cMax = self.calculateTotalMakespans()
        self.displayCharts()


    # def solve(self, cls):
    #     self.machines = self.readInputs(self.mainTable)
    #     chosenMethod = self.dropdownMenu.currentIndex()
    #     algos = [
    #         CDS,
    #         Td2H1,
    #         Td2H2,
    #         Td2H3,
    #     ]
    #     self.solution = algos[chosenMethod](self.machines)
    #     self.printResults()
    def solve(self):
        chosenMethod = self.dropdownMenu.currentIndex()
        self.machines = self.readInputs(self.mainTable)

        if chosenMethod == 0:
            self.solution = CDS(self.machines)
        elif chosenMethod == 1:
            self.solution = Td2H1(self.machines)
        else:
            # try:
            #     deadlines = self.readInputs(self.delayTable)
            # except:
            #     deadlines = [1 for i in range(self.mainTable.columnCount())]
            deadlines = self.readInputs(self.delayTable)

            if chosenMethod == 2:
                self.solution = Td2H2(deadlines)   
            elif chosenMethod == 3:
                self.solution = Td2H3(self.machines, deadlines)   

        self.printResults()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    # for i in range(5):
    #     window.insertPage(QLabel(f'This is page {i+1}'))
    window.resize(960, 720)
    window.show()
    app.exec()
    # sys.exit(app.exec())