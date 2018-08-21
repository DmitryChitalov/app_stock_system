import sys
from PyQt5 import QtCore
from PyQt5.QtWidgets import QMainWindow, QAction, QDockWidget, \
    QFrame, QListWidget, QDesktopWidget, QApplication, \
    QStyle, QLabel, QLineEdit, QHBoxLayout, QGridLayout, QTreeView, \
    QScrollArea, QTableView, QWidget, QVBoxLayout, QPushButton, QTextEdit, \
    QScrollArea, QFormLayout, QTableWidget, QHeaderView, QTableWidgetItem, \
    QVBoxLayout

from PyQt5.QtGui import QPixmap

from PyQt5.QtGui import QStandardItemModel, QStandardItem

import sqlite3


class item_card_class(QWidget):
    def __init__(self, parent, db_path, file_name):
        QWidget.__init__(self, parent)

        # Получаем рисунок и помещаем его в виджет
        con = sqlite3.connect(db_path)
        cur = con.cursor()

        sql_item_img_select = "SELECT item_img FROM nomenclature WHERE item_name = ?"
        cur.execute(sql_item_img_select, [file_name])
        item_img = cur.fetchone()

        pix = QPixmap(item_img[0])
        pix_mini = pix.scaled(350, 290, QtCore.Qt.KeepAspectRatio)
        img_lbl = QLabel()

        img_lbl.setPixmap(pix_mini)
        img_lbl_vbox = QVBoxLayout()
        img_lbl_vbox.addWidget(img_lbl)
        img_lbl_frame = QFrame()
        img_lbl_frame.setLayout(img_lbl_vbox)
        img_lbl_frame.setFixedSize(350, 290)

        # Получаем все данные для товара
        # -номер
        sql_item_numb_select = "SELECT item_numb FROM nomenclature WHERE item_name = ?"
        cur.execute(sql_item_numb_select, [file_name])
        item_numb = cur.fetchone()
        # -название
        sql_item_name_select = "SELECT item_name FROM nomenclature WHERE item_name = ?"
        cur.execute(sql_item_name_select, [file_name])
        item_name = cur.fetchone()
        # -ед.изм.
        sql_item_unit_select = "SELECT item_unit FROM nomenclature WHERE item_name = ?"
        cur.execute(sql_item_unit_select, [file_name])
        item_unit = cur.fetchone()
        # -категория
        sql_item_cat_select = "SELECT item_cat FROM nomenclature WHERE item_name = ?"
        cur.execute(sql_item_cat_select, [file_name])
        item_cat = cur.fetchone()
        # -количество
        sql_item_amount_select = "SELECT item_amount FROM items_positions WHERE item_name = ?"
        # -поставщики
        sql_item_sup_select = "SELECT DISTINCT supp FROM ro_orders WHERE name = ?"

        # Проверяем, есть ли товар в наличии и только тогда выводим количество
        # и поставщиков
        sql_item_cur_select = "SELECT DISTINCT name FROM ro_orders WHERE name = ?"
        cur.execute(sql_item_cur_select, [file_name])
        item_cur = cur.fetchone()
        if item_cur is not None:
            cur.execute(sql_item_amount_select, [file_name])
            item_amount = cur.fetchone()
            cur.execute(sql_item_sup_select, [file_name])
            item_supp = cur.fetchall()

            suppliers_str = ''
            k = 1
            for el in item_supp[0]:
                if k != len(item_supp):
                    suppliers_str = suppliers_str + el + ','
                else:
                    suppliers_str = suppliers_str + el
                k = k + 1
            item_amount_str = str(item_amount[0])
        else:
            item_amount_str = 'Товар не в наличии'
            suppliers_str = 'Товар не в наличии'

        # Формируем таблицу
        item_card_table = QTableWidget()
        item_card_table.setRowCount(6)
        item_card_table.setColumnCount(1)
        item_card_table.horizontalHeader().hide()
        item_card_table.setFixedSize(210, 185)
        item_card_table.horizontalHeader().resizeSection(0, 125)
        #horizontal
        # столбец - номер
        item_card_table.verticalHeader().resizeSection(0, 30)
        item_card_table.verticalHeader().setSectionResizeMode(0, QHeaderView.Fixed)
        item_card_table.verticalHeader().minimumSectionSize()
        column_1 = QTableWidgetItem()
        column_1.setText("№")
        item_card_table.setVerticalHeaderItem(0, column_1)
        item_card_table.verticalHeader().setStyleSheet("color: steelblue")

        item_numb_lbl = QLabel(str(item_numb[0]))
        item_card_table.setCellWidget(0, 0, item_numb_lbl)

        # столбец - название
        item_card_table.verticalHeader().resizeSection(1, 30)
        item_card_table.verticalHeader().setSectionResizeMode(1, QHeaderView.Fixed)
        column_2 = QTableWidgetItem()
        column_2.setText("Название")
        item_card_table.setVerticalHeaderItem(1, column_2)
        item_card_table.verticalHeader().setStyleSheet("color: steelblue")

        item_name_lbl = QLabel(item_name[0])
        item_card_table.setCellWidget(1, 0, item_name_lbl)

        # столбец - ед.изм
        item_card_table.verticalHeader().resizeSection(2, 30)
        item_card_table.verticalHeader().setSectionResizeMode(2, QHeaderView.Fixed)
        column_3 = QTableWidgetItem()
        column_3.setText("Ед.изм.")
        item_card_table.setVerticalHeaderItem(2, column_3)
        item_card_table.verticalHeader().setStyleSheet("color: steelblue")

        item_unit_lbl = QLabel(item_unit[0])
        item_card_table.setCellWidget(2, 0, item_unit_lbl)

        # столбец - категория
        item_card_table.verticalHeader().resizeSection(3, 30)
        item_card_table.verticalHeader().setSectionResizeMode(3, QHeaderView.Fixed)
        column_4 = QTableWidgetItem()
        column_4.setText("Категория")
        item_card_table.setVerticalHeaderItem(3, column_4)
        item_card_table.verticalHeader().setStyleSheet("color: steelblue")

        item_cat_lbl = QLabel(item_cat[0])
        item_card_table.setCellWidget(3, 0, item_cat_lbl)

        # столбец - количество
        item_card_table.verticalHeader().resizeSection(4, 30)
        item_card_table.verticalHeader().setSectionResizeMode(4, QHeaderView.Fixed)
        column_5 = QTableWidgetItem()
        column_5.setText("Количество")
        item_card_table.setVerticalHeaderItem(4, column_5)
        item_card_table.verticalHeader().setStyleSheet("color: steelblue")

        item_amount_lbl = QLabel(item_amount_str)
        item_card_table.setCellWidget(4, 0, item_amount_lbl)

        # столбец - поставщики
        item_card_table.verticalHeader().resizeSection(5, 30)
        item_card_table.verticalHeader().setSectionResizeMode(5, QHeaderView.Fixed)
        column_6 = QTableWidgetItem()
        column_6.setText("Поставщики")
        item_card_table.setVerticalHeaderItem(5, column_6)
        item_card_table.verticalHeader().setStyleSheet("color: steelblue")

        item_supp_lbl = QLabel(suppliers_str)
        item_card_table.setCellWidget(5, 0, item_supp_lbl)

        cur.close()
        con.close()

        item_prs_grid = QGridLayout()
        item_prs_grid.addWidget(
            img_lbl_frame, 0, 0, alignment=QtCore.Qt.AlignCenter)
        item_prs_grid.addWidget(
            item_card_table, 1, 0, alignment=QtCore.Qt.AlignCenter)

        scrollArea = QScrollArea()
        scrollArea.setWidgetResizable(True)
        scrollArea.setLayout(item_prs_grid)
        scrollArea.setFixedSize(600, 518)

        fQMD_grid = QGridLayout()
        fQMD_grid.addWidget(scrollArea, 0, 0, alignment=QtCore.Qt.AlignCenter)
        fQMD_frame = QFrame()
        fQMD_frame.setStyleSheet(
            open(
                "./styles/properties_form_style.qss",
                "r").read())
        fQMD_frame.setFrameShape(QFrame.Panel)
        fQMD_frame.setFrameShadow(QFrame.Sunken)
        fQMD_frame.setLayout(fQMD_grid)

        fQMD_vbox = QVBoxLayout()
        fQMD_vbox.addWidget(fQMD_frame)

        # Размещение на форме всех компонентов

        form = QFormLayout()
        form.addRow(fQMD_vbox)
        self.setLayout(form)
