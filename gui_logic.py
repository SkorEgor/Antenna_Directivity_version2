from data_and_processing import DataAndProcessing
from gui import Ui_Dialog

import numpy as np
import functools

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication,
    QGridLayout,
    QPushButton,
    QWidget, QSizePolicy
)


# КЛАСС АЛГОРИТМА ПРИЛОЖЕНИЯ
class GuiProgram(Ui_Dialog):

    def __init__(self, dialog):
        # ПОЛЯ КЛАССА
        self.data_and_processing = DataAndProcessing()
        # Стиль кнопок
        self.text_color = "color: rgb(255, 255, 255);"
        self.empty_field_color = "background-color: rgb(33, 37, 43);"
        self.axis_color_x = "background-color: rgb(187, 55, 45);"
        self.axis_color_y = "background-color: rgb(52, 163, 73);"
        self.antenna_color = "background-color: rgb(36, 78, 229);"

        # Создаем слой QGridLayout под кнопки
        self.layout_button_field = QGridLayout()

        # ДЕЙСТВИЯ ПРИ ВКЛЮЧЕНИИ
        # Создаем окно
        Ui_Dialog.__init__(self)
        self.setupUi(dialog)  # Устанавливаем пользовательский интерфейс
        self.pushButton_display_antenna_installation_field.clicked.connect(self.initialize_button_field)

    def initialize_button_field(self):
        # Очищаем от старых кнопок
        self.delete_button_field()

        # Получаем количество строк и столбцов
        cells_radius_x = int(self.lineEdit_number_cells_x.text())
        cells_radius_y = int(self.lineEdit_number_cells_y.text())

        # Находим значения области
        radius_x = float(self.lineEdit_radius_x.text())
        radius_y = float(self.lineEdit_radius_y.text())

        # Сохраняем параметры, считаем матрицу антенн
        self.data_and_processing = DataAndProcessing()
        self.data_and_processing.field_initialization(cells_radius_x, cells_radius_y,
                                                      radius_x, radius_y)

        size_policy = QSizePolicy(QSizePolicy.Expanding,
                                  QSizePolicy.Expanding)  # Установка размерной политики для кнопки

        # Проходим по ячейкам и задаем кнопки
        for column in range(self.data_and_processing.cells_x):
            for row in range(self.data_and_processing.cells_y):
                # Создаем кнопку и задаем её текст (координата)
                button = QPushButton(
                    f""" x: {(self.data_and_processing.cells_radius_x - column) * self.data_and_processing.step_x}
y: {(self.data_and_processing.cells_radius_y - row) * self.data_and_processing.step_y}""")

                # Устанавливаем политику размера
                button.setSizePolicy(size_policy)

                # Устанавливаем стиль
                if row == self.data_and_processing.cells_radius_y:
                    button.setStyleSheet(self.text_color + self.axis_color_x)
                elif column == self.data_and_processing.cells_radius_x:
                    button.setStyleSheet(self.text_color + self.axis_color_y)
                else:
                    button.setStyleSheet(self.text_color + self.empty_field_color)
                button.sizePolicy()

                # Обработчик нажатия, с передачей отправителя
                button.clicked.connect(
                    functools.partial(
                        self.button_selection, row, column, button
                    )
                )

                # Добавляем кнопку на слой
                self.layout_button_field.addWidget(
                    button, row, column)

        # Добавляем слой в виджет
        self.widget_plot_1.setLayout(self.layout_button_field)

    def delete_button_field(self):
        for i in reversed(range(self.layout_button_field.count())):
            self.layout_button_field.itemAt(i).widget().deleteLater()

    def button_selection(self, row, column, button):
        # Меняем предыдущее значение на противоположное
        self.data_and_processing.field[row][column] = not self.data_and_processing.field[row][column]
        # Задаем цвет
        # Если ячейка с антенной - цвет антенны
        if self.data_and_processing.field[row][column]:
            button.setStyleSheet(self.text_color + self.antenna_color)
        # Иначе восстанавливаем исходный цвет
        else:
            if row == self.data_and_processing.cells_radius_y:
                button.setStyleSheet(self.text_color + self.axis_color_x)
            elif column == self.data_and_processing.cells_radius_x:
                button.setStyleSheet(self.text_color + self.axis_color_y)
            else:
                button.setStyleSheet(self.text_color + self.empty_field_color)
