# -*- coding: utf-8 -*-
#--------------------------Импорт модулей и внешних форм-----------------------#
#item_form_class
import sys
from PyQt5 import QtCore, QtWidgets, QtSql
import sqlite3
from PyQt5.QtWidgets import QMainWindow, QAction, QDockWidget, \
    QFrame, QListWidget, QDesktopWidget, QApplication, \
    QStyle, QLabel, QLineEdit, QHBoxLayout, QGridLayout, QTreeView, \
    QScrollArea, QTableView, QWidget, QVBoxLayout, QPushButton, \
    QDesktopWidget, QListWidgetItem, QComboBox

from PyQt5.QtGui import QStandardItemModel, QStandardItem

from forms.item_form import item_form_class
from functions.add_window_functions import add_functions_class


class directories_class:

    #! Справочник 'Пользователи'
    def on_u_catalog_btn(parent, db_path):
        def on_add_user():
            # Добавляем строку
            um.insertRow(um.rowCount())

        def on_del_user():
            # Удаляем строку
            um.removeRow(umv.currentIndex().row())
            # Выполняем повторное считывание данных в модель,
            # чтобы убрать пустую "мусорную" запись
            um.select()

        def on_data_change(um):
            um.submitAll()
            # Считаем количество записей после сохранения
            query = QtSql.QSqlQuery()
            query.exec("SELECT COUNT(*) AS new_count FROM users")
            query.next()
            recordCount = query.record()
            new_count_int = query.value(recordCount.indexOf("new_count"))

            if old_count_int != new_count_int:
                msg_lbl = QLabel(
                    '<span style="color:green">Добавлен новый пользователь</span>')
                parent.sm_list_widget.clear()
                parent.item = QListWidgetItem()
                parent.sm_list_widget.addItem(parent.item)
                parent.sm_list_widget.setItemWidget(parent.item, msg_lbl)

        # Устанавливаем соединение с базой данных
        con = QtSql.QSqlDatabase.addDatabase('QSQLITE')
        con.setDatabaseName(db_path)
        con.open()

        # Создаем окно
        parent.u_table_window = QWidget()
        parent.u_table_window.setWindowModality(QtCore.Qt.ApplicationModal)
        parent.u_table_window.setWindowTitle("Справочник 'Пользователи'")
        parent.u_table_window.resize(440, 300)

        # Создаем модель
        um = QtSql.QSqlRelationalTableModel(parent=parent.u_table_window)
        # Связываем таблицу с моделью
        um.setTable('users')
        um.setSort(0, QtCore.Qt.AscendingOrder)
        # Устанавливаем связь с внешней таблицей
        um.setRelation(4, QtSql.QSqlRelation('rules', 'rule', 'rule'))
        # Считываем данные в модель
        um.select()

        # Задаем заголовки для столбцов модели
        um.setHeaderData(1, QtCore.Qt.Horizontal, 'Логин')
        um.setHeaderData(2, QtCore.Qt.Horizontal, 'Пароль')
        um.setHeaderData(3, QtCore.Qt.Horizontal, 'Имя')
        um.setHeaderData(4, QtCore.Qt.Horizontal, 'Права')
        # При изменении данных выполняем сохранение
        # Считаем количество записей до сохранения
        query = QtSql.QSqlQuery()
        query.exec("SELECT COUNT(*) AS old_count FROM users")
        query.next()
        recordCount = query.record()
        old_count_int = query.value(recordCount.indexOf("old_count"))
        query.finish()

        um.dataChanged.connect(lambda: on_data_change(um))
        # Создаем виджет-таблицу
        umv = QTableView()
        # Связываем модель с виджетом-таблицей
        umv.setModel(um)
        umv.setItemDelegate(QtSql.QSqlRelationalDelegate(umv))
        umv.hideColumn(0)

        # Создаем контейнер
        users_vbox = QVBoxLayout()
        users_vbox.addWidget(umv)

        # Создаем кнопки и размещаем их в контейнеры
        btnAdd = QPushButton("Добавить пользователя")
        btnAdd.clicked.connect(on_add_user)
        users_vbox.addWidget(btnAdd)
        btnDel = QPushButton("Удалить пользователя")
        btnDel.clicked.connect(on_del_user)
        users_vbox.addWidget(btnDel)

        # Размещаем контейнер в окне
        parent.u_table_window.setLayout(users_vbox)
        parent.u_table_window.show()

        screen = QDesktopWidget().screenGeometry()
        x = int((screen.width() - parent.u_table_window.width()) / 2)
        y = int((screen.height() - parent.u_table_window.height()) / 2)
        parent.u_table_window.move(x, y)

    #! Справочник 'Права'
    def on_r_catalog_btn(parent, db_path):
        def on_add_rule():
            rm.insertRow(rm.rowCount())

        def on_del_rule():
            rm.removeRow(rmv.currentIndex().row())
            rm.select()

        con = QtSql.QSqlDatabase.addDatabase('QSQLITE')
        con.setDatabaseName(db_path)
        con.open()

        parent.rules_table_window = QWidget()
        parent.rules_table_window.setWindowModality(QtCore.Qt.ApplicationModal)
        parent.rules_table_window.setWindowTitle("Права пользователей")
        parent.rules_table_window.resize(400, 250)

        rm = QtSql.QSqlTableModel(parent=parent.rules_table_window)
        rm.setTable('rules')
        rm.setSort(0, QtCore.Qt.AscendingOrder)
        rm.select()

        rm.setHeaderData(1, QtCore.Qt.Horizontal, 'Права')
        rm.setHeaderData(2, QtCore.Qt.Horizontal, 'Описание')

        rmv = QTableView()
        rmv.setModel(rm)

        rmv.setColumnWidth(0, 100)
        rmv.setColumnWidth(1, 260)

        vbox = QVBoxLayout()
        vbox.addWidget(rmv)
        parent.rules_table_window.setLayout(vbox)

        parent.rules_table_window.show()

        screen = QDesktopWidget().screenGeometry()
        x = int((screen.width() - parent.rules_table_window.width()) / 2)
        y = int((screen.height() - parent.rules_table_window.height()) / 2)
        parent.rules_table_window.move(x, y)

    #! Справочник 'Категории'
    def on_c_catalog_btn(parent, db_path):
        def on_add_cat():
            cm.insertRow(cm.rowCount())

        def on_del_cat():
            cm.removeRow(cmv.currentIndex().row())
            cm.select()

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
                #print(items)
                parent_item = QStandardItem(cat[0])
                parent.ldw_tree_model.appendRow(parent_item)

                j = 0

                for item in items:
                    child_item = QStandardItem(item[0])
                    parent_item.setChild(j, 0, child_item)
                    j = j + 1

            cur.close()
            con.close()

        def on_data_change(cm):
            cm.submitAll()
            # Считаем количество записей после сохранения
            query = QtSql.QSqlQuery()
            query.exec("SELECT COUNT(*) AS new_count FROM categories")
            query.next()
            recordCount = query.record()
            new_count_int = query.value(recordCount.indexOf("new_count"))
            if old_count_int != new_count_int:
                msg_lbl = QLabel(
                    '<span style="color:green">Добавлена новая категория</span>')
                parent.sm_list_widget.clear()
                parent.item = QListWidgetItem()
                parent.sm_list_widget.addItem(parent.item)
                parent.sm_list_widget.setItemWidget(parent.item, msg_lbl)

        con = QtSql.QSqlDatabase.addDatabase('QSQLITE')
        con.setDatabaseName(db_path)
        con.open()

        parent.cat_table_window = QWidget()
        parent.cat_table_window.setWindowModality(QtCore.Qt.ApplicationModal)
        parent.cat_table_window.setWindowTitle("Категории товаров")
        parent.cat_table_window.resize(400, 250)

        cm = QtSql.QSqlTableModel(parent=parent.cat_table_window)
        cm.setTable('categories')
        cm.setSort(0, QtCore.Qt.AscendingOrder)
        cm.select()

        cm.setHeaderData(0, QtCore.Qt.Horizontal, 'Категория')
        cm.setHeaderData(1, QtCore.Qt.Horizontal, 'Описание')

        cmv = QTableView()
        cmv.setModel(cm)

        cmv.setColumnWidth(0, 100)
        cmv.setColumnWidth(1, 260)

        vbox = QVBoxLayout()
        vbox.addWidget(cmv)

        btnAdd = QPushButton("Добавить категорию")
        btnAdd.clicked.connect(on_add_cat)
        vbox.addWidget(btnAdd)
        btnDel = QPushButton("Удалить категорию")
        btnDel.clicked.connect(on_del_cat)
        vbox.addWidget(btnDel)
        parent.cat_table_window.setLayout(vbox)

        parent.cat_table_window.show()

       # Считаем количество записей до сохранения
        query = QtSql.QSqlQuery()
        query.exec("SELECT COUNT(*) AS old_count FROM categories")
        query.next()
        recordCount = query.record()
        old_count_int = query.value(recordCount.indexOf("old_count"))
        query.finish()
        #print(old_count_int)
        cm.dataChanged.connect(lambda: on_data_change(cm))

        screen = QDesktopWidget().screenGeometry()
        x = int((screen.width() - parent.cat_table_window.width()) / 2)
        y = int((screen.height() - parent.cat_table_window.height()) / 2)
        parent.cat_table_window.move(x, y)

    #! Справочник 'Номенклатура'

    def on_n_catalog_btn(parent, db_path):
        def on_add_item():
            nm.insertRow(nm.rowCount())
            nm_row_count = nm.rowCount()
            img_btn = QPushButton("Выбрать")
            img_btn.setStyleSheet(
                "border-width: 1px;"
                "border-style: solid;"
                "border-color: dimgray;"
                "border-radius: 4px;"
                "background-color: silver;")
            img_btn.clicked.connect(on_img_choose)
            img_btn.setFixedSize(90, 25)
            cell = nm.index(nm_row_count - 1, 4)
            nmv.setIndexWidget(cell, img_btn)

        def on_del_item():
            nm.removeRow(nmv.currentIndex().row())
            nm.select()

            empty_lbl = QLabel()
            parent.setCentralWidget(empty_lbl)
            parent.cdw.setWidget(empty_lbl)

            parent.ldw_tree_model.removeRows(0, parent.ldw_tree_model.rowCount())

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

        def on_img_choose():
            cur_index = nmv.currentIndex().row()
            numb_txt = nm.index(cur_index, 0).data()
            item_form_class.on_form_open(parent.nom_table_window, numb_txt, db_path, parent)

        con = QtSql.QSqlDatabase.addDatabase('QSQLITE')
        con.setDatabaseName(db_path)
        con.open()

        parent.nom_table_window = QWidget()
        parent.nom_table_window.setWindowModality(QtCore.Qt.ApplicationModal)
        parent.nom_table_window.setWindowTitle("Номенклатура товаров")
        parent.nom_table_window.resize(760, 250)

        nm = QtSql.QSqlRelationalTableModel(parent=parent.nom_table_window)
        nm.setTable('nomenclature')
        nm.setSort(0, QtCore.Qt.AscendingOrder)
        nm.setRelation(2, QtSql.QSqlRelation('units', 'unit', 'unit'))
        nm.setRelation(
            3,
            QtSql.QSqlRelation(
                'categories',
                'category',
                'category'))

        nm.select()

        nmv = QTableView()
        nmv.setModel(nm)
        nmv.setItemDelegate(QtSql.QSqlRelationalDelegate(nmv))
        nmv.setColumnWidth(0, 130)
        nmv.setColumnWidth(1, 320)
        nmv.setColumnWidth(2, 50)
        nmv.setColumnWidth(3, 130)
        nmv.setColumnWidth(4, 90)

        # Задаем заголовки для столбцов модели
        nm.setHeaderData(0, QtCore.Qt.Horizontal, 'Номенклатурный №')
        nm.setHeaderData(1, QtCore.Qt.Horizontal, 'Название')
        nm.setHeaderData(2, QtCore.Qt.Horizontal, 'Ед. изм.')
        nm.setHeaderData(3, QtCore.Qt.Horizontal, 'Категория')
        nm.setHeaderData(4, QtCore.Qt.Horizontal, 'Изображение')

        items_vbox = QVBoxLayout()
        items_vbox.addWidget(nmv)

        nm_row_count = nm.rowCount()
        for index in range(nm_row_count):
            img_btn = QPushButton("Выбрать")
            img_btn.setStyleSheet(
                "border-width: 1px;"
                "border-style: solid;"
                "border-color: dimgray;"
                "border-radius: 4px;"
                "background-color: silver;")
            img_btn.clicked.connect(on_img_choose)
            img_btn.setFixedSize(90, 25)
            cell = nm.index(index, 4)
            nmv.setIndexWidget(cell, img_btn)

        btnAdd = QPushButton("Добавить товар")
        btnAdd.clicked.connect(on_add_item)
        items_vbox.addWidget(btnAdd)
        btnDel = QPushButton("Удалить товар")
        btnDel.clicked.connect(on_del_item)
        items_vbox.addWidget(btnDel)

        parent.nom_table_window.setLayout(items_vbox)
        parent.nom_table_window.show()

        # Считаем количество записей до сохранения
        query = QtSql.QSqlQuery()
        query.exec("SELECT COUNT(*) AS old_count FROM nomenclature")
        query.next()
        recordCount = query.record()
        old_count_int = query.value(recordCount.indexOf("old_count"))
        query.finish()
        print(nm.dataChanged.connect(nm.submitAll))

        screen = QDesktopWidget().screenGeometry()
        x = int((screen.width() - parent.nom_table_window.width()) / 2)
        y = int((screen.height() - parent.nom_table_window.height()) / 2)
        parent.nom_table_window.move(x, y)

    #! Справочник 'Единицы измерения'
    def on_un_catalog_btn(parent, db_path):
        def on_add_unit():
            unm.insertRow(unm.rowCount())

        def on_del_unit():
            unm.removeRow(unmv.currentIndex().row())
            unm.select()

        def on_data_change(unm):

            unm.submitAll()
            # Считаем количество записей после сохранения
            query = QtSql.QSqlQuery()
            query.exec("SELECT COUNT(*) AS new_count FROM units")
            query.next()
            recordCount = query.record()
            new_count_int = query.value(recordCount.indexOf("new_count"))

            if old_count_int != new_count_int:
                msg_lbl = QLabel(
                    '<span style="color:green">Добавлена новая единица измерения</span>')
                parent.sm_list_widget.clear()
                parent.item = QListWidgetItem()
                parent.sm_list_widget.addItem(parent.item)
                parent.sm_list_widget.setItemWidget(parent.item, msg_lbl)

        # Устанавливаем соединение с базой данных
        con = QtSql.QSqlDatabase.addDatabase('QSQLITE')
        con.setDatabaseName(db_path)
        con.open()

        parent.un_table_window = QWidget()
        parent.un_table_window.setWindowModality(QtCore.Qt.ApplicationModal)
        parent.un_table_window.setWindowTitle("Единицы измерения")
        parent.un_table_window.resize(100, 250)

        unm = QtSql.QSqlTableModel(parent=parent.un_table_window)
        unm.setTable('units')
        unm.setSort(0, QtCore.Qt.AscendingOrder)
        unm.select()

        unm.setHeaderData(0, QtCore.Qt.Horizontal, 'Единица измерения')

        unmv = QTableView()
        unmv.setModel(unm)
        unmv.setColumnWidth(0, 150)

        vbox = QVBoxLayout()
        vbox.addWidget(unmv)
        btnAdd = QPushButton("Добавить единицу измерения")
        btnAdd.clicked.connect(on_add_unit)
        vbox.addWidget(btnAdd)
        btnDel = QPushButton("Удалить единицу измерения")
        btnDel.clicked.connect(on_del_unit)
        vbox.addWidget(btnDel)
        parent.un_table_window.setLayout(vbox)

        parent.un_table_window.show()

        # Считаем количество записей до сохранения
        query = QtSql.QSqlQuery()
        query.exec("SELECT COUNT(*) AS old_count FROM units")
        query.next()
        recordCount = query.record()
        old_count_int = query.value(recordCount.indexOf("old_count"))
        query.finish()

        unm.dataChanged.connect(lambda: on_data_change(unm))

        screen = QDesktopWidget().screenGeometry()
        x = int((screen.width() - parent.un_table_window.width()) / 2)
        y = int((screen.height() - parent.un_table_window.height()) / 2)
        parent.un_table_window.move(x, y)

    #! Справочник 'Поставщики'
    def on_s_catalog_btn(parent, db_path):
        def on_add_supp():
            sm.insertRow(sm.rowCount())

        def on_del_supp():
            sm.removeRow(smv.currentIndex().row())
            # Выполняем повторное считывание данных в модель,
            # чтобы убрать пустую "мусорную" запись
            sm.select()

        def on_data_change(sm):
            sm.submitAll()
            # Считаем количество записей после сохранения
            query = QtSql.QSqlQuery()
            query.exec("SELECT COUNT(*) AS new_count FROM suppliers")
            query.next()
            recordCount = query.record()
            new_count_int = query.value(recordCount.indexOf("new_count"))

            if old_count_int != new_count_int:
                msg_lbl = QLabel(
                    '<span style="color:green">Добавлен новый поставщик</span>')
                parent.sm_list_widget.clear()
                parent.item = QListWidgetItem()
                parent.sm_list_widget.addItem(parent.item)
                parent.sm_list_widget.setItemWidget(parent.item, msg_lbl)

        # Устанавливаем соединение с базой данных
        con = QtSql.QSqlDatabase.addDatabase('QSQLITE')
        con.setDatabaseName(db_path)
        con.open()

        # Создаем окно-таблицу
        parent.supp_table_window = QWidget()
        parent.supp_table_window.setWindowModality(QtCore.Qt.ApplicationModal)
        parent.supp_table_window.setWindowTitle("Поставщики")
        parent.supp_table_window.resize(740, 250)

        sm = QtSql.QSqlTableModel(parent=parent.supp_table_window)
        sm.setTable('suppliers')
        sm.setSort(0, QtCore.Qt.AscendingOrder)
        sm.select()

        sm.setHeaderData(1, QtCore.Qt.Horizontal, 'Название')
        sm.setHeaderData(2, QtCore.Qt.Horizontal, 'Форма собственности')
        sm.setHeaderData(3, QtCore.Qt.Horizontal, 'Адрес')
        sm.setHeaderData(4, QtCore.Qt.Horizontal, 'Телефон')
        sm.setHeaderData(5, QtCore.Qt.Horizontal, 'e-mail')

        smv = QTableView()
        smv.setModel(sm)

        smv.setColumnWidth(1, 150)
        smv.setColumnWidth(2, 150)
        smv.setColumnWidth(3, 200)
        smv.setColumnWidth(4, 100)
        smv.setColumnWidth(5, 100)
        smv.hideColumn(0)

        vbox = QVBoxLayout()
        vbox.addWidget(smv)
        btnAdd = QPushButton("Добавить поставщика")
        btnAdd.clicked.connect(on_add_supp)
        vbox.addWidget(btnAdd)
        btnDel = QPushButton("Удалить поставщика")
        btnDel.clicked.connect(on_del_supp)
        vbox.addWidget(btnDel)
        parent.supp_table_window.setLayout(vbox)

        parent.supp_table_window.show()

        # Считаем количество записей до сохранения
        query = QtSql.QSqlQuery()
        query.exec("SELECT COUNT(*) AS old_count FROM suppliers")
        query.next()
        recordCount = query.record()
        old_count_int = query.value(recordCount.indexOf("old_count"))
        query.finish()

        sm.dataChanged.connect(lambda: on_data_change(sm))

        screen = QDesktopWidget().screenGeometry()
        x = int((screen.width() - parent.supp_table_window.width()) / 2)
        y = int((screen.height() - parent.supp_table_window.height()) / 2)
        parent.supp_table_window.move(x, y)

    #! Справочник 'Должности'
    def on_p_catalog_btn(parent, db_path):
        def on_add_position():
            pm.insertRow(pm.rowCount())

        def on_del_position():
            pm.removeRow(pmv.currentIndex().row())
            pm.select()

        def on_data_change(pm):
            pm.submitAll()
            # Считаем количество записей после сохранения
            query = QtSql.QSqlQuery()
            query.exec("SELECT COUNT(*) AS new_count FROM positions")
            query.next()
            recordCount = query.record()
            new_count_int = query.value(recordCount.indexOf("new_count"))

            if old_count_int != new_count_int:
                msg_lbl = QLabel(
                    '<span style="color:green">Добавлена новая должность</span>')
                parent.sm_list_widget.clear()
                parent.item = QListWidgetItem()
                parent.sm_list_widget.addItem(parent.item)
                parent.sm_list_widget.setItemWidget(parent.item, msg_lbl)

        con = QtSql.QSqlDatabase.addDatabase('QSQLITE')
        con.setDatabaseName(db_path)
        con.open()

        parent.positions_table_window = QWidget()
        parent.positions_table_window.setWindowModality(
            QtCore.Qt.ApplicationModal)
        parent.positions_table_window.setWindowTitle("Список должностей")
        parent.positions_table_window.resize(205, 250)

        pm = QtSql.QSqlTableModel(parent=parent.positions_table_window)
        pm.setTable('positions')
        pm.setSort(0, QtCore.Qt.AscendingOrder)
        pm.select()

        pm.setHeaderData(0, QtCore.Qt.Horizontal, 'Должность')

        pmv = QTableView()
        pmv.setModel(pm)

        pmv.setColumnWidth(0, 200)

        vbox = QVBoxLayout()
        vbox.addWidget(pmv)

        btnAdd = QPushButton("Добавить должность")
        btnAdd.clicked.connect(on_add_position)
        vbox.addWidget(btnAdd)
        btnDel = QPushButton("Удалить должность")
        btnDel.clicked.connect(on_del_position)
        vbox.addWidget(btnDel)
        parent.positions_table_window.setLayout(vbox)

        parent.positions_table_window.show()

        # Считаем количество записей до сохранения
        query = QtSql.QSqlQuery()
        query.exec("SELECT COUNT(*) AS old_count FROM positions")
        query.next()
        recordCount = query.record()
        old_count_int = query.value(recordCount.indexOf("old_count"))
        query.finish()

        pm.dataChanged.connect(lambda: on_data_change(pm))

        screen = QDesktopWidget().screenGeometry()
        x = int((screen.width() - parent.positions_table_window.width()) / 2)
        y = int((screen.height() - parent.positions_table_window.height()) / 2)
        parent.positions_table_window.move(x, y)

    #! Справочник 'Сотрудники'
    def on_e_catalog_btn(parent, db_path):
        def on_add_employee():
            em.insertRow(em.rowCount())

        def on_del_employee():
            em.removeRow(emv.currentIndex().row())
            em.select()

        def on_data_change(em):
            em.submitAll()
            # Считаем количество записей после сохранения
            query = QtSql.QSqlQuery()
            query.exec("SELECT COUNT(*) AS new_count FROM employee")
            query.next()
            recordCount = query.record()
            new_count_int = query.value(recordCount.indexOf("new_count"))

            if old_count_int != new_count_int:
                msg_lbl = QLabel(
                    '<span style="color:green">Добавлен новый сотрудник</span>')
                parent.sm_list_widget.clear()
                parent.item = QListWidgetItem()
                parent.sm_list_widget.addItem(parent.item)
                parent.sm_list_widget.setItemWidget(parent.item, msg_lbl)

        con = QtSql.QSqlDatabase.addDatabase('QSQLITE')
        con.setDatabaseName(db_path)
        con.open()

        parent.employee_table_window = QWidget()
        parent.employee_table_window.setWindowModality(
            QtCore.Qt.ApplicationModal)
        parent.employee_table_window.setWindowTitle("Список сотрудников")
        parent.employee_table_window.resize(240, 250)

        em = QtSql.QSqlRelationalTableModel(
            parent=parent.employee_table_window)
        em.setTable('employee')
        em.setSort(0, QtCore.Qt.AscendingOrder)
        em.setRelation(
            2,
            QtSql.QSqlRelation(
                'positions',
                'position',
                'position'))
        em.select()

        em.setHeaderData(1, QtCore.Qt.Horizontal, 'ФИО')
        em.setHeaderData(2, QtCore.Qt.Horizontal, 'Должность')

        emv = QTableView()
        emv.setModel(em)

        emv.setItemDelegate(QtSql.QSqlRelationalDelegate(emv))
        emv.hideColumn(0)

        vbox = QVBoxLayout()
        vbox.addWidget(emv)

        btnAdd = QPushButton("Добавить сотрудника")
        btnAdd.clicked.connect(on_add_employee)
        vbox.addWidget(btnAdd)
        btnDel = QPushButton("Удалить сотрудника")
        btnDel.clicked.connect(on_del_employee)
        vbox.addWidget(btnDel)
        parent.employee_table_window.setLayout(vbox)

        parent.employee_table_window.show()

        # Считаем количество записей до сохранения
        query = QtSql.QSqlQuery()
        query.exec("SELECT COUNT(*) AS old_count FROM employee")
        query.next()
        recordCount = query.record()
        old_count_int = query.value(recordCount.indexOf("old_count"))
        query.finish()

        em.dataChanged.connect(lambda: on_data_change(em))

        screen = QDesktopWidget().screenGeometry()
        x = int((screen.width() - parent.employee_table_window.width()) / 2)
        y = int((screen.height() - parent.employee_table_window.height()) / 2)
        parent.employee_table_window.move(x, y)
