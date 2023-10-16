import functools

from PyQt5.QtWidgets import (
    QGridLayout,
    QPushButton,
    QSizePolicy
)

from data_and_processing import ButtonField, IntensityField
from drawer import Drawer
from graph import Graph
from gui import Ui_Dialog


# КЛАСС АЛГОРИТМА ПРИЛОЖЕНИЯ
class GuiProgram(Ui_Dialog):

    def __init__(self, dialog):
        # Создаем окно
        Ui_Dialog.__init__(self)
        self.setupUi(dialog)  # Устанавливаем пользовательский интерфейс

        # ПОЛЯ КЛАССА
        # Параметры 1 графика
        self.graph_intensity_2d = Graph(
            layout=self.layout_plot_2,
            widget=self.widget_plot_2
        )
        # Параметры 2 графика
        self.graph_intensity_3d = Graph(
            layout=self.layout_plot_3,
            widget=self.widget_plot_3,
            tridimensional=True
        )
        # Данные нахождения антенн и интенсивности
        self.data_button_field = ButtonField()
        self.data_intensity_field = IntensityField()

        # Стиль кнопок
        self.text_color = "color: rgb(255, 255, 255);"
        self.empty_field_color = "background-color: rgb(33, 37, 43);"
        self.axis_color_x = "background-color: rgb(187, 55, 45);"
        self.axis_color_y = "background-color: rgb(52, 163, 73);"
        self.antenna_color = "background-color: rgb(36, 78, 229);"

        # Слой QGridLayout под кнопки
        self.layout_button_field = QGridLayout()

        # ДЕЙСТВИЯ ПРИ ВКЛЮЧЕНИИ
        self.pushButton_display_antenna_installation_field.clicked.connect(self.initialize_button_field)
        self.pushButton_start_processing.clicked.connect(self.intensity_calculation)

    # ( I ) ПОЛЕ КНОПОК ПОЛЯ КНОПОК УСТАНОВКИ АНТЕН
    # (1) СОЗДАНИЕ
    def initialize_button_field(self):
        # Очищаем от старых кнопок
        self.delete_button_field()

        # Получаем количество ячеек на радиус
        number_cells = int(self.lineEdit_number_cells_of_antenna_field.text())

        # Находим значения радиуса
        radius = float(self.lineEdit_radius_of_cells_of_antenna_field.text())

        # Сохраняем параметры, считаем матрицу антенн
        self.data_button_field = ButtonField()
        self.data_button_field.field_initialization(number_cells, radius)

        size_policy = QSizePolicy(QSizePolicy.Expanding,
                                  QSizePolicy.Expanding)  # Установка размерной политики для кнопки

        # Проходим по ячейкам и задаем кнопки
        for column in range(self.data_button_field.cells_side):
            for row in range(self.data_button_field.cells_side):
                # Создаем кнопку и задаем её текст (координата)
                button = QPushButton(
                    f""" x: {(-self.data_button_field.cells_radius + column) * self.data_button_field.radius_step}
y: {(self.data_button_field.cells_radius - row) * self.data_button_field.radius_step}""")

                # Устанавливаем политику размера
                button.setSizePolicy(size_policy)

                # Устанавливаем стиль
                if row == self.data_button_field.cells_radius:
                    button.setStyleSheet(self.text_color + self.axis_color_x)
                elif column == self.data_button_field.cells_radius:
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

    # (2) ОЧИСТКА
    def delete_button_field(self):
        for i in reversed(range(self.layout_button_field.count())):
            self.layout_button_field.itemAt(i).widget().deleteLater()

    # (3) ОБРАБОТКА НАЖАТИЯ КНОПКИ - УСТАНОВКА АНТЕНЫ
    def button_selection(self, row, column, button):
        # Меняем предыдущее значение на противоположное
        self.data_button_field.field[row][column] = not self.data_button_field.field[row][column]
        # Задаем цвет
        # Если ячейка с антенной - цвет антенны
        if self.data_button_field.field[row][column]:
            button.setStyleSheet(self.text_color + self.antenna_color)
        # Иначе восстанавливаем исходный цвет
        else:
            # Строка посередине - ось x, закрашиваем особым цветом
            if row == self.data_button_field.cells_radius:
                button.setStyleSheet(self.text_color + self.axis_color_x)
            # Колонка посередине - ось y, закрашиваем особым цветом
            elif column == self.data_button_field.cells_radius:
                button.setStyleSheet(self.text_color + self.axis_color_y)
            # Закраска пустых ячеек
            else:
                button.setStyleSheet(self.text_color + self.empty_field_color)

    # ( II ) РАСЧЕТ ИНТЕНСИВНОСТИ
    def intensity_calculation(self):
        # Проверяем что поле кнопок создано
        if self.data_button_field.field is None:
            return

        # Проверяем что антенны поставлены
        if self.data_button_field.field.sum() == 0:
            return

        # Получаем количество ячеек на радиус
        number_cells = int(self.lineEdit_number_cells_of_intensity.text())

        # Находим значения радиуса
        radius = float(self.lineEdit_radius_of_cells_of_intensity.text())

        # Сохраняем параметры, считаем матрицу антенн
        self.data_intensity_field = IntensityField()
        self.data_intensity_field.field_initialization(number_cells, radius)

        # Считаем интенсивность
        self.data_intensity_field.intensity_calculation(self.data_button_field)

        # Строим графики
        Drawer.gray_2d(self.graph_intensity_2d, self.data_intensity_field)
        Drawer.gray_3d(self.graph_intensity_3d, self.data_intensity_field)
