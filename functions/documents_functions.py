# -*- coding: utf-8 -*-
#---------------------------Импорт модулей и внешних форм----------------------#


import sys
from PyQt5 import QtCore, QtWidgets, QtSql
import sqlite3
from PyQt5.QtWidgets import QMainWindow, QAction, QDockWidget, \
    QFrame, QListWidget, QDesktopWidget, QApplication, \
    QStyle, QLabel, QLineEdit, QHBoxLayout, QGridLayout, QTreeView, \
    QScrollArea, QTableView, QWidget, QVBoxLayout, QPushButton, \
    QDesktopWidget, QListWidgetItem

from PyQt5.QtGui import QStandardItemModel, QStandardItem

from functions.add_window_functions import add_functions_class
from forms.ro_order_form import ro_order_form_class
from forms.wo_order_form import wo_order_form_class


class documents_class:

    # Окно с приходными ордерами
    def on_ro_doc_btn(parent, db_path):
        def on_add_ro_order(ro_orders_window):
            ro_order_form_class.on_form_open(
                db_path,
                add_functions_class,
                parent.ro_orders_window,
                parent,
                ro_orders_table,
                ro_orders_model)

        # Отобразить все приходные ордера
        ro_orders_model = add_functions_class.all_ro_orders_print(parent,
                                                                  db_path)

        # Привязываем импортированную модель к виджету QTableView
        ro_orders_table = QTableView()
        ro_orders_table.setModel(ro_orders_model)
        ro_orders_table.setColumnWidth(0, 100)
        ro_orders_table.setColumnWidth(1, 140)
        ro_orders_table.setColumnWidth(2, 220)
        ro_orders_table.setColumnWidth(3, 120)
        ro_orders_table.setColumnWidth(4, 120)
        ro_orders_table.setColumnWidth(5, 120)
        ro_orders_table.setColumnWidth(6, 120)
        ro_orders_table.setColumnWidth(7, 120)

        ro_orders_vbox = QVBoxLayout()
        ro_orders_vbox.addWidget(ro_orders_table)

        parent.ro_orders_window = QWidget()

        btnAdd = QPushButton("Создать приходный ордер")
        btnAdd.clicked.connect(
            lambda: on_add_ro_order(
                parent.ro_orders_window))
        ro_orders_vbox.addWidget(btnAdd)

        parent.ro_orders_window.setWindowModality(QtCore.Qt.ApplicationModal)
        parent.ro_orders_window.setWindowTitle("Приходные ордера")

        parent.ro_orders_window.setLayout(ro_orders_vbox)
        parent.ro_orders_window.resize(1100, 300)
        parent.ro_orders_window.show()

    # Окно с расходными ордерами
    def on_wo_doc_btn(parent, db_path):
        def on_add_wo_order(wo_orders_window):
            wo_order_form_class.on_form_open(
                db_path,
                add_functions_class,
                parent.wo_orders_window,
                parent,
                wo_orders_table,
                wo_orders_model)

        # Отобразить все расходные ордера
        wo_orders_model = add_functions_class.all_wo_orders_print(parent,
                                                                  db_path)

        # Привязываем импортированную модель к виджету QTableView
        wo_orders_table = QTableView()
        wo_orders_table.setModel(wo_orders_model)
        wo_orders_table.setColumnWidth(0, 100)
        wo_orders_table.setColumnWidth(1, 140)
        wo_orders_table.setColumnWidth(2, 220)
        wo_orders_table.setColumnWidth(3, 120)
        wo_orders_table.setColumnWidth(4, 120)
        wo_orders_table.setColumnWidth(5, 120)
        wo_orders_table.setColumnWidth(6, 150)
        wo_orders_table.setColumnWidth(7, 150)

        wo_orders_vbox = QVBoxLayout()
        wo_orders_vbox.addWidget(wo_orders_table)

        parent.wo_orders_window = QWidget()

        btnAdd = QPushButton("Создать расходный ордер")
        btnAdd.clicked.connect(
            lambda: on_add_wo_order(
                parent.wo_orders_window))
        wo_orders_vbox.addWidget(btnAdd)

        parent.wo_orders_window.setWindowModality(QtCore.Qt.ApplicationModal)
        parent.wo_orders_window.setWindowTitle("Расходные ордера")

        parent.wo_orders_window.setLayout(wo_orders_vbox)
        parent.wo_orders_window.resize(1145, 300)
        parent.wo_orders_window.show()
