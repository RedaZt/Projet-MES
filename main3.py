import sys
from PyQt5 import QtCore, QtPrintSupport, QtGui
from PyQt5.QtWidgets import *
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from algorithms.Johnson import Johnson
from algorithms.Td2H1 import Td2H1
from algorithms.Td2H2 import Td2H2
from algorithms.Td2H3 import Td2H3

class Window(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()
        self.stackedWidget.currentChanged.connect(self.set_button_state)
        self.next_button.clicked.connect(self.nextPage)
        self.prev_button.clicked.connect(self.prevPage)


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
        self.page1()

        self.setLayout(vbox)


    def addRow(self):
        self.mainTable.insertRow(self.mainTable.rowCount())
        for col in range(self.mainTable.columnCount()):
            item = QTableWidgetItem('0')
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            self.mainTable.setItem(self.mainTable.rowCount() - 1, col, item)
        self.setHeaders(self.mainTable)

    def removeRow(self):
        if  self.mainTable.rowCount() > 0 :
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
        if  self.mainTable.columnCount() > 0 :
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


    def readInputs(self, table):
        nRows = table.rowCount()
        nColumns = table.columnCount()
        machines = []

        for row in range(nRows):
            d = []
            for col in range(nColumns):
                item = table.item(row, col)
                d += (int(item.text()),)
            if nRows == 1:
                machines = d
            else:
                machines += (d,)

        return machines


    # def solve(self, cls):
    #     machines = self.readInputs(self.mainTable)
    #     self.solution = cls(machines)
    #     self.printResults()
    def solve(self):
        chosenMethod = self.dropdownMenu.currentIndex()
        machines = self.readInputs(self.mainTable)

        if chosenMethod == 0:
            self.solution = Td2H1(machines)
        else:
            try:
                deadlines = self.readInputs(self.delayTable)
            except:
                deadlines = [1 for i in range(self.mainTable.columnCount())]
            if chosenMethod == 1:
                self.solution = Td2H2(deadlines)   
            elif chosenMethod == 2:
                self.solution = Td2H3(machines, deadlines)   
        self.printResults()


    def printResults(self):
        nRows = self.mainTable.rowCount()
        nColumns = self.mainTable.columnCount()

        self.resTable = QTableWidget(nRows, nColumns, self)
        machines = self.readInputs(self.mainTable)
        order = self.solution.order
        res = []

        for machine in machines:
            d = [machine[order[i]] for i in range(len(order))]
            res += d

        for row in range(nRows):
            for col in range(nColumns):
                item = QTableWidgetItem(str(res[row * nColumns + col]))
                item.setTextAlignment(QtCore.Qt.AlignCenter)
                self.resTable.setItem(row, col, item)

        self.drawChart()

    
    def drawChart(self):
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
        nColumns = self.mainTable.columnCount()
        machines = [*self.readInputs(self.resTable)]
        results = []

        for i in range(len(machines)):
            result = []
            if i == 0:
                for j in range(nColumns):
                    result += ((self.calculateM(i, j), machines[i][j]),)
            else:
                for j in range(nColumns):
                    result += ((self.calculateM(i, j), machines[i][j]),)
            results += (result,)

        # Set the figure size
        plt.rcParams["figure.figsize"] = [7.50, 3.50]
        plt.rcParams["figure.autolayout"] = True

        # Figure and set of subplots
        self.figure, self.ax = plt.subplots()

        # Horizontal sequence of rectangles
        startIndex = 5
        for index, result in enumerate(results[::-1]):
            color = tabColors[index % len(tabColors)]
            self.ax.broken_barh(result, (startIndex, 9), facecolors=color, edgecolor="black")
            
            self.ax.text(
                x = -1.5, 
                y = startIndex + 4.5,
                s = f"M{len(results) - index}", 
                ha = "center", 
                va = "center",
                color = "black",
            )
    
            for order, (x1, x2) in enumerate(result):
                self.ax.text(
                    x = x1 + x2/2, 
                    y = startIndex + 4.5,
                    s = f"J{self.solution.order[order] + 1}", 
                    ha = "center", 
                    va = "center",
                    color = "black",
                )
                
            startIndex += 10

        # ylim and xlim of the axes
        self.ax.set_ylim(0, startIndex + 5)
        self.ax.set_yticks([])
        
        self.ax.set_xlim(0, results[-1][-1][0] + results[-1][-1][1] + 5)
        
        # Show the plot
        # plt.show()

        # self.oTabWidget = QTabWidget()
        self.chartWindow = QWidget()
        self.chartLayout = QGridLayout()
        # setting this layout to the widget
        self.chartWindow.setLayout(self.chartLayout)
        # this is the Canvas Widget that
        # displays the 'figure'it takes the
        # 'figure' instance as a parameter to __init__
        self.canvas = FigureCanvas(self.figure)
        # this is the Navigation widget
        # it takes the Canvas widget and a parent
        self.toolbar = NavigationToolbar(self.canvas, self)
        buttonText = ", ".join(f"J{x + 1}" for x in self.solution.order)
        self.sequence = QPushButton(f"σ = [{buttonText}]", self)

        self.chartLayout.addWidget(self.toolbar)
        self.chartLayout.addWidget(self.canvas)
        self.chartLayout.addWidget(self.sequence)

        self.insertPage(self.chartWindow, 1)
        self.stackedWidget.setCurrentIndex(1)

    
    # def calculateM1(self, i):
    #     if i == 0:
    #         return 0
    #     else:
    #         return int(self.resTable.item(0, i - 1).text()) + self.calculateM1(i - 1)


    # def calculateM2(self, i, j):
    #     if j == 0:
    #         if i == 1:
    #             return int(self.resTable.item(i - 1, 0).text())
    #         else:
    #             return self.calculateM2(i - 1, 0) + int(self.resTable.item(i - 1, 0).text())
    #     else:
    #         if i == 1:
    #             return max(
    #                 self.calculateM1(j) + int(self.resTable.item(0, j).text()),
    #                 self.calculateM2(i, j - 1) + int(self.resTable.item(i, j - 1).text()),
    #             )
    #         else:
    #             return max(
    #                 self.calculateM2(i - 1, j) + int(self.resTable.item(i - 1, j).text()),
    #                 self.calculateM2(i, j - 1) + int(self.resTable.item(i, j - 1).text()),
    #             )


    def calculateM(self, i, j):
        if j == 0:
            if i==0:
                return 0
            else:
                return self.calculateM(i - 1, 0) + int(self.resTable.item(i - 1, 0).text())
        else:
            if i == 0:
                return int(self.resTable.item(i, j - 1).text()) + self.calculateM(i, j - 1)
            else:
                return max(
                    self.calculateM(i - 1, j) + int(self.resTable.item(i - 1, j).text()),
                    self.calculateM(i, j - 1) + int(self.resTable.item(i, j - 1).text()),
                )


    def page1(self):
        self.testWindow = QWidget()
        self.firstPageGrid = QGridLayout(self)
        self.mainTable = QTableWidget(2, 4, self)
        self.fillTableWithZeros(self.mainTable)
        self.setHeaders(self.mainTable)

        # self.secondTable = QTableWidget(1, 4, self)
        self.buttonAddRow = QPushButton("Add a line", self)
        self.buttonRemoveRow = QPushButton("Delete a line", self)
        self.buttonAddColumn = QPushButton("Add a Column", self)
        self.buttonRemoveColumn = QPushButton("Delete a Column", self)
        self.delayCheckbox = QCheckBox("Deadlines", self)
        # self.preparationCheckbox = QCheckBox("Preparation", self)
        self.dropdownMenu = QComboBox()
        self.dropdownMenu.addItems(["Td2H1", "Td2H2", "Td2H3"])
        # self.dropdownMenu.addItems(["Johnson", "Td2H1", "Td2H2", "Td2H3"])
        self.buttonSolve = QPushButton("Solve", self)
        # print(self.testCheckbox.isChecked())
        self.delayCheckbox.stateChanged.connect(self.toggleDelayTable)
        # self.preparationCheckbox.stateChanged.connect(self.togglePreparationTable)

        # setting this layout to the widget
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
        # self.dropdownMenu.activated.connect(self.chooseResolutionMethod)
        self.buttonSolve.clicked.connect(self.solve)

        self.stackedWidget.insertWidget(0, self.testWindow)


    def toggleDelayTable(self):
        # print(self.testCheckbox.checkState())
        if self.delayCheckbox.isChecked():
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
            self.firstPageGrid.removeWidget(self.delayTable)
            self.delayTable.deleteLater()
            # self.delayTable = None


    def togglePreparationTable(self):
        if self.preparationCheckbox.isChecked():
            self.preparationTable = QTableWidget(1, 4, self)
            self.fillTableWithZeros(self.preparationTable)
            self.firstPageGrid.addWidget(self.preparationTable, 7, 0, 1, 8)
        else:
            self.firstPageGrid.removeWidget(self.preparationTable)
            self.preparationTable.deleteLater()
            # self.preparationTable = None


    def set_button_state(self, index):
        self.prev_button.setEnabled(index > 0)
        nPages = len(self.stackedWidget)
        self.next_button.setEnabled( index % nPages < nPages - 1)


    def insertPage(self, widget, index=-1):
        self.stackedWidget.insertWidget(index, widget)
        self.set_button_state(self.stackedWidget.currentIndex())


    def nextPage(self):
        newIndex = self.stackedWidget.currentIndex() + 1
        if newIndex < len(self.stackedWidget):
            self.stackedWidget.setCurrentIndex(newIndex)


    def prevPage(self):
        newIndex = self.stackedWidget.currentIndex()-1
        if newIndex >= 0:
            self.stackedWidget.setCurrentIndex(newIndex)


if __name__ == '__main__':

    app = QApplication(sys.argv)
    window = Window()
    # for i in range(5):
    #     window.insertPage(QLabel(f'This is page {i+1}'))
    window.resize(960, 720)
    window.show()
    # app.exec()
    sys.exit(app.exec())