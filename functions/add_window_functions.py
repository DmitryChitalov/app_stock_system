# -*- coding: utf-8 -*-
#--------------------------Импорт модулей и внешних форм-----------------------#

import sys
from PyQt5 import QtCore
import sqlite3
from PyQt5.QtWidgets import QMainWindow, QAction, QDockWidget, \
    QFrame, QListWidget, QDesktopWidget, QApplication, \
    QStyle, QLabel, QLineEdit, QHBoxLayout, QGridLayout, QTreeView, \
    QScrollArea, QTableView, QWidget, QVBoxLayout, QPushButton, \
    QDesktopWidget

from PyQt5.QtGui import QStandardItemModel, QStandardItem

class add_functions_class:

    # Модель со списком 'Приходных ордеров'
    def all_ro_orders_print(parent, db_path):

        con = sqlite3.connect(db_path)
        cur = con.cursor()
        sql_ro_orders_create = """\
        CREATE TABLE IF NOT EXISTS ro_orders (
            ro_order_id INTEGER PRIMARY KEY AUTOINCREMENT,
            numb INTEGER,
            name STRING,
            cat STRING,
            unit STRING,
            quant INTEGER,
            price DOUBLE,
            supp STRING
        );
        """

        cur.execute(sql_ro_orders_create)
        con.commit()

        # Создаем дополнительную таблицу 'Товары в наличии'
        sql_items_position_create = """\
        CREATE TABLE IF NOT EXISTS items_positions (
            item_name STRING PRIMARY KEY,
            item_amount INTEGER
        );
        """
        cur.execute(sql_items_position_create)
        con.commit()

        sql_ro_orders_list = """\
        SELECT ro_order_id, numb, name, cat, unit, quant, price, supp FROM ro_orders
        """
        cur.execute(sql_ro_orders_list)
        arr = cur.fetchall()

        cur.close()
        con.close()

        ro_orders_model = QStandardItemModel()
        ro_orders_model.setHorizontalHeaderLabels(
            [
                '№ ордера',
                'Номенклатурный №',
                'Название товара',
                'Категория',
                'Ед. измерения',
                'Количество',
                'Цена',
                'Поставщик'])

        k = 0
        for el in arr:

            ro_order_id = QStandardItem(str(el[0]))
            ro_orders_model.setItem(k, 0, ro_order_id)

            numb = QStandardItem(str(el[1]))
            ro_orders_model.setItem(k, 1, numb)

            name = QStandardItem(el[2])
            ro_orders_model.setItem(k, 2, name)

            cat = QStandardItem(el[3])
            ro_orders_model.setItem(k, 3, cat)

            unit = QStandardItem(el[4])
            ro_orders_model.setItem(k, 4, unit)

            quant = QStandardItem(str(el[5]))
            ro_orders_model.setItem(k, 5, quant)

            price = QStandardItem(str(el[6]))
            ro_orders_model.setItem(k, 6, price)

            supp = QStandardItem(el[7])
            ro_orders_model.setItem(k, 7, supp)

            k = k + 1

        return ro_orders_model

    # Модель со списком 'Расходных ордеров'
    def all_wo_orders_print(parent, db_path):

        con = sqlite3.connect(db_path)
        cur = con.cursor()
        sql_wo_orders_create = """\
        CREATE TABLE IF NOT EXISTS wo_orders (
            wo_order_id INTEGER PRIMARY KEY AUTOINCREMENT,
            numb INTEGER,
            name STRING,
            cat STRING,
            unit STRING,
            quant INTEGER,
            fio STRING,
            receiver STRING
        );
        """

        cur.execute(sql_wo_orders_create)
        con.commit()

        sql_wo_orders_list = """\
        SELECT wo_order_id, numb, name, cat, unit, quant, fio, receiver FROM wo_orders
        """
        cur.execute(sql_wo_orders_list)
        arr = cur.fetchall()

        cur.close()
        con.close()

        wo_orders_model = QStandardItemModel()
        wo_orders_model.setHorizontalHeaderLabels(
            [
                '№ ордера',
                'Номенклатурный №',
                'Название товара',
                'Категория',
                'Ед. измерения',
                'Количество',
                'ФИО',
                'Получатель'])

        k = 0
        for el in arr:

            wo_order_id = QStandardItem(str(el[0]))
            wo_orders_model.setItem(k, 0, wo_order_id)

            numb = QStandardItem(str(el[1]))
            wo_orders_model.setItem(k, 1, numb)

            name = QStandardItem(el[2])
            wo_orders_model.setItem(k, 2, name)

            cat = QStandardItem(el[3])
            wo_orders_model.setItem(k, 3, cat)

            unit = QStandardItem(el[4])
            wo_orders_model.setItem(k, 4, unit)

            quant = QStandardItem(str(el[5]))
            wo_orders_model.setItem(k, 5, quant)

            fio = QStandardItem(str(el[6]))
            wo_orders_model.setItem(k, 6, fio)

            receiver = QStandardItem(str(el[7]))
            wo_orders_model.setItem(k, 7, receiver)

            k = k + 1

        return wo_orders_model
