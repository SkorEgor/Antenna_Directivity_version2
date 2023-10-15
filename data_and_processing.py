# Класс хранения данных расположение антенн и их координат
# Методов обработки и получения данных
import numpy as np


class DataAndProcessing:
    def __init__(self):
        # Марица расстановки антенн
        self.cells_radius_x = None
        self.cells_radius_y = None

        self.cells_x = None
        self.cells_y = None

        self.field = None

        # Значения области антенн
        self.radius_x = None
        self.radius_y = None

        self.step_x = None
        self.step_y = None

    def field_initialization(self,
                             cells_radius_x, cells_radius_y,
                             radius_x, radius_y):
        self.cells_radius_x = cells_radius_x
        self.cells_radius_y = cells_radius_y

        self.radius_x = radius_x
        self.radius_y = radius_y

        # Количество всего строк и столбцов
        self.cells_x = self.cells_radius_x * 2 + 1
        self.cells_y = self.cells_radius_y * 2 + 1

        # Создаем матрицу значений - данных
        self.field = np.full((self.cells_y, self.cells_x), False)

        self.step_x = self.radius_x / self.cells_radius_x
        self.step_y = self.radius_y / self.cells_radius_y
