import sys
import pandas as pd
from pprint import pprint
import matplotlib.pyplot as plt
from PyQt5 import QtWidgets, QtCore, QtPrintSupport, QtGui

class Window(QtWidgets.QWidget):
    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        self.setWindowTitle(self.tr("Johnson Solver By Reda Zitouni"))

        self.mainTable = QtWidgets.QTableWidget(2, 4, self)
        self.setHeadersForMainTable()
        fillTableWithZeros(self.mainTable)
        self.textbox = QtWidgets.QLineEdit()
        
        self.buttonAddColumn = QtWidgets.QPushButton('Add a Column', self)
        self.buttonRemoveColumn = QtWidgets.QPushButton('Delete a Column', self)
        self.buttonSolve = QtWidgets.QPushButton('Solve', self)

        self.layout = QtWidgets.QGridLayout(self)
        self.layout.addWidget(self.buttonAddColumn, 0, 0, 1, 4)
        self.layout.addWidget(self.buttonRemoveColumn, 0, 4, 1, 4)
        self.layout.addWidget(self.mainTable, 1, 0, 3, 8)
        self.layout.addWidget(self.buttonSolve, 4, 0, 1, 8)

        self.buttonAddColumn.clicked.connect(self.addColumn)
        self.buttonRemoveColumn.clicked.connect(self.removeColumn)
        self.buttonSolve.clicked.connect(self.Johnson)

    def addColumn(self):
        self.mainTable.insertColumn(self.mainTable.columnCount())
        for row in range(self.mainTable.rowCount()):
            item = QtWidgets.QTableWidgetItem('0')
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            self.mainTable.setItem(row, self.mainTable.columnCount() - 1, item)
        self.setHeadersForMainTable()

    def removeColumn(self):
        if  self.mainTable.columnCount() > 0 :
            self.mainTable.removeColumn(self.mainTable.columnCount() - 1)
        self.setHeadersForMainTable()

    def setHeadersForMainTable(self):
        rowsHeaders = ''.join(f"M{row+1}|" for row in range(self.mainTable.rowCount()))
        columnsHeaders = ''.join(f"J{column+1}|" for column in range(self.mainTable.columnCount()))

        self.mainTable.setHorizontalHeaderLabels(columnsHeaders.split('|'))
        self.mainTable.setVerticalHeaderLabels(rowsHeaders.split('|'))

    def readInputs(self, table):
        ncells = table.columnCount()
        m1 = []
        m2 = []

        for row in range(2):
            # d = []
            for cell in range(ncells):
                item = table.item(row, cell)
                if row == 0:
                    m1 += int(item.text()),
                else:
                    m2 += int(item.text()),
        
        return m1, m2

    def Johnson(self):
        ncells = self.mainTable.columnCount()
        m1, m2 = self.readInputs(self.mainTable)

        start, end = [], []

        for i in range(ncells):
            minM1 = min(m1)
            minM2 = min(m2)

            if minM1 <= minM2:
                indexMinM1 = m1.index(minM1)
                start += indexMinM1,
                m1[indexMinM1] = m1[indexMinM1] + 9**10
                m2[indexMinM1] = m2[indexMinM1] + 9**10
            else:    
                indexMinM2 = m2.index(minM2)
                end += indexMinM2,
                m1[indexMinM2] = m1[indexMinM2] + 9**10
                m2[indexMinM2] = m2[indexMinM2] + 9**10

        order = start + end[::-1]
        self.resTable = QtWidgets.QTableWidget(2, ncells, self)
        m1, m2 = self.readInputs(self.mainTable)
        resM1 = [m1[order[i]] for i in range(len(order))]
        resM2 = [m2[order[i]] for i in range(len(order))]
        res = resM1 + resM2
        for row in range(self.resTable.rowCount()):
            for col in range(self.resTable.columnCount()):
                item = QtWidgets.QTableWidgetItem(str(res[row*ncells + col]))
                item.setTextAlignment(QtCore.Qt.AlignCenter)
                self.resTable.setItem(row, col, item)
        setHeaders(self.resTable, order)
        self.buttonShowchart = QtWidgets.QPushButton("Draw Chart", self)
        
        self.layout.addWidget(self.resTable, 5, 0, 3, 8)
        self.layout.addWidget(self.buttonShowchart, 8, 0, 1, 8)
        self.buttonShowchart.clicked.connect(self.drawChart)

    def drawChart(self):
        ncells = self.mainTable.columnCount()
        machines = [*self.readInputs(self.resTable)]
        # print(machines)
        # resM1, resM2 = self.readInputs(self.resTable)

        # resM1 = [m1[order[i]] for i in range(len(order))]
        # resM2 = [m2[order[i]] for i in range(len(order))]

        # df = pd.DataFrame(list(zip(m1, m2)), columns=["M1", "M2"])
        # res1 = []
        # for i in range(ncells):
        #     res1 += (self.calculateM1(i), resM1[i]),
        
        # res2 = []
        # for i in range(ncells):
        #     res2 += (self.calculateM2(i), resM2[i]),
        results = []
        for i in range(len(machines)):
            result = []
            if i == 0:
                for j in range(ncells):
                    result += (self.calculateM1(j), machines[i][j]),
            else:
                for j in range(ncells):
                    result += (self.calculateM2(i, j), machines[i][j]),
            results += result,

        # Set the figure size
        plt.rcParams["figure.figsize"] = [7.50, 3.50]
        plt.rcParams["figure.autolayout"] = True

        # Figure and set of subplots
        fig, ax = plt.subplots()

        # Horizontal sequence of rectangles
        ax.broken_barh(results[0], (20, 9), facecolors='tab:blue', edgecolor='black')
        ax.broken_barh(results[1], (10, 9), facecolors='tab:orange', edgecolor='black')

        # ylim and xlim of the axes
        ax.set_ylim(5, 35)
        ax.set_xlim(0, 60)

        # Show the plot
        plt.show()
    
    def calculateM1(self, i):
        if i == 0 :
            return 0
        else:
            return int(self.resTable.item(0, i-1).text()) + self.calculateM1(i-1)
        
    def calculateM2(self, i, j):
        if j == 0 :
            return int(self.resTable.item(i - 1, 0).text())
        else:
            return max(self.calculateM1(j) + int(self.resTable.item(0, j).text()), self.calculateM2(i, j-1) + int(self.resTable.item(i, j-1).text())) 
    # def calculateM2(self, i, j):
    #     if j == 0 :
    #         return int(self.resTable.item(i - 1, 0).text())
    #     else:
    #         return max(self.calculateM1(j) + int(self.resTable.item(0, j).text()), self.calculateM2(i, j-1) + int(self.resTable.item(i, j-1).text())) 
        # else:
        #     if j == 0 :
        #         return self.calculateM2(i - 1, j) + int(self.resTable.item(i - 1, j).text())
        #     else:
        #         return max(self.calculateM1(j) + int(self.resTable.item(0, j).text()), self.calculateM2(i, j-1) + int(self.resTable.item(i, j-1).text())) 
       
def fillTableWithZeros(table):
        for row in range(table.rowCount()):
            for col in range(table.columnCount()):
                item = QtWidgets.QTableWidgetItem('0')
                item.setTextAlignment(QtCore.Qt.AlignCenter)
                table.setItem(row, col, item)

def setHeaders(table, order):
    rowsHeaders = '|'.join(f"M{row+1}" for row in range(table.rowCount()))
    columnsHeaders = '|'.join(f"J{order[column]+1}" for column in range(table.columnCount()))

    table.setHorizontalHeaderLabels(columnsHeaders.split('|'))
    table.setVerticalHeaderLabels(rowsHeaders.split('|'))

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = Window()
    window.resize(640, 480)
    window.show()
    sys.exit(app.exec_())