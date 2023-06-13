import sys
import numpy as np
from PyQt5 import QtCore, QtPrintSupport, QtGui
from PyQt5.QtWidgets import *
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import Rectangle
from matplotlib import cm
from matplotlib.cm import get_cmap
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from lib.utils import calculateMakespan, calculateMakespanWithPreparation, calculateMakespanWithBlockage, prep, prepBlo
from lib.CDS import CDS
from lib.CustomSort import CustomSort

class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(self.tr("MES Project By Reda Zitouni"))
        self.initUI()
        self.graphStartingIndex = 5
        self.stackedWidget.currentChanged.connect(self.SetButtonState)
        self.next_button.clicked.connect(self.gotoNextPage)
        self.prev_button.clicked.connect(self.gotoPrevPage)


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
        self.setHeaders(self.mainTable, 'M', 'J')

        self.buttonAddRow = QPushButton("Add a line", self)
        self.buttonRemoveRow = QPushButton("Delete a line", self)
        self.buttonAddColumn = QPushButton("Add a Column", self)
        self.buttonRemoveColumn = QPushButton("Delete a Column", self)

        self.blockageCheckbox = QCheckBox("Blockage", self)
        self.preparationCheckbox = QCheckBox("Preparation", self)
        
        self.dropdownMenu = QComboBox()
        self.dropdownMenu.addItems([
            "CDS",
            # "Td2H1",
            # "Td2H2",
            # "Td2H3",
            # "Ordre de TPj",
            "Custom Order",
        ])

        self.textbox = QLineEdit(self)
        self.textbox.setPlaceholderText("Insert Your Sequence Here. Ex: 1 2 3")
        self.textbox.setDisabled(True)

        self.buttonSolve = QPushButton("Solve", self)

        self.testWindow.setLayout(self.firstPageGrid)

        self.firstPageGrid.addWidget(self.buttonAddRow, 0, 0, 1, 2)
        self.firstPageGrid.addWidget(self.buttonRemoveRow, 0, 2, 1, 2)
        self.firstPageGrid.addWidget(self.buttonAddColumn, 0, 4, 1, 2)
        self.firstPageGrid.addWidget(self.buttonRemoveColumn, 0, 6, 1, 2)
        self.firstPageGrid.addWidget(self.mainTable, 1, 0, 4, 8)
        # self.firstPageGrid.addWidget(self.mainTable, 1, 0, 2, 8)
        self.firstPageGrid.addWidget(self.blockageCheckbox, 5, 0, 1, 8)
        # self.firstPageGrid.addWidget(self.delayCheckbox, 4, 0, 1, 8)
        # self.firstPageGrid.addWidget(self.preparationCheckbox, 6, 0, 1, 8)
        # self.firstPageGrid.addWidget(self.dropdownMenu, 8, 0, 1, 2)
        self.firstPageGrid.addWidget(self.preparationCheckbox, 6, 0, 1, 8)
        self.firstPageGrid.addWidget(self.dropdownMenu, 8, 0, 1, 2)
        self.firstPageGrid.addWidget(self.textbox, 8, 2, 1, 2)
        self.firstPageGrid.addWidget(self.buttonSolve, 8, 4, 1, 4)

        self.buttonAddRow.clicked.connect(self.addRow)
        self.buttonRemoveRow.clicked.connect(self.removeRow)
        self.buttonAddColumn.clicked.connect(self.addColumn)
        self.buttonRemoveColumn.clicked.connect(self.removeColumn)
        # self.delayCheckbox.stateChanged.connect(self.toggleDelayTable)
        self.preparationCheckbox.stateChanged.connect(self.togglePreparationTable)
        # self.dropdownMenu.currentTextChanged.connect(self.activateTextbox)
        self.dropdownMenu.currentIndexChanged.connect(self.activateTextbox)
        self.buttonSolve.clicked.connect(self.solve)

        self.stackedWidget.insertWidget(0, self.testWindow)
        self.setLayout(vbox)
    

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


    def addRow(self):
        self.mainTable.insertRow(self.mainTable.rowCount())
        for col in range(self.mainTable.columnCount()):
            item = QTableWidgetItem('0')
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            self.mainTable.setItem(self.mainTable.rowCount() - 1, col, item)
        self.setHeaders(self.mainTable, 'M', 'J')


    def removeRow(self):
        if self.mainTable.rowCount() > 0:
            self.mainTable.removeRow(self.mainTable.rowCount() - 1)
        self.setHeaders(self.mainTable, 'M', 'J')


    def addColumn(self):
        self.mainTable.insertColumn(self.mainTable.columnCount())
        for row in range(self.mainTable.rowCount()):
            item = QTableWidgetItem('0')
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            self.mainTable.setItem(row, self.mainTable.columnCount() - 1, item)
        self.setHeaders(self.mainTable, 'M', 'J')


    def removeColumn(self):
        if self.mainTable.columnCount() > 0:
            self.mainTable.removeColumn(self.mainTable.columnCount() - 1)
        self.setHeaders(self.mainTable, 'M', 'J')

    
    def fillTableWithZeros(self, table):
        for row in range(table.rowCount()):
            for col in range(table.columnCount()):
                item = QTableWidgetItem("0")
                item.setTextAlignment(QtCore.Qt.AlignCenter)
                table.setItem(row, col, item)


    def setHeaders(self, table, rowText, columnText):
        columnsHeaders = "|".join(
            f"{columnText}{column+1}" for column in range(table.columnCount())
        )
        rowsHeaders = "|".join(
            f"{rowText}{row+1}" for row in range(table.rowCount())
        )
        table.setHorizontalHeaderLabels(
            columnsHeaders.split("|")
        )
        table.setVerticalHeaderLabels(
            rowsHeaders.split("|")
        )


    # def toggleDelayTable(self):
    #     if self.delayCheckbox.isChecked():
    #         # self.dropdownMenu.addItem("Td2H2")
    #         # self.dropdownMenu.addItem("Td2H3")

    #         nColumns = self.mainTable.columnCount()
    #         self.delayTable = QTableWidget(1, nColumns, self)
    #         self.fillTableWithZeros(self.delayTable)

    #         columnsHeaders = '|'.join(
    #             f"J{column+1}" for column in range(self.delayTable.columnCount())
    #         )
    #         self.delayTable.setHorizontalHeaderLabels(
    #             columnsHeaders.split('|')
    #         )
    #         self.delayTable.setVerticalHeaderLabels(
    #             ['']
    #         )
    #         self.firstPageGrid.addWidget(self.delayTable, 5, 0, 1, 8)
    #     else:
    #         # for _ in range(2):
    #         #     self.dropdownMenu.removeItem(self.dropdownMenu.count() - 1)
    #         self.firstPageGrid.removeWidget(self.delayTable)
    #         self.delayTable.deleteLater()
    #         # self.delayTable = None


    def togglePreparationTable(self):
        if self.preparationCheckbox.isChecked():
            # self.dropdownMenu.addItem("CDS With Preparation")
            nRows = self.mainTable.rowCount()
            nColumns = self.mainTable.columnCount()
            self.table = QTableWidget()
            self.preparationTabs = QTabWidget()

            self.preparationTablesWidget = QWidget()
            preparationTablesGrid = QGridLayout()
            tables = []
            for i in range(nRows):
                self.preparationTabs.setCurrentIndex(i)
                tables += QTableWidget(nColumns, nColumns, self),
                self.setHeaders(tables[-1], 'J', 'J')
                self.fillTableWithZeros(tables[-1])
                self.preparationTabs.addTab(
                    tables[-1], 
                    f"Machine {i + 1}"
                )
            preparationTablesGrid.addWidget(self.preparationTabs, 0, 0, 1, 8)
            self.preparationTablesWidget.setLayout(preparationTablesGrid)

            # stack.insertWidget(len(chartslist) - 1, chartWidget)
            self.firstPageGrid.addWidget(self.preparationTablesWidget, 7, 0, 1, 8)
        else:
            # self.dropdownMenu.removeItem(self.dropdownMenu.count() - 1)
            self.firstPageGrid.removeWidget(self.preparationTablesWidget)
            self.preparationTablesWidget.deleteLater()
            # self.preparationTable = None
    

    def activateTextbox(self):
        if self.dropdownMenu.currentText() == "Custom Order":
            self.textbox.setDisabled(False)
        else:
            self.textbox.setDisabled(True)


    def solve(self):
        self.readPreparationTables()
        self.machines = self.readTableInputs(self.mainTable)
        chosenMethod = self.dropdownMenu.currentText()
        if chosenMethod == "Custom Order":
            customOrder = self.getCustonOrder()
            self.solution = CustomSort(self.machines, self.preparations, customOrder)
        else:
            algos = {
                "CDS" : CDS,
                # "Td2H1" : Td2H1,
                # "Td2H2" : Td2H2,
                # "Td2H3" : Td2H3,
                # "Ordre de TPj": TPj,
            }
            self.solution = algos[chosenMethod](self.machines, self.preparations)

        self.printResults()    


    def readTableInputs(self, table):
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
    

    def readPreparationTables(self):
        try:
            self.preparations = []
            for i in range(self.preparationTabs.count()):
                table = self.preparationTabs.widget(i)
                res = self.readTableInputs(table)
                self.preparations += res,
        except:
            nRows = self.mainTable.rowCount()
            nColumns = self.mainTable.columnCount()
            self.preparations = [
                [[0 for k in range(nColumns)] for j in range(nColumns)] for i in range(nRows)
            ]
    

    def getCustonOrder(self):
        # customOrder = map(lambda x: int(x.split()), self.textbox.text().split())
        return [*map(lambda x: int(x) - 1, self.textbox.text().split())]
        # print(customOrder)

    
    def orderMachines(self):
        nRows = self.mainTable.rowCount()
        orderedMachines = []

        for i in range(nRows):
            lst = []
            for j in self.solution.order:
            # for j in [4, 2, 0, 3, 1]:
                lst += self.machines[i][j],
            orderedMachines += lst,
        return orderedMachines


    def printResults(self):
        self.orderedMachines = self.orderMachines()
        if self.blockageCheckbox.isChecked():
            self.makespans, self.cMax = self.calculateTotalMakespans(calculateMakespanWithBlockage)
            self.prepTimes = self.calculatePrepTimes(prepBlo)
            self.findBlockage()
        else:
            self.makespans, self.cMax = self.calculateTotalMakespans(calculateMakespanWithPreparation)
            self.prepTimes = self.calculatePrepTimes(prep)

        self.displayCharts()


    def calculateTotalMakespans(self, function):
    # def calculateTotalMakespans(self):
        nRows = self.mainTable.rowCount()
        nColumns = self.mainTable.columnCount()
        makespans = []

        for i in range(nRows):
            result = []
            for j in range(nColumns):
                result += (function(self.orderedMachines, self.preparations, self.solution.order, i, j), self.orderedMachines[i][j]),
            makespans += result,
        cMax = makespans[-1][-1][0] + makespans[-1][-1][1]
        return makespans, cMax
    

    def calculatePrepTimes(self, function):
        nRows = self.mainTable.rowCount()
        nColumns = self.mainTable.columnCount()
        prep = []

        for i in range(nRows):
            result = []
            for j in range(nColumns):
                if j!=0:
                    result += (function(self.orderedMachines, self.preparations, self.solution.order, i, j), self.preparations[i][self.solution.order[j - 1]][self.solution.order[j]]),
                else:
                    result += (function(self.orderedMachines, self.preparations, self.solution.order, i, j), self.preparations[i][self.solution.order[j]][self.solution.order[j]]),
            prep += result,
        return prep
    

    def findBlockage(self):
        self.makespans2, _ = self.calculateTotalMakespans(calculateMakespanWithPreparation)
        self.differences = [[(0, 0) for j in range(len(self.makespans[0]))] for i in range(len(self.makespans))]
        # cumSum = 0
        for i in range(len(self.makespans) - 1):
            cumSum = 0
            for j in range(1, len(self.makespans[0])):
                if self.makespans2[i][j][0] + cumSum != self.makespans[i][j][0] and\
                   (self.makespans[i][j][0] != self.makespans[i][j - 1][0] + self.makespans[i][j - 1][1] and\
                    self.makespans[i][j][0] != self.makespans[i - 1][j][0] + self.makespans[i - 1][j][1]):
                    value = self.makespans[i][j][0] - self.makespans2[i][j][0]
                    difference = value - cumSum if value - cumSum > 0 else 0
                    self.differences[i][j] = (self.makespans2[i][j][0] + cumSum - self.preparations[i][self.solution.order[j - 1]][self.solution.order[j]], difference)
                    cumSum += value
                if i != len(self.makespans) - 1:
                    if self.makespans[i][j][0] + self.makespans[i][j][1] != self.makespans[i + 1][j][0]:
                        difference = self.makespans[i + 1][j][0] - self.makespans[i][j][0] - self.makespans[i][j][1]
                        self.differences[i][j] = (self.makespans[i][j][0] + self.makespans[i][j][1], difference)
        # for x in self.differences:
        #     print(x)


    def displayCharts(self):
        try:
            self.stackedWidget.removeWidget(self.chartsWindow)
        except:
            pass

        # closing figures to prevent memory consumption
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
        self.addChartToChartsStack(self.ChartsStack, self.ganttToolbar, self.ganttCanvas)
        self.addChartToChartsStack(self.ChartsStack, self.tfrToolbar, self.tfrCanvas)
        self.addChartToChartsStack(self.ChartsStack, self.tarToolbar, self.tarCanvas)

        self.chartsLayout.addWidget(self.ganttChartButton, 0, 2, 1, 2)
        self.chartsLayout.addWidget(self.tfrChartButton, 0, 4, 1, 2)
        self.chartsLayout.addWidget(self.tarChartButton, 0, 6, 1, 2)
        self.chartsLayout.addWidget(self.ChartsStack, 1, 1, 1, 8)
        self.chartsLayout.addWidget(self.sequenceButton, 2, 1, 1, 8)
        self.chartsLayout.addWidget(self.cMaxButton, 3, 1, 1, 8)

        self.ganttChartButton.clicked.connect(self.showGanttChart)
        self.tfrChartButton.clicked.connect(self.showTfrChart)
        self.tarChartButton.clicked.connect(self.showTarChart)

        self.insertPage(self.chartsWindow, 1)
        self.stackedWidget.setCurrentIndex(1)


    def drawGanttChart(self):
        # Set the figure size
        plt.rcParams["figure.figsize"] = [7.50, 3.50]
        plt.rcParams["figure.autolayout"] = True

        # Figure and set of subplots
        self.ganttFigure, self.ganttAx = plt.subplots()

        # Add legend
        self.addGraphLegend()

        # Setting the colors
        colors = cm.rainbow(np.linspace(0, 3, 3*len(self.makespans[0])))
        # name = "Accent"
        # cmap = get_cmap(name)  # type: matplotlib.colors.ListedColormap
        # colors = cmap.colors  # type: list
        # axes.set_prop_cycle(color=colors)

        for index, makespan in enumerate(self.makespans[::-1]):
            self.ganttAx.broken_barh(makespan, (self.graphStartingIndex + index * 10, 9), facecolors=colors, edgecolor="black")
            self.ganttAx.text(
                x = -1.5, 
                y = self.graphStartingIndex + index * 10 + 4.5,
                s = f"M{len(self.makespans) - index}", 
                ha = "center", 
                va = "center",
                color = "black",
            )
            for order, (x1, x2) in enumerate(makespan):
                self.ganttAx.text(
                    x = x1 + x2 / 2, 
                    y = self.graphStartingIndex + index * 10 + 4.5,
                    s = f"J{self.solution.order[order] + 1}", 
                    ha = "center", 
                    va = "center",
                    color = "black",
                )

        # ylim and xlim of the axes
        self.ganttAx.set_ylim(0, self.graphStartingIndex + 10 * len(self.makespans) + 5)
        self.ganttAx.set_yticks([])  
        self.ganttAx.set_xlim(0, self.makespans[-1][-1][0] + self.makespans[-1][-1][1] + 5)

        self.ganttCanvas = FigureCanvas(self.ganttFigure)
        self.ganttToolbar = NavigationToolbar(self.ganttCanvas, self)
    

    def drawPatches(self, data, pattern, color):
        self.graphStartingIndex = 5
        for index, makespan in enumerate(data[::-1]):
            # self.ganttAx.broken_barh(makespan, (self.graphStartingIndex, 9), facecolors="red", edgecolor="red")
            # self.ganttAx.barh(y=self.graphStartingIndex, width=makespan[1], left=makespan[0], height=5, color="maroon")
            # ax.barh(labels, widths, left=starts, height=0.5,label=colname, color=color)
            for x in makespan:
                self.ganttAx.add_patch(
                    Rectangle(
                        [x[0], self.graphStartingIndex + index * 10],
                        width=x[1], 
                        height=9,
                        hatch=pattern,
                        facecolor=color
                    )
                )
    

    def addGraphLegend(self):
        handles = []
        if self.blockageCheckbox.isChecked():
            blockagePattern = "\\\\\\"
            blockageColor = "red"
            self.drawPatches(self.differences, blockagePattern, blockageColor)
            blockageLegend = mpatches.Patch(facecolor=blockageColor, hatch=blockagePattern, label="Blockage")
            handles += blockageLegend,
        if self.preparationCheckbox.isChecked():
            prepPattern = "///"
            prepColor = "lightgray"
            self.drawPatches(self.prepTimes, prepPattern, prepColor)
            prepLegend = mpatches.Patch(facecolor=prepColor, hatch=prepPattern, label="Preparation")
            handles += prepLegend,
        if handles:
            self.ganttAx.legend(handles=handles, loc ="upper left")


    def drawTfrChart(self):
        self.tfrFigure, self.tfrAx = plt.subplots()
        machines = [f"M{i + 1}" for i in range(len(self.machines))]
        tfrList = [sum(machine) / self.cMax for machine in self.machines]
        self.tfrAx.bar(machines, tfrList)

        for index, value in enumerate(tfrList):
            label = f"{round(value * 100, 2)}%"
            self.tfrAx.text(index - len(label) / (2 * 100), value + .03, label)

        self.tfrAx.set_ylim(0, 1)
        self.tfrFigure.set_tight_layout(False)
        self.tfrCanvas = FigureCanvas(self.tfrFigure)
        self.tfrToolbar = NavigationToolbar(self.tfrCanvas, self)


    def drawTarChart(self):
        self.tarFigure, self.tarAx = plt.subplots()
        machines = [f"M{i + 1}" for i in range(len(self.machines))]
        tarList = [ 1 - sum(machine) / self.cMax for machine in self.machines]

        self.tarAx.bar(machines, tarList)
        for index, value in enumerate(tarList):
            label = f"{round(value * 100, 2)}%"
            plt.text(index - len(label) / (2 * 100), value + .03, label)

        self.tarAx.set_ylim(0, 1)
        self.tarFigure.set_tight_layout(False)
        self.tarCanvas = FigureCanvas(self.tarFigure)
        self.tarToolbar = NavigationToolbar(self.tarCanvas, self)
    

    def addChartToChartsStack(self, stack, toolbar, canvas):
        chartWidget = QWidget()
        chartGrid = QGridLayout()
        chartGrid.addWidget(toolbar, 0, 1, 1, 8)
        chartGrid.addWidget(canvas, 1, 1, 1, 8)

        chartWidget.setLayout(chartGrid)
        stack.addWidget(chartWidget)


    def showGanttChart(self):
        self.ChartsStack.setCurrentIndex(0)


    def showTfrChart(self):
        self.ChartsStack.setCurrentIndex(1)


    def showTarChart(self):
        self.ChartsStack.setCurrentIndex(2)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    # for i in range(5):
    #     window.insertPage(QLabel(f'This is page {i+1}'))
    window.resize(960, 720)
    window.show()
    app.exec()
    # sys.exit(app.exec())