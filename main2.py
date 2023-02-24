from PyQt5 import QtCore, QtPrintSupport, QtGui
from PyQt5.QtWidgets import *
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from algorithms.Johnson import Johnson
# from PyQt5.QtWidgets import (QWidget, QPushButton,
#     QHBoxLayout, QVBoxLayout, QApplication, QStackedWidget, QLabel, QTableWidget, QGridLayout, QCheckBox)

class Example(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()
        self.stackedWidget.currentChanged.connect(self.set_button_state)
        # self.next_button.clicked.connect(self.nextPage)
        # self.prev_button.clicked.connect(self.prevPage)
        self.next_button.clicked.connect(self.page2)
        self.prev_button.clicked.connect(self.page1)


    def initUI(self):
        self.firstPageGrid = QGridLayout(self)
        self.secondPageGrid = QGridLayout(self)
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
        # self.page2() 

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


    # def solve(self, cls):
    #     machines = self.readInputs(self.mainTable)
    #     self.solution = cls(machines)
    #     self.printResults()
    def solve(self):
        machines = self.readInputs(self.mainTable)
        self.solution = Johnson(machines)

    
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


    def page1(self):
        self.testWindow = QWidget()
        # self.firstPageGrid = QGridLayout(self)
        self.mainTable = QTableWidget(2, 4, self)
        self.fillTableWithZeros(self.mainTable)
        self.setHeaders(self.mainTable)

        # self.secondTable = QTableWidget(1, 4, self)
        self.buttonAddColumn = QPushButton("Add a Column", self)
        self.buttonRemoveColumn = QPushButton("Delete a Column", self)
        self.delayCheckbox = QCheckBox("Delay", self)
        self.preparationCheckbox = QCheckBox("Preparation", self)
        # print(self.testCheckbox.isChecked())
        self.delayCheckbox.stateChanged.connect(self.toggleDelayTable)
        self.preparationCheckbox.stateChanged.connect(self.togglePreparationTable)

        # setting this layout to the widget
        self.testWindow.setLayout(self.firstPageGrid)

        self.firstPageGrid.addWidget(self.buttonAddColumn, 0, 0, 1, 4)
        self.firstPageGrid.addWidget(self.buttonRemoveColumn, 0, 4, 1, 4)
        self.firstPageGrid.addWidget(self.mainTable, 1, 0, 3, 8)
        self.firstPageGrid.addWidget(self.delayCheckbox, 4, 0, 1, 8)
        self.firstPageGrid.addWidget(self.preparationCheckbox, 6, 0, 1, 8)

        self.buttonAddColumn.clicked.connect(self.addColumn)
        self.buttonRemoveColumn.clicked.connect(self.removeColumn)

        self.stackedWidget.insertWidget(0, self.testWindow)
        self.stackedWidget.setCurrentIndex(0)


    def page2(self):
        self.secondTestWindow = QWidget()
        # self.secondPageGrid = QGridLayout(self)
        self.testTable = QTableWidget(2, self.mainTable.columnCount(), self)
        self.secondPageGrid.addWidget(self.testTable, 0, 0, 3, 8)
        # setting this layout to the widget
        self.secondTestWindow.setLayout(self.secondPageGrid)
        self.stackedWidget.insertWidget(1, self.secondTestWindow)
        self.stackedWidget.setCurrentIndex(1)


    def toggleDelayTable(self):
        # print(self.testCheckbox.checkState())
        if self.delayCheckbox.isChecked():
            nColumns = self.mainTable.columnCount()
            self.delayTable = QTableWidget(1, nColumns, self)
            columnsHeaders = "|".join(
                f"J{column+1}" for column in range(self.delayTable.columnCount())
            )
            self.delayTable.setHorizontalHeaderLabels(
                columnsHeaders.split("|")
            )
            self.firstPageGrid.addWidget(self.delayTable, 5, 0, 1, 8)
        else:
            self.firstPageGrid.removeWidget(self.delayTable)
            self.delayTable.deleteLater()
            # self.delayTable = None


    def togglePreparationTable(self):
        if self.preparationCheckbox.isChecked():
            self.preparationTable = QTableWidget(1, 4, self)
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

    app = QApplication([])
    window = Example()
    for i in range(5):
        window.insertPage(QLabel(f'This is page {i+1}'))
    window.resize(640, 480)
    window.show()
    app.exec()