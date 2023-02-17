import sys
from PyQt5 import QtWidgets, QtCore, QtPrintSupport, QtGui
from PyQt5.QtWidgets import QDialog, QApplication, QPushButton, QVBoxLayout, QTabWidget
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from algorithms.Johnson import Johnson
from pprint import pprint


class Window(QtWidgets.QWidget):
    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        self.setWindowTitle(self.tr("MES Project By Reda Zitouni"))

        self.mainTable = QtWidgets.QTableWidget(2, 4, self)
        self.setHeadersForMainTable()
        self.fillTableWithZeros(self.mainTable)
        self.textbox = QtWidgets.QLineEdit()

        # self.buttonAddRow = QtWidgets.QPushButton('Add a line', self)
        # self.buttonRemoveRow = QtWidgets.QPushButton('Delete a line', self)
        self.buttonAddColumn = QtWidgets.QPushButton("Add a Column", self)
        self.buttonRemoveColumn = QtWidgets.QPushButton("Delete a Column", self)
        self.buttonSolve = QtWidgets.QPushButton("Solve", self)

        self.layout = QtWidgets.QGridLayout(self)
        # self.layout.addWidget(self.buttonAddRow, 0, 0, 1, 2)
        # self.layout.addWidget(self.buttonRemoveRow, 0, 2, 1, 2)
        # self.layout.addWidget(self.buttonAddColumn, 0, 4, 1, 2)
        # self.layout.addWidget(self.buttonRemoveColumn, 0, 6, 1, 2)
        self.layout.addWidget(self.buttonAddColumn, 0, 0, 1, 4)
        self.layout.addWidget(self.buttonRemoveColumn, 0, 4, 1, 4)
        self.layout.addWidget(self.mainTable, 1, 0, 3, 8)
        self.layout.addWidget(self.buttonSolve, 4, 0, 1, 8)

        # self.buttonAddRow.clicked.connect(self.addRow)
        # self.buttonRemoveRow.clicked.connect(self.removeRow)
        self.buttonAddColumn.clicked.connect(self.addColumn)
        self.buttonRemoveColumn.clicked.connect(self.removeColumn)
        self.buttonSolve.clicked.connect(lambda: self.solve(Johnson))

    def addRow(self):
        self.mainTable.insertRow(self.mainTable.rowCount())
        for col in range(self.mainTable.columnCount()):
            item = QtWidgets.QTableWidgetItem('0')
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            self.mainTable.setItem(self.mainTable.rowCount() - 1, col, item)
        self.setHeadersForMainTable()

    def removeRow(self):
        if self.mainTable.rowCount() > 0:
            self.mainTable.removeRow(self.mainTable.rowCount() - 1)
        self.setHeadersForMainTable()

    def addColumn(self):
        self.mainTable.insertColumn(self.mainTable.columnCount())
        for row in range(self.mainTable.rowCount()):
            item = QtWidgets.QTableWidgetItem('0')
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            self.mainTable.setItem(row, self.mainTable.columnCount() - 1, item)
        self.setHeadersForMainTable()

    def removeColumn(self):
        if self.mainTable.columnCount() > 0:
            self.mainTable.removeColumn(self.mainTable.columnCount() - 1)
        self.setHeadersForMainTable()

    def fillTableWithZeros(self, table):
        for row in range(table.rowCount()):
            for col in range(table.columnCount()):
                item = QtWidgets.QTableWidgetItem("0")
                item.setTextAlignment(QtCore.Qt.AlignCenter)
                table.setItem(row, col, item)

    def setHeadersForMainTable(self):
        columnsHeaders = "|".join(
            f"J{column+1}" for column in range(self.mainTable.columnCount())
        )
        rowsHeaders = "|".join(
            f"M{row+1}" for row in range(self.mainTable.rowCount())
        )
        self.mainTable.setHorizontalHeaderLabels(
            columnsHeaders.split("|")
        )
        self.mainTable.setVerticalHeaderLabels(
            rowsHeaders.split("|")
        )

    def setHeaders(self, table, order):
        columnsHeaders = "|".join(
            f"J{order[column]+1}" for column in range(table.columnCount())
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
        nColumns = table.columnCount()
        machines = []

        for row in range(2):
            d = []
            for col in range(nColumns):
                item = table.item(row, col)
                d += (int(item.text()),)
            machines += (d,)

        return machines

    def solve(self, cls):
        machines = self.readInputs(self.mainTable)
        self.solution = cls(machines)
        self.printResults()

    def printResults(self):
        nRows = self.mainTable.rowCount()
        nColumns = self.mainTable.columnCount()

        self.resTable = QtWidgets.QTableWidget(nRows, nColumns, self)
        machines = self.readInputs(self.mainTable)
        order = self.solution.order
        res = []

        for machine in machines:
            d = [machine[order[i]] for i in range(len(order))]
            res += d

        for row in range(nRows):
            for col in range(nColumns):
                item = QtWidgets.QTableWidgetItem(str(res[row * nColumns + col]))
                item.setTextAlignment(QtCore.Qt.AlignCenter)
                self.resTable.setItem(row, col, item)
        self.setHeaders(self.resTable, order)
        self.buttonShowchart = QtWidgets.QPushButton("Draw Chart", self)

        self.layout.addWidget(self.resTable, 5, 0, 3, 8)
        self.layout.addWidget(self.buttonShowchart, 8, 0, 1, 8)
        self.buttonShowchart.clicked.connect(self.drawChart)

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
        ncolumns = self.mainTable.columnCount()
        machines = [*self.readInputs(self.resTable)]
        results = []

        for i in range(len(machines)):
            result = []
            if i == 0:
                for j in range(ncolumns):
                    result += ((self.calculateM1(j), machines[i][j]),)
            else:
                for j in range(ncolumns):
                    result += ((self.calculateM2(i, j), machines[i][j]),)
            results += (result,)
        
        # results = [
        #     [(0, 2), (2, 3), (5, 6), (11, 7), (18, 3)], 
        #     [(2, 4), (6, 4), (11, 5), (18, 3), (21, 2)],
        #     [(0, 2), (2, 3), (5, 6), (11, 7), (18, 5)], 
        #     [(2, 4), (6, 4), (11, 5), (18, 3), (23, 2)],
        #     [(0, 2), (2, 3), (5, 6), (11, 7), (18, 5)], 
        #     [(2, 4), (6, 4), (11, 5), (18, 3), (23, 2)],
        #     [(0, 2), (2, 3), (5, 6), (11, 7), (18, 5)], 
        #     [(2, 4), (6, 4), (11, 5), (18, 3), (23, 2)],
        #     [(0, 2), (2, 3), (5, 6), (11, 7), (18, 5)], 
        #     [(2, 4), (6, 4), (11, 5), (18, 3), (23, 2)],
        #     [(0, 2), (2, 3), (5, 6), (11, 7), (18, 5)], 
        #     [(2, 4), (6, 4), (11, 5), (18, 3), (23, 2)],
        #     [(0, 2), (2, 3), (5, 6), (11, 7), (18, 5)], 
        #     [(2, 4), (6, 4), (11, 5), (18, 3), (23, 2)],
        # ]

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
                x = -1, 
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

        self.oTabWidget = QtWidgets.QTabWidget()
        self.chartWindow = QtWidgets.QWidget()
        self.chartLayout = QtWidgets.QGridLayout()
        # setting this layout to the widget
        self.chartWindow.setLayout(self.chartLayout)
        # this is the Canvas Widget that
        # displays the 'figure'it takes the
        # 'figure' instance as a parameter to __init__
        self.canvas = FigureCanvas(self.figure)
        # this is the Navigation widget
        # it takes the Canvas widget and a parent
        self.toolbar = NavigationToolbar(self.canvas, self)

        self.chartLayout.addWidget(self.toolbar)
        self.chartLayout.addWidget(self.canvas)

        self.chartWindow.setWindowTitle("Graph")
        self.chartWindow.resize(600, 400)
        self.chartWindow.show()

    def calculateM1(self, i):
        if i == 0:
            return 0
        else:
            return int(self.resTable.item(0, i - 1).text()) + self.calculateM1(i - 1)

    def calculateM2(self, i, j):
        if j == 0:
            return int(self.resTable.item(i - 1, 0).text())
        else:
            return max(
                self.calculateM1(j) + int(self.resTable.item(0, j).text()),
                self.calculateM2(i, j - 1) + int(self.resTable.item(i, j - 1).text()),
            )


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = Window()
    window.resize(640, 480)
    window.show()
    sys.exit(app.exec_())
