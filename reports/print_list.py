from PyQt5 import QtCore, QtGui, QtPrintSupport

from PyQt5.QtWidgets import QLabel, QListWidgetItem

import time

class PrintList:
    def __init__(self):
        self.printer = QtPrintSupport.QPrinter()
        self.headerFont = QtGui.QFont(
            "Arial", pointSize=10, weight=QtGui.QFont.Bold)
        self.bodyFont = QtGui.QFont("Arial", pointSize=10)
        self.footerFont = QtGui.QFont("Arial", pointSize=9, italic=True)
        self.headerFlags = QtCore.Qt.AlignHCenter | QtCore.Qt.TextWordWrap
        self.bodyFlags = QtCore.Qt.TextWordWrap
        self.footerFlags = QtCore.Qt.AlignHCenter | QtCore.Qt.TextWordWrap
        color = QtGui.QColor(QtCore.Qt.black)
        self.headerPen = QtGui.QPen(color, 2)
        self.bodyPen = QtGui.QPen(color, 1)
        self.margin = 5
        self.resetData()

    def resetData(self):
        self.headers = None
        self.columnWidths = None
        self.data = None
        self.brush = QtCore.Qt.NoBrush
        self.currentRowHeight = 0
        self.currentPageHeight = 0
        self.headerRowHeight = 0
        self.footerRowHeight = 0
        self.currentPageNumber = 1
        self.painter = None

    def printImage(self, report_name, parent):
        self.painter = QtGui.QPainter()
        self.painter.begin(self.printer)

        msg_lbl = QLabel(
            '<span style="color:green">Отчет ' + report_name + ' отправлен на печать</span>')
        parent.sm_list_widget.clear()
        parent.item = QListWidgetItem()
        parent.sm_list_widget.addItem(parent.item)
        parent.sm_list_widget.setItemWidget(parent.item, msg_lbl)





        self.painter.setBrush(self.brush)
        if self.headerRowHeight == 0:
            self.painter.setFont(self.headerFont)
            self.headerRowHeight = self.calculateRowHeight(
                self.columnWidths, self.headers)
        if self.footerRowHeight == 0:
            self.painter.setFont(self.footerFont)
            self.footerRowHeight = self.calculateRowHeight(
                [self.printer.width()], "Страница")
        for i in range(len(self.data)):
            height = self.calculateRowHeight(self.columnWidths, self.data[i])
            if self.currentPageHeight + height > self.printer.height() - \
                    self.footerRowHeight - 2 * self.margin:
                self.printFooterRow()
                self.currentPageHeight = 0
                self.currentPageNumber += 1
                self.printer.newPage()
            if self.currentPageHeight == 0:
                self.painter.setPen(self.headerPen)
                self.painter.setFont(self.headerFont)
                self.printRow(
                    self.columnWidths,
                    self.headers,
                    self.headerRowHeight,
                    self.headerFlags)
                self.painter.setPen(self.bodyPen)
                self.painter.setFont(self.bodyFont)
            self.printRow(
                self.columnWidths,
                self.data[i],
                height,
                self.bodyFlags)
        self.printFooterRow()
        self.painter.end()

    def printData(self, parent, report_name):
        pp = QtPrintSupport.QPrintPreviewDialog(self.printer, parent = parent)
        pp.paintRequested.connect(lambda: self.printImage(report_name, parent))
        pp.exec()

    def calculateRowHeight(self, widths, cellData):
        height = 0
        for i in range(len(widths)):
            r = self.painter.boundingRect(0,
                                           0,
                                           widths[i] - 2 * self.margin,
                                           50,
                                           QtCore.Qt.TextWordWrap,
                                           str(cellData[i]))
            h = r.height() + 2 * self.margin
            if height < h:
                height = h
        return height

    def printRow(self, widths, cellData, height, flags):
        x = 0
        for i in range(len(widths)):
            self.painter.drawText(x +
                                   self.margin, self.currentPageHeight +
                                   self.margin, widths[i] -
                                   self.margin, height -
                                   2 *
                                   self.margin, flags, str(cellData[i]))
            self.painter.drawRect(
                x, self.currentPageHeight, widths[i], height)
            x += widths[i]
        self.currentPageHeight += height

    def printFooterRow(self):
        self.painter.setFont(self.footerFont)
        self.painter.drawText(self.margin,
                               self.printer.height() - self.footerRowHeight - self.margin,
                               self.printer.width() - 2 * self.margin,
                               self.footerRowHeight - 2 * self.margin,
                               self.footerFlags,
                               "Страница " + str(self.currentPageNumber))
