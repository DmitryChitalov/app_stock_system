# -*- coding: utf-8 -*-
#-----------------------Импорт модулей и внешних классов-----------------------#

from PyQt5 import QtCore
from PyQt5 import QtGui

from PyQt5.QtWidgets import QMainWindow, QAction, QDockWidget, \
    QFrame, QListWidget, QDesktopWidget, QApplication, \
    QStyle, QLabel, QLineEdit, QHBoxLayout, QGridLayout, QTreeView, \
    QScrollArea, QTableView, QWidget, QVBoxLayout, QPushButton, \
    QFormLayout, QComboBox, QListWidgetItem, QSpinBox, QDoubleSpinBox, \
    QFileDialog

import sqlite3

#--------------------Разметка формы приходного ордера--------------------------#
class ro_order_form_class:
    def on_form_open(db_path, add_functions_class, ro_order_window, parent, ro_orders_table, ro_orders_model):
        def on_name_changed():
            con = sqlite3.connect(db_path)
            cur = con.cursor()

            cur_name = name_edit.currentText()

            # Подаставляем номер
            sql_item_numb = """\
            SELECT item_numb FROM nomenclature WHERE item_name=?
            """
            cur.execute(sql_item_numb, (cur_name,))
            cur_numb = cur.fetchone()
            numb_edit.setValue(cur_numb[0])

            # Подаставляем ед. изм
            sql_item_unit = """\
            SELECT item_unit FROM nomenclature WHERE item_name=?
            """
            cur.execute(sql_item_unit, (cur_name,))
            cur_unit = cur.fetchone()

            unit_edit_mas = unit_edit.count()
            for i in range(unit_edit_mas):
                if unit_edit.itemText(i) == cur_unit[0]:
                    unit_edit.setCurrentIndex(i)

            # Подставляем категорию
            sql_item_cat = """\
            SELECT item_cat FROM nomenclature WHERE item_name=?
            """
            cur.execute(sql_item_cat, (cur_name,))
            cur_cat = cur.fetchone()

            cat_edit_mas = cat_edit.count()

            for i in range(cat_edit_mas):
                if cat_edit.itemText(i) == cur_cat[0]:
                    cat_edit.setCurrentIndex(i)

            cur.close()
            con.close()

        def on_ro_form_btnCancel():
            ro_order_window.ro_order_form_window.close()

        def on_ro_form_btnSave():

            con = sqlite3.connect(db_path)
            cur = con.cursor()

            sql_ro_insert = "INSERT INTO ro_orders (numb, name, cat, unit, quant, price, supp) VALUES (?, ?, ?, ?, ?, ?, ?)"
            numb_val = numb_edit.value()
            name_val = name_edit.currentText()
            cat_val = cat_edit.currentText()
            unit_val = unit_edit.currentText()
            quant_val = quant_edit.value()
            price_val = price_edit.value()
            supp_val = supp_edit.currentText()
            sql_ro_values = (numb_val, name_val, cat_val, unit_val, quant_val, price_val, supp_val)
            cur.execute(sql_ro_insert, sql_ro_values)
            con.commit()

            ro_order_window.ro_order_form_window.close()

            ro_orders_model = add_functions_class.all_ro_orders_print(parent, db_path)
            ro_orders_table.setModel(ro_orders_model)
            #создаем еще одну дополнительную таблицу с: название товара, количество

            sql_item_pos = """\
            SELECT item_name FROM items_positions WHERE item_name = ?
            """
            cur.execute(sql_item_pos, (name_val,))
            cur_item_pos = cur.fetchone()

            if cur_item_pos is None:
                sql_pos_insert = "INSERT INTO items_positions (item_name, item_amount) VALUES (?, ?)"
                sql_pos_values = (name_val, quant_val)
                cur.execute(sql_pos_insert, sql_pos_values)
            else:
                sql_item_quant = """\
                SELECT item_amount FROM items_positions WHERE item_name = ?
                """
                cur.execute(sql_item_quant, (name_val,))
                cur_item_quant = cur.fetchone()
                item_amount = cur_item_quant[0] + quant_val

                sql_amount_upd = "UPDATE items_positions SET item_amount = ? WHERE item_name = ?"
                cur.execute(sql_amount_upd, (item_amount, name_val))

            con.commit()

            cur.close()
            con.close()

        con = sqlite3.connect(db_path)
        cur = con.cursor()

        # Названия полей
        numb_label = QLabel('Номенклатурный номер:')
        name_label = QLabel('Наименование:')
        cat_label = QLabel('Категория:')
        unit_label = QLabel('Ед.измерения:')
        quant_label = QLabel('Количество:')
        price_label = QLabel('Цена:')
        supp_label = QLabel('Поставщик:')

        # Поля

        ##-Наименование
        con = sqlite3.connect(db_path)
        cur = con.cursor()
        sql_name = """\
        SELECT item_name FROM nomenclature ORDER BY rowid
        """
        cur.execute(sql_name)
        name_arr = cur.fetchall()
        name_list = [el[0] for el in name_arr]

        name_edit = QComboBox()
        name_edit.setFixedSize(300, 25)
        name_edit.addItems(name_list)
        name_edit.activated.connect(on_name_changed)
        item_name_txt = name_edit.currentText()

        ##-Номенклатурный номер
        numb_edit = QSpinBox()
        numb_edit.setFixedSize(100, 25)
        numb_edit.setRange(0, 10000000)
        numb_edit.setEnabled(False)
        sql_numb_first = """\
        SELECT item_numb FROM nomenclature where item_name = ?
        """
        cur.execute(sql_numb_first, (item_name_txt,))
        first_numb = cur.fetchone()
        numb_edit.setValue(first_numb[0])

        ##-Категория
        sql_cat = """\
        SELECT item_cat FROM nomenclature where item_name = ?
        """
        cur.execute(sql_cat, (item_name_txt,))
        first_cat = cur.fetchone()

        sql_cat_all = """\
        SELECT category FROM categories
        """
        cur.execute(sql_cat_all)
        cat_arr = cur.fetchall()

        cat_list = [el[0] for el in cat_arr]

        cat_edit = QComboBox()
        cat_edit.setFixedSize(200, 25)
        cat_edit.addItems(cat_list)

        cat_edit_mas = cat_edit.count()
        for i in range(cat_edit_mas):
            if cat_edit.itemText(i) == first_cat[0]:
                cat_edit.setCurrentIndex(i)

        ##-Ед. измерения
        cur = con.cursor()
        sql_units = """\
        SELECT item_unit FROM nomenclature where item_name = ?
        """
        cur.execute(sql_units, (item_name_txt,))
        first_unit = cur.fetchone()

        sql_units_all = """\
        SELECT unit FROM units
        """
        cur.execute(sql_units_all)
        unit_arr = cur.fetchall()

        unit_list = [el[0] for el in unit_arr]

        unit_edit = QComboBox()
        unit_edit.addItems(unit_list)
        unit_edit.setFixedSize(100, 25)

        unit_edit_mas = unit_edit.count()
        for i in range(unit_edit_mas):
            if unit_edit.itemText(i) == first_unit[0]:
                unit_edit.setCurrentIndex(i)

        ##-Количество
        quant_edit = QSpinBox()
        quant_edit.setFixedSize(100, 25)
        quant_edit.setRange(0, 1000000)

        ##-Цена
        price_edit = QDoubleSpinBox()
        price_edit.setFixedSize(100, 25)
        price_edit.setRange(0.00, 1000000.00)

        ##-Постпавщик
        sql_supp = """\
        SELECT supplier FROM suppliers ORDER BY rowid
        """
        cur.execute(sql_supp)
        supp_arr = cur.fetchall()
        supp_list = [el[0] for el in supp_arr]

        cur.close()
        con.close()

        supp_edit = QComboBox()
        supp_edit.setFixedSize(100, 25)
        supp_edit.addItems(supp_list)

        ### Размещаем все компоненты
        ro_order_form_grid = QGridLayout()

        ro_order_form_grid = QGridLayout()
        ro_order_form_grid.addWidget(numb_label, 0, 0, alignment=QtCore.Qt.AlignCenter)
        ro_order_form_grid.addWidget(numb_edit, 0, 1, alignment=QtCore.Qt.AlignCenter)

        ro_order_form_grid.addWidget(name_label, 1, 0, alignment=QtCore.Qt.AlignCenter)
        ro_order_form_grid.addWidget(name_edit, 1, 1, alignment=QtCore.Qt.AlignCenter)

        ro_order_form_grid.addWidget(cat_label, 2, 0, alignment=QtCore.Qt.AlignCenter)
        ro_order_form_grid.addWidget(cat_edit, 2, 1, alignment=QtCore.Qt.AlignCenter)

        ro_order_form_grid.addWidget(unit_label, 3, 0, alignment=QtCore.Qt.AlignCenter)
        ro_order_form_grid.addWidget(unit_edit, 3, 1, alignment=QtCore.Qt.AlignCenter)

        ro_order_form_grid.addWidget(quant_label, 4, 0, alignment=QtCore.Qt.AlignCenter)
        ro_order_form_grid.addWidget(quant_edit, 4, 1, alignment=QtCore.Qt.AlignCenter)

        ro_order_form_grid.addWidget(price_label, 5, 0, alignment=QtCore.Qt.AlignCenter)
        ro_order_form_grid.addWidget(price_edit, 5, 1, alignment=QtCore.Qt.AlignCenter)

        ro_order_form_grid.addWidget(supp_label, 6, 0, alignment=QtCore.Qt.AlignCenter)
        ro_order_form_grid.addWidget(supp_edit, 6, 1, alignment=QtCore.Qt.AlignCenter)

        ro_order_form_frame = QFrame()
        ro_order_form_frame.setStyleSheet(open("./styles/properties_form_style.qss","r").read())
        ro_order_form_frame.setLayout(ro_order_form_grid)

		#-----------------------------Кнопки формы--------------------------#

        ro_order_form_btnSave = QPushButton('Сохранить')
        ro_order_form_btnSave.setFixedSize(80, 25)
        ro_order_form_btnSave.clicked.connect(on_ro_form_btnSave)

        ro_order_form_btnCancel = QPushButton('Отмена')
        ro_order_form_btnCancel.setFixedSize(80, 25)
        ro_order_form_btnCancel.clicked.connect(on_ro_form_btnCancel)

        buttons_hbox = QHBoxLayout()
        buttons_hbox.addWidget(ro_order_form_btnSave)
        buttons_hbox.addWidget(ro_order_form_btnCancel)

		# --------------------Размещение на форме всех компонентов---------#

        ro_order_form_grid = QGridLayout()
        ro_order_form_grid.addWidget(ro_order_form_frame, 0, 0, alignment=QtCore.Qt.AlignCenter)
        ro_order_form_grid.addLayout(buttons_hbox, 1, 0, alignment=QtCore.Qt.AlignCenter)

        ro_order_window.ro_order_form_window = QWidget()
        ro_order_window.ro_order_form_window.setWindowModality(QtCore.Qt.ApplicationModal)
        ro_order_window.ro_order_form_window.setWindowTitle("Приходный ордер")

        ro_order_window.ro_order_form_window.setLayout(ro_order_form_grid)
        ro_order_window.ro_order_form_window.show()
