# Класс хранения данных расположение антенн и их координат
# Методов обработки и получения данных
import numpy as np
import math
import cmath


# Базовый класс. Для хранения матрицы значений и её диапазонов по осям x, y
class Field:
    def __init__(self):
        # Марица расстановки антенн
        self.cells_radius = None  # Кол-во ячеек в радиусе
        self.cells_side = None  # Кол-во всего ячеек на стороне 2*radius+1

        # Значения области антенн
        self.radius = None  # Радиус
        self.radius_step = None  # Шаг по радиусу

        # Матрица с расстановкой антенн
        self.field = None

        # Заполнение матрицы / тип
        self.empty_cell_field = False

    # Создание 2d массива для значений, по заданным параметрам
    def field_initialization(self,
                             cells_radius,
                             radius):
        self.radius = radius  # Значение радиуса
        self.cells_radius = cells_radius  # Ячеек в радиусу

        # Количество всего строк или столбцов
        self.cells_side = self.cells_radius * 2 + 1

        # Создаем матрицу значений - данных
        self.field = np.full((self.cells_side, self.cells_side), self.empty_cell_field)

        self.radius_step = self.radius / self.cells_radius


# Класс наследник поля. Для хранения поля антенн и получения координат антенн
class ButtonField(Field):
    def __init__(self):
        Field.__init__(self)

        # Массив координат антенн
        self.antenna_x = None
        self.antenna_y = None

    # Получение координат антенн
    # В матрице значение true - означает наличие антенны в клетке
    # По индексам антенны находим её координаты
    def antenna_radius(self):
        # Поля нет - сброс
        if self.field is None:
            return

        # Если ничего не выбрано - сброс
        if self.field.sum() == 0:
            return

        # Создаем массивы координат
        self.antenna_x = np.zeros(self.field.sum())
        self.antenna_y = np.zeros(self.field.sum())

        # Перебираем ячейки
        index_for_record = 0
        for column in range(self.cells_side):
            for row in range(self.cells_side):
                # Если в ячейке антенна
                if self.field[row][column]:
                    # Переводим в координаты, заносим в массив
                    self.antenna_x[index_for_record] = (-self.cells_radius + column) * self.radius_step
                    self.antenna_y[index_for_record] = (self.cells_radius - row) * self.radius_step
                    # Сдвигаем индекс записи
                    index_for_record += 1


# Класс наследник поля. Для хранения и расчета интенсивностей в точках сферы
class IntensityField(Field):
    def __init__(self):
        Field.__init__(self)

        self.empty_cell_field = 0.0     # Значение заполнения матрицы
        self.wave_length = 1    # Длинна волны
        self.k = (2 * cmath.pi) / self.wave_length  # Волновой вектор

    # Расчет интенсивностей по полю антенн
    def intensity_calculation(self, antenna_field: ButtonField):
        # Поля нет - сброс
        if self.field is None:
            return

        # Поля антенн нет - сброс
        if antenna_field.field is None:
            return

        # Находим координаты радиусов
        antenna_field.antenna_radius()

        # Перебираем ячейки
        for column in range(self.cells_side):
            for row in range(self.cells_side):
                # Координата в которой находимся
                x = (-self.cells_radius + column) * self.radius_step
                y = (self.cells_radius - row) * self.radius_step

                # Радиус от выбранной точки матрицы до центра
                # смотрим попадание в купол
                r_2d = math.sqrt(x * x + y * y)

                # Если за пределом радиуса - сброс итерации
                if r_2d > self.radius:
                    continue

                # Считаем проекцию на сферу -> z
                '''
                 Уравнение сферы: (x - x0)^2 + (y - y0)^2 + (z - z0)^2 = R^2
                 Сфера в начале координат: x^2 + y^2 + z^2 = R^2
                 Координата z: z = sqrt( R^2 - x^2 - y^2 )
                 '''
                z = math.sqrt(self.radius * self.radius - x * x - y * y)
                # Считаем интенсивность; z - антенн считаем 0
                z_pow_2 = z * z
                source_radius = np.sqrt((x - antenna_field.antenna_x) ** 2 +
                                        (y - antenna_field.antenna_y) ** 2 +
                                        z_pow_2)

                # Считаем сумму интенсивностей от каждой антенны
                intensity = 0
                for radius_i in source_radius:
                    intensity += (1 / radius_i) * cmath.exp(complex(0.0, 1.0) * self.k * radius_i)

                # В ячейку поля заносим модуль интенсивности
                self.field[row][column] = abs(intensity)
