 #!/usr/bin/python3
# -*- coding: utf-8 -*-
# Modules import
import sys
from PyQt5 import QtCore, QtWidgets, QtSql
from PyQt5.QtWidgets import QMainWindow, QAction, QDockWidget, \
    QFrame, QListWidget, QDesktopWidget, QApplication, \
    QStyle, QLabel, QLineEdit, QHBoxLayout, QGridLayout, QTreeView, \
    QScrollArea, QTableView, QWidget, QVBoxLayout, QPushButton, QTextEdit, \
    QScrollArea, QFileDialog

from PyQt5.QtGui import QStandardItemModel, QStandardItem

import sqlite3

import re
import traceback

from forms.item_card import item_card_class
from functions.directories_functions import directories_class
from functions.documents_functions import documents_class
from reports.gis_report import gis_report_class
from reports.tws_report import tws_report_class


class CatalogMainWindow(QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)

        # Структура главного окна
        # Создаем меню
        self.menu_bar = self.menuBar()

        # Создаем блоки меню
        # Блок меню 'Учет движения товаров'

        self.gma_menu = self.menu_bar.addMenu('Учет движения товаров')
        self.gma_menu.setEnabled(False)
        self.ro_open_btn = QAction(self)
        self.ro_open_btn.setText('Приходный ордер')
        self.wo_open_btn = QAction(self)
        self.wo_open_btn.setText('Расходный ордер')
        self.gma_menu.addAction(self.ro_open_btn)
        self.gma_menu.addAction(self.wo_open_btn)

        # Блок меню 'Отчеты'

        self.r_menu = self.menu_bar.addMenu('Отчеты')
        self.r_menu.setEnabled(False)
        self.tws_report_btn = QAction(self)
        self.tws_report_btn.setText('Операции с поставщиками')
        self.gis_report_btn = QAction(self)
        self.gis_report_btn.setText('Товары в наличии')
        self.r_menu.addAction(self.tws_report_btn)
        self.r_menu.addAction(self.gis_report_btn)

        # Блок меню 'Справочники'
        self.d_menu = self.menu_bar.addMenu('Справочники')
        self.d_menu.setEnabled(False)

        self.u_catalog_btn = QAction(self)
        self.u_catalog_btn.setText('Пользователи')

        self.r_catalog_btn = QAction(self)
        self.r_catalog_btn.setText('Права пользователей')

        self.c_catalog_btn = QAction(self)
        self.c_catalog_btn.setText('Категории')

        self.n_catalog_btn = QAction(self)
        self.n_catalog_btn.setText('Номенклатура товаров')

        self.un_catalog_btn = QAction(self)
        self.un_catalog_btn.setText('Единицы измерения')

        self.s_catalog_btn = QAction(self)
        self.s_catalog_btn.setText('Поставщики')

        self.p_catalog_btn = QAction(self)
        self.p_catalog_btn.setText('Должности')

        self.e_catalog_btn = QAction(self)
        self.e_catalog_btn.setText('Сотрудники')

        self.d_menu.addAction(self.u_catalog_btn)
        self.d_menu.addAction(self.r_catalog_btn)
        self.d_menu.addAction(self.c_catalog_btn)
        self.d_menu.addAction(self.n_catalog_btn)
        self.d_menu.addAction(self.un_catalog_btn)
        self.d_menu.addAction(self.s_catalog_btn)
        self.d_menu.addAction(self.p_catalog_btn)
        self.d_menu.addAction(self.e_catalog_btn)

        # Верхний виджет с полным путем до файла БД

        self.db_lbl = QLabel()
        self.db_lbl.setText('Путь до БД:')
        self.db_lbl.setStyleSheet("border-style: none;" "font-size: 10pt;")
        self.db_path_lbl = QLineEdit()
        self.db_path_lbl.setStyleSheet(
            "background-color: white;"
            "font-size: 10pt;"
            "color: green;")
        self.db_path_lbl.setFixedSize(700, 25)
        self.db_path_lbl.setEnabled(False)
        self.db_path_btn = QPushButton('...')
        self.db_path_btn.setFixedSize(25, 25)
        self.db_path_btn.setStyleSheet(
            "border-width: 1px;"
            "border-style: solid;"
            "border-color: dimgray;"
            "border-radius: 5px;"
            "background-color: gainsboro;")
        self.db_path_btn.clicked.connect(self.on_db_path_btn_clicked)

        self.tdw = QDockWidget()
        self.tdw.setFixedHeight(65)
        self.tdw.setFeatures(self.tdw.NoDockWidgetFeatures)
        self.tdw_grid = QGridLayout()
        self.tdw_grid.setColumnStretch(3, 1)
        self.tdw_grid.addWidget(self.db_lbl)
        self.tdw_grid.addWidget(self.db_path_lbl)
        self.tdw_grid.addWidget(self.db_path_btn)
        self.tdw_frame = QFrame()
        self.tdw_frame.setStyleSheet(
            "background-color: ghostwhite;"
            "border-width: 0.5px;"
            "border-style: solid;"
            "border-color: silver;")
        self.tdw_frame.setLayout(self.tdw_grid)
        self.tdw.setWidget(self.tdw_frame)
        self.addDockWidget(QtCore.Qt.TopDockWidgetArea, self.tdw)

        # Левый виджет с окном каталога продукции

        self.ldw = QDockWidget()
        self.ldw.setFixedSize(500, 570)
        self.ldw.setFeatures(self.ldw.NoDockWidgetFeatures)
        self.ldw_tree = QTreeView()
        self.ldw_tree.setFixedSize(500, 530)
        self.ldw_tree.setHeaderHidden(True)
        self.ldw_tree_model = QStandardItemModel()
        self.ldw_tree.setModel(self.ldw_tree_model)
        self.ldw_tree.clicked.connect(self.on_ldw_tree_clicked)
        self.outf_scroll = QScrollArea()
        self.outf_scroll.setWidget(self.ldw_tree)
        self.ldw.setWidget(self.outf_scroll)
        self.ldw.setWindowTitle("Каталог продукции")

        # Центральный виджет с карточкой товара

        self.cdw = QDockWidget()
        self.cdw.setFeatures(self.cdw.NoDockWidgetFeatures)
        #self.setCentralWidget(self.cdw)

        # Нижний виджет со служебными сообщениями

        self.smdw = QDockWidget()
        self.smdw.setFixedHeight(140)
        self.smdw.setFeatures(self.smdw.NoDockWidgetFeatures)
        self.sm_list_widget = QListWidget()
        self.smdw.setWidget(self.sm_list_widget)
        self.smdw.setWindowTitle("Служебные сообщения")

    # Функции главного окна
    # Функция выбора файла базы данных
    def on_db_path_btn_clicked(self):
        global db_path
        db_path, _filter = QFileDialog.getOpenFileName(
            None, "Open Data File", '.', "(*.sqlite)")
        self.db_path_lbl.setText(db_path)
        self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, self.ldw)
        self.addDockWidget(QtCore.Qt.BottomDockWidgetArea, self.smdw)

        # Создаем все таблицы, которые нужны
        con = QtSql.QSqlDatabase.addDatabase('QSQLITE')
        con.setDatabaseName(db_path)
        con.open()

        if 'rules' not in con.tables():

            query = QtSql.QSqlQuery()
            query.exec(
                "CREATE TABLE rules(rule STRING UNIQUE, description STRING)")

            r1 = "admin"
            d1 = "Доступны все опции"
            query.exec(
                "INSERT INTO rules(rule, description) VALUES ('%s','%s')" %
                (r1, d1))

            r2 = "Кладовщик"
            d2 = "Доступны опции кладовщика"
            query.exec(
                "INSERT INTO rules(rule, description) VALUES ('%s','%s')" %
                (r2, d2))

        if 'nomenclature' not in con.tables():
            query = QtSql.QSqlQuery()
            query.exec(
                "CREATE TABLE nomenclature(item_numb INTEGER UNIQUE PRIMARY KEY NOT NULL, \
                item_name STRING NOT NULL, item_unit STRING REFERENCES units (unit) NOT NULL, \
                item_cat STRING REFERENCES categories (category) NOT NULL, item_img BLOB)")

        if 'units' not in con.tables():
            query = QtSql.QSqlQuery()
            query.exec("CREATE TABLE units(unit STRING PRIMARY KEY \
            UNIQUE NOT NULL)")

        if 'categories' not in con.tables():
            query = QtSql.QSqlQuery()
            query.exec(
                "CREATE TABLE categories(category STRING PRIMARY KEY UNIQUE \
                NOT NULL, description STRING NOT NULL)")

        # Создаем таблицу 'users', если не существует
        if 'users' not in con.tables():
            query = QtSql.QSqlQuery()
            query.exec(
                "CREATE TABLE users(id_user INTEGER PRIMARY KEY AUTOINCREMENT \
                unique NOT NULL, \
                login STRING UNIQUE NOT NULL, password STRING NOT NULL, \
                name TEXT NOT NULL, \
                rules STRING REFERENCES rules (rule) NOT NULL)")

        if 'suppliers' not in con.tables():
            query = QtSql.QSqlQuery()
            query.exec("CREATE TABLE suppliers( \
                id_supplier INTEGER UNIQUE PRIMARY KEY AUTOINCREMENT NOT NULL, \
                supplier STRING UNIQUE NOT NULL, \
                ownerchipform STRING NOT NULL, \
                address STRING NOT NULL, \
                phone STRING NOT NULL, \
                email STRING NOT NULL \
            )")

        if 'positions' not in con.tables():
            query = QtSql.QSqlQuery()
            query.exec(
                "CREATE TABLE positions(position STRING PRIMARY KEY UNIQUE \
                NOT NULL)")

        if 'employee' not in con.tables():
            query = QtSql.QSqlQuery()
            query.exec(
                "CREATE TABLE employee(employee_id INTEGER UNIQUE PRIMARY KEY AUTOINCREMENT, \
                fio STRING NOT NULL, \
                position STRING REFERENCES positions (position) NOT NULL)")

        con.close()



        con = sqlite3.connect(db_path)
        cur = con.cursor()
        sql_cats_select = """\
        SELECT DISTINCT item_cat FROM nomenclature
        """
        cur.execute(sql_cats_select)
        arr = cur.fetchall()
        #print(arr)

        for cat in arr:
            sql_items_select = "SELECT item_name FROM nomenclature \
            WHERE item_cat = ?"
            cur.execute(sql_items_select, [cat[0]])
            items = cur.fetchall()
            #print(items)
            parent_item = QStandardItem(cat[0])
            self.ldw_tree_model.appendRow(parent_item)

            j = 0

            for item in items:
                child_item = QStandardItem(item[0])
                parent_item.setChild(j, 0, child_item)
                j = j + 1


        cur.close()
        con.close()

        self.gma_menu.setEnabled(True)
        self.r_menu.setEnabled(True)
        self.d_menu.setEnabled(True)

        self.ro_open_btn.triggered.connect(
            lambda: documents_class.on_ro_doc_btn(
                self, db_path))
        self.wo_open_btn.triggered.connect(
            lambda: documents_class.on_wo_doc_btn(
                self, db_path))

        self.gis_report_btn.triggered.connect(
            lambda: gis_report_class.on_gis_report_btn(
                self, db_path))

        self.tws_report_btn.triggered.connect(
            lambda: tws_report_class.on_tws_report_btn(
                self, db_path))

        self.u_catalog_btn.triggered.connect(
            lambda: directories_class.on_u_catalog_btn(
                self, db_path))
        self.r_catalog_btn.triggered.connect(
            lambda: directories_class.on_r_catalog_btn(
                self, db_path))
        self.c_catalog_btn.triggered.connect(
            lambda: directories_class.on_c_catalog_btn(
                self, db_path))
        self.n_catalog_btn.triggered.connect(
            lambda: directories_class.on_n_catalog_btn(
                self, db_path))
        self.un_catalog_btn.triggered.connect(
            lambda: directories_class.on_un_catalog_btn(
                self, db_path))
        self.s_catalog_btn.triggered.connect(
            lambda: directories_class.on_s_catalog_btn(
                self, db_path))
        self.p_catalog_btn.triggered.connect(
            lambda: directories_class.on_p_catalog_btn(
                self, db_path))
        self.e_catalog_btn.triggered.connect(
            lambda: directories_class.on_e_catalog_btn(
                self, db_path))

    # Функция выбора товара из каталога-дерева
    def on_ldw_tree_clicked(self):
        #print('вах')


        try:
            current_index = self.ldw_tree.currentIndex()
            file_name = self.ldw_tree.model().data(current_index)
            con = sqlite3.connect(db_path)
            cur = con.cursor()
            sql_item_select = "SELECT item_name FROM nomenclature \
            WHERE item_name = ?"
            cur.execute(sql_item_select, [file_name])
            item = cur.fetchone()
            if item:
                self.setCentralWidget(self.cdw)
                self.cdw.setWindowTitle("Карточка товара")
                item_card = item_card_class(self, db_path, file_name)
                self.cdw.setWidget(item_card)
            cur.close()
            con.close()
        except Exception as e:
            print('Ошибка:\n', traceback.format_exc())


# Отобразить главное окно
if __name__ == "__main__":
    #closeInput = raw_input("Press ENTER to exit")
    app = QApplication(sys.argv)
    CMW = CatalogMainWindow()
    CMW.setWindowTitle('Складской учет')
    CMW.setFixedSize(1200, 800)
    CMW.show()
    sys.exit(app.exec_())
    #input()
