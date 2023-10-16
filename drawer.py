from data_and_processing import IntensityField
from graph import Graph
from mpl_toolkits.axes_grid1 import make_axes_locatable
# from mpl_toolkits.mplot3d.axes3d import Axes3D
# from matplotlib.ticker import LinearLocator

import numpy as np


# ШАБЛОНЫ ОТРИСОВКИ ГРАФИКОВ
# Очистка и подпись графика (вызывается в начале)
def cleaning_and_chart_graph(graph: Graph, x_label, y_label, title):
    graph.toolbar.home()  # Возвращаем зум в домашнюю позицию
    graph.toolbar.update()  # Очищаем стек осей (от старых x, y lim)
    # Очищаем график
    graph.axis.clear()
    # Задаем название осей
    graph.axis.set_xlabel(x_label)
    graph.axis.set_ylabel(y_label)
    # Задаем название графика
    graph.axis.set_title(title)


# Отрисовка (вызывается в конце)
def draw_graph(graph: Graph):
    # Убеждаемся, что все помещается внутри холста
    graph.figure.tight_layout()
    # Показываем новую фигуру в интерфейсе
    graph.canvas.draw()


# Отрисовка при отсутствии данных
def no_data(graph: Graph):
    graph.axis.text(0.5, 0.5, "Нет данных",
                    fontsize=14,
                    horizontalalignment='center',
                    verticalalignment='center')
    # Отрисовка, без подписи данных графиков
    draw_graph(graph)


# Класс художник. Имя холст (graph), рисует на нем данные
class Drawer:
    # ПАРАМЕТРЫ ГРАФИКОВ
    horizontal_axis_name_data = "X"
    vertical_axis_name_data = "Y"

    # ОТРИСОВКИ
    # (1) 2d интенсивность вид сверху
    @staticmethod
    def gray_2d(
            graph: Graph,
            data: IntensityField
    ):

        # Очистка, подпись графика и осей (вызывается в начале)
        cleaning_and_chart_graph(
            # Объект графика
            graph=graph,
            # Название графика
            title=graph.name_graphics,
            # Подпись осей
            x_label=Drawer.horizontal_axis_name_data, y_label=Drawer.vertical_axis_name_data
        )

        # Рисуем график
        im = graph.axis.imshow(data.field, cmap='gray', extent=[-data.radius, data.radius,
                                                                -data.radius, data.radius])

        # Если color bar нет- создаем, иначе обновляем
        if not graph.colorbar:
            divider = make_axes_locatable(graph.axis)
            cax = divider.append_axes("right", "10%", pad="3%")
            graph.colorbar = graph.figure.colorbar(im, orientation='vertical', cax=cax)
        else:
            graph.colorbar.update_normal(im)

        # Отрисовка (вызывается в конце)
        draw_graph(graph)

    # (2) 3d интенсивность
    @staticmethod
    def gray_3d(
            graph: Graph,
            data: IntensityField
    ):

        # Очистка, подпись графика и осей (вызывается в начале)
        cleaning_and_chart_graph(
            # Объект графика
            graph=graph,
            # Название графика
            title=graph.name_graphics,
            # Подпись осей
            x_label=Drawer.horizontal_axis_name_data, y_label=Drawer.vertical_axis_name_data
        )

        # ВАРИАНТ ОТРИСОВКИ ЧЕРЕЗ - ПРЯМОУГОЛЬНИКИ (красиво, но очень медленный и тяжелый)
        # _x = np.arange(0, data.cells_side, 1)
        # _y = np.arange(0, data.cells_side, 1)
        # _xx, _yy = np.meshgrid(_x, _y)
        # x, y = _xx.ravel(), _yy.ravel()
        #
        # top = data.field.ravel()
        # print(top)
        # bottom = np.zeros_like(top)
        # width = depth = 1
        #
        # graph.axis.bar3d(x, y, bottom, width, depth, top, shade=True)

        # ВАРИАНТ ОТРИСОВКИ ЧЕРЕЗ - ПОВЕРХНОСТИ
        x = np.arange(-data.cells_radius, data.cells_radius + 1, 1) * data.radius_step
        y = np.arange(-data.cells_radius, data.cells_radius + 1, 1) * data.radius_step
        x, y = np.meshgrid(x, y)

        # Построение поверхности
        graph.axis.plot_surface(x, y, data.field, cmap=graph.axis.cm.coolwarm,
                                linewidth=0, antialiased=True)

        # Отрисовка (вызывается в конце)
        draw_graph(graph)
