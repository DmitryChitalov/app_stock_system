# -*- coding: utf-8 -*-
#-----------------------Импорт модулей и внешних классов-----------------------#

from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtSql

from PyQt5.QtWidgets import QMainWindow, QAction, QDockWidget, \
    QFrame, QListWidget, QDesktopWidget, QApplication, \
    QStyle, QLabel, QLineEdit, QHBoxLayout, QGridLayout, QTreeView, \
    QScrollArea, QTableView, QWidget, QVBoxLayout, QPushButton, \
    QFormLayout, QComboBox, QListWidgetItem, QSpinBox, QDoubleSpinBox, \
    QFileDialog

from reports.print_list import PrintList

import sqlite3

#--------------------Разметка формы приходного ордера--------------------------#
class tws_report_class:
    def on_tws_report_btn(parent, db_path):

        def on_tws_report_print():
            report_name = "'Операции с поставщиками'"
            pl = PrintList()

            # Формируем данные для вывода на печать
            data = []

            i = 0
            while i < sqm.rowCount():
                record = sqm.record(i)
                numb = record.value(0)
                name = record.value(1)
                unit = record.value(2)
                quant = record.value(3)
                supp = record.value(4)
                data.append([numb, name, unit, quant, supp])
                i = i + 1
            pl.data = data
            pl.columnWidths = [70, 100, 60, 80, 80]
            pl.headers = ["№", "Название", "Ед.изм.", "Количество", "Поставщик"]
            pl.printData(parent, report_name)

        # Создаем таблицу
        tws_table_window = QTableView()
        tws_table_window.setFixedSize(408, 150)

        # Устанавливаем соединение с базой данных
        con = QtSql.QSqlDatabase.addDatabase('QSQLITE')
        con.setDatabaseName(db_path)
        con.open()

        query_str = 'SELECT DISTINCT numb, name, unit, SUM(quant), supp FROM ro_orders'
        sqm = QtSql.QSqlQueryModel(parent = tws_table_window)
        sqm.setQuery(query_str)

        sqm.setHeaderData(0, QtCore.Qt.Horizontal, '№')
        sqm.setHeaderData(1, QtCore.Qt.Horizontal, 'Название')
        sqm.setHeaderData(2, QtCore.Qt.Horizontal, 'Ед.изм.')
        sqm.setHeaderData(3, QtCore.Qt.Horizontal, 'Количество')
        sqm.setHeaderData(4, QtCore.Qt.Horizontal, 'Поставщик')

        tws_table_window.setModel(sqm)

        tws_table_window.setColumnWidth(0, 70)
        tws_table_window.setColumnWidth(1, 100)
        tws_table_window.setColumnWidth(2, 60)
        tws_table_window.setColumnWidth(3, 80)
        tws_table_window.setColumnWidth(4, 80)

        tws_report_btn = QPushButton("Печать")
        tws_report_btn.clicked.connect(on_tws_report_print)

        ### Размещаем все компоненты
        tws_report_grid = QGridLayout()

        tws_report_grid.addWidget(tws_table_window, 0, 0, alignment=QtCore.Qt.AlignCenter)
        tws_report_grid.addWidget(tws_report_btn, 1, 0, alignment=QtCore.Qt.AlignCenter)

        tws_report_frame = QFrame()
        tws_report_frame.setStyleSheet(open("./styles/properties_form_style.qss","r").read())
        tws_report_frame.setLayout(tws_report_grid)

        parent.tws_report_window = QWidget()
        parent.tws_report_window.setWindowModality(QtCore.Qt.ApplicationModal)
        parent.tws_report_window.setWindowTitle("Отчет 'Операции с поставщиками'")

        parent.tws_report_window.resize(460, 200)
        parent.tws_report_window.setLayout(tws_report_grid)
        parent.tws_report_window.show()

        screen = QDesktopWidget().screenGeometry()
        x = int((screen.width() - parent.tws_report_window.width()) / 2)
        y = int((screen.height() - parent.tws_report_window.height()) / 2)
        parent.tws_report_window.move(x, y)
