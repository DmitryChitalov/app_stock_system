# -*- coding: utf-8 -*-
#---------------------------Импорт модулей и внешних классов-------------------------#

from PyQt5 import QtCore, QtWidgets, QtSql

from PyQt5.QtWidgets import QMainWindow, QAction, QDockWidget, \
    QFrame, QListWidget, QDesktopWidget, QApplication, \
    QStyle, QLabel, QLineEdit, QHBoxLayout, QGridLayout, QTreeView, \
    QScrollArea, QTableView, QWidget, QVBoxLayout, QPushButton, \
    QFormLayout, QComboBox, QListWidgetItem, QSpinBox, QFileDialog

from PyQt5.QtGui import QStandardItem

import sqlite3

import os
import shutil

import traceback

#--------------------------------Класс формы-----------------------------------#

class item_form_class:
    def on_form_open(nom_table_window, numb_txt, db_path, parent):

        def on_img_choose():
            global img_path
            img_path, _filter = QFileDialog.getOpenFileName(
            None, "Выберите изображение", '.', "(*.png *.img *jpg)")
            img_edit.setText(img_path)

        def on_item_form_btnSave():
            if os.path.exists('./images') == False:
                os.mkdir('./images')
            shutil.copy(img_path, './images')
            base_name = os.path.basename(img_path)
            sql_img_name = './images' + '/' + base_name

            con = QtSql.QSqlDatabase.addDatabase('QSQLITE')
            con.setDatabaseName(db_path)
            con.open()

            parent.ldw_tree_model.removeRows(0, parent.ldw_tree_model.rowCount())

            query = QtSql.QSqlQuery()

            query.exec(
                "update nomenclature set item_img = '%s' where item_numb = '%s'" % (sql_img_name, numb_txt))

            msg_lbl = QLabel(
                '<span style="color:green">Добавлен новый товар</span>')
            parent.sm_list_widget.clear()
            parent.item = QListWidgetItem()
            parent.sm_list_widget.addItem(parent.item)
            parent.sm_list_widget.setItemWidget(parent.item, msg_lbl)

            con = sqlite3.connect(db_path)
            cur = con.cursor()
            sql_cats_select = """\
            SELECT DISTINCT item_cat FROM nomenclature
            """
            cur.execute(sql_cats_select)
            arr = cur.fetchall()
            for cat in arr:
                sql_items_select = "SELECT item_name FROM nomenclature \
                WHERE item_cat = ?"
                cur.execute(sql_items_select, [cat[0]])
                items = cur.fetchall()
                parent_item = QStandardItem(cat[0])
                parent.ldw_tree_model.appendRow(parent_item)

                j = 0

                for item in items:
                    child_item = QStandardItem(item[0])
                    parent_item.setChild(j, 0, child_item)
                    j = j + 1

            parent.ldw_tree.setModel(parent.ldw_tree_model)
            nom_table_window.item_form_window.close()

        def on_item_form_btnCancel(self):
            nom_table_window.item_form_window.close()

        img_label = QLabel('Изображение:')

        img_edit = QLineEdit()
        img_edit.setFixedSize(200, 25)
        img_edit.setEnabled(False)
        img_btn = QPushButton("...")
        img_btn.clicked.connect(on_img_choose)
        img_btn.setFixedSize(25, 25)

        item_form_grid = QGridLayout()

        item_form_grid = QGridLayout()
        item_form_grid.addWidget(img_label, 0, 0, alignment=QtCore.Qt.AlignCenter)
        item_form_grid.addWidget(img_edit, 0, 1, alignment=QtCore.Qt.AlignCenter)
        item_form_grid.addWidget(img_btn, 0, 2, alignment=QtCore.Qt.AlignCenter)

        item_form_frame = QFrame()
        item_form_frame.setStyleSheet(open("./styles/properties_form_style.qss","r").read())
        item_form_frame.setLayout(item_form_grid)

		#-----------------------------Кнопки формы--------------------------#

        item_form_btnSave = QPushButton('Сохранить')
        item_form_btnSave.setFixedSize(80, 25)
        item_form_btnSave.clicked.connect(on_item_form_btnSave)

        item_form_btnCancel = QPushButton('Отмена')
        item_form_btnCancel.setFixedSize(80, 25)
        item_form_btnCancel.clicked.connect(on_item_form_btnCancel)

        buttons_hbox = QHBoxLayout()
        buttons_hbox.addWidget(item_form_btnSave)
        buttons_hbox.addWidget(item_form_btnCancel)

		# --------------------Размещение на форме всех компонентов---------#

        item_form_grid = QGridLayout()
        item_form_grid.addWidget(item_form_frame, 0, 0, alignment=QtCore.Qt.AlignCenter)
        item_form_grid.addLayout(buttons_hbox, 1, 0, alignment=QtCore.Qt.AlignCenter)

        nom_table_window.item_form_window = QWidget()
        nom_table_window.item_form_window.setWindowModality(QtCore.Qt.ApplicationModal)
        nom_table_window.item_form_window.setWindowTitle("Форма выбора изображения товара")

        nom_table_window.item_form_window.setLayout(item_form_grid)
        nom_table_window.item_form_window.show()

        screen = QDesktopWidget().screenGeometry()
        x = int((screen.width() - nom_table_window.item_form_window.width()) / 2)
        y = int((screen.height() - nom_table_window.item_form_window.height()) / 2)
        nom_table_window.item_form_window.move(x, y)