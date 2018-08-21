# -*- coding: utf-8 -*-
#-----------------------Импорт модулей и внешних классов-----------------------#

from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtSql
from PyQt5 import QtPrintSupport

from reports.print_list import PrintList
#from reports.my_window import MyWindow

import sys

from PyQt5.QtWidgets import QMainWindow, QAction, QDockWidget, \
    QFrame, QListWidget, QDesktopWidget, QApplication, \
    QStyle, QLabel, QLineEdit, QHBoxLayout, QGridLayout, QTreeView, \
    QScrollArea, QTableView, QWidget, QVBoxLayout, QPushButton, \
    QFormLayout, QComboBox, QListWidgetItem, QSpinBox, QDoubleSpinBox, \
    QFileDialog

import sqlite3

#--------------------Разметка формы приходного ордера--------------------------#
class gis_report_class:
    def on_gis_report_btn(parent, db_path):

        def on_gis_report_print():
            report_name = "'Товары в наличии'"
            pl = PrintList()

            # Формируем данные для вывода на печать
            data = []

            i = 0
            while i < sqm.rowCount():
                record = sqm.record(i)
                item_name = record.value(0)
                item_amount = record.value(1)
                data.append([item_name, item_amount])
                i = i + 1
            pl.data = data
            pl.columnWidths = [130, 100]
            pl.headers = ["Товар", "Количество"]
            pl.printData(parent, report_name)

        #def on_gis_report_print():
            #mw = MyWindow()


        # Создаем таблицу
        gis_table_window = QTableView()
        gis_table_window.setFixedSize(248, 150)

        # Устанавливаем соединение с базой данных
        con = QtSql.QSqlDatabase.addDatabase('QSQLITE')
        con.setDatabaseName(db_path)
        con.open()

        query_str = 'SELECT * FROM items_positions ORDER BY item_name'
        sqm = QtSql.QSqlQueryModel(parent = gis_table_window)
        sqm.setQuery(query_str)

        sqm.setHeaderData(0, QtCore.Qt.Horizontal, 'Товар')
        sqm.setHeaderData(1, QtCore.Qt.Horizontal, 'Количество')

        gis_table_window.setModel(sqm)

        #gis_table_window.hideColumn(0)
        gis_table_window.setColumnWidth(0, 130)
        gis_table_window.setColumnWidth(1, 100)

        gis_report_btn = QPushButton("Печать")
        gis_report_btn.clicked.connect(on_gis_report_print)

        ### Размещаем все компоненты
        gis_report_grid = QGridLayout()

        gis_report_grid.addWidget(gis_table_window, 0, 0, alignment=QtCore.Qt.AlignCenter)
        gis_report_grid.addWidget(gis_report_btn, 1, 0, alignment=QtCore.Qt.AlignCenter)

        gis_report_frame = QFrame()
        gis_report_frame.setStyleSheet(open("./styles/properties_form_style.qss","r").read())
        gis_report_frame.setLayout(gis_report_grid)

        parent.gis_report_window = QWidget()
        parent.gis_report_window.setWindowModality(QtCore.Qt.ApplicationModal)
        parent.gis_report_window.setWindowTitle("Отчет 'Товары в наличии'")

        parent.gis_report_window.resize(460, 200)
        parent.gis_report_window.setLayout(gis_report_grid)
        parent.gis_report_window.show()

        screen = QDesktopWidget().screenGeometry()
        x = int((screen.width() - parent.gis_report_window.width()) / 2)
        y = int((screen.height() - parent.gis_report_window.height()) / 2)
        parent.gis_report_window.move(x, y)
