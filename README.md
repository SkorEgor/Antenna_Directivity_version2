<!---------------------------------------------------------------------------------->
<div align="left">
<img src="https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54" height=24> 
<img src="https://img.shields.io/badge/Matplotlib-%23ffffff.svg?style=for-the-badge&logo=Matplotlib&logoColor=black" height=24>
<img src="https://img.shields.io/badge/numpy-%23013243.svg?style=for-the-badge&logo=numpy&logoColor=white" height=24>
<img src="https://img.shields.io/badge/Qt-41CD52?style=for-the-badge&logo=Qt&logoColor=white" height=24>
</div>

<h1 align="center"> Antenna Directive / Направленность Антенн </h1>

Программа генерирует поле кнопок по заданным размерам. Каждая кнопка это ячейка куда можно поставить антенну. После обработки получаем значения интенсивности на сфере (в виде проекции на плоскость) в виде 3d и 2d графика
<!---------------------------------------------------------------------------------->

---

<h2 align="left"> Содержание </h2>

1. [ Описание задачи и демонстрация работы ](https://github.com/SkorEgor/Antenna_Directivity_version2#-1-описание-задачи-и-демонстрация-работы-)
2. [ Входные и выходные данные ](https://github.com/SkorEgor/Antenna_Directivity_version2#-2-входные-и-выходные-данные-)
3. [ Описание логической структуры - Алгоритм программы ](https://github.com/SkorEgor/Antenna_Directivity_version2#-3-описание-логической-структуры---алгоритм-программы-)
4. [ Структура программы - Классы и их описание](https://github.com/SkorEgor/Antenna_Directivity_version2#-4-структура-программы---классы-и-их-описание-)

<!---------------------------------------------------------------------------------->

---

<h2 align="left"> 1. Описание задачи и демонстрация работы </h2>
Результат работы приложения
<br><br>
<div align="center">
<!--- 1_general_view -->
<img src="https://raw.githubusercontent.com/SkorEgor/picturesgifs-for-readme/RobotControl/Antenna_Directive/1_general_view.jpg" >
</div>

Демонстрация работы
<div align="center">
<!--- 1_general_view -->
<img src="https://raw.githubusercontent.com/SkorEgor/picturesgifs-for-readme/RobotControl/Antenna_Directive/2_demonstration_work.gif" >
</div>
<!---------------------------------------------------------------------------------->

---

<h2 align="left"> 2. Входные и выходные данные </h2>

**Входные данные** 
1.	Радиус зоны с антеннами и количество ячеек по радиусу
2. Радиус сферы на которой смотрим интенсивность и количество ячеек по радиусу

**Выходные данные** - 2d и 3d графики интенсивности проекции со сферы на плоскость

<!---------------------------------------------------------------------------------->

---

<h2 align="left"> 3. Описание логической структуры - Алгоритм программы </h2>

1. Ввод параметров поля с кнопками
2. Генерация поля
3. [Перевод индексов нажатых кнопок в координаты](https://github.com/SkorEgor/Antenna_Directivity_version2/blob/45ff1a4aace8682dbb988b6af9fea11546140977/data_and_processing.py#L67C1-L67C1) 
```C
self.antenna_x[index_for_record] = (-self.cells_radius + column) * self.radius_step
self.antenna_y[index_for_record] = (self.cells_radius - row) * self.radius_step
```
4. [Считаем радиусы от антенны до точки сферы](https://github.com/SkorEgor/Antenna_Directivity_version2/blob/45ff1a4aace8682dbb988b6af9fea11546140977/data_and_processing.py#L125)
```C
source_radius = np.sqrt((x - antenna_field.antenna_x) ** 2 +
                        (y - antenna_field.antenna_y) ** 2 +
```
* [Где координата z](https://github.com/SkorEgor/Antenna_Directivity_version2/blob/45ff1a4aace8682dbb988b6af9fea11546140977/data_and_processing.py#L122C17-L122C73)
```C
z = math.sqrt(self.radius * self.radius - x * x - y * y)
```
5. [Считаем сумму интенсивностей от каждой антенны для конкретной точки и записываем модуль](https://github.com/SkorEgor/Antenna_Directivity_version2/blob/45ff1a4aace8682dbb988b6af9fea11546140977/data_and_processing.py#L130)
```C
intensity = 0
for radius_i in source_radius:
    intensity += (1 / radius_i) * cmath.exp(complex(0.0, 1.0) * self.k * radius_i)

self.field[row][column] = abs(intensity)
```
6. Выводим результат


<!---------------------------------------------------------------------------------->

---

<h2 align="left"> 4. Структура программы - Классы и их описание </h2>

1. main.py - Запускает окно программы класса GuiProgram
2. gui_logic - class GuiProgram(Ui_Dialog) - контроллер интерфейса - обрабатывает нажатия и ошибки, вызывает функции обработки
   1. Содержит объект интерфейса, наследник Ui_Dialog
   2. Содержит два объекта графики Graph и поля кнопок
   3. Содержит объекты данных и их обработки из data_and_processing.py -> ButtonField и IntensityField
3. gui.ui -> gui.py - class Ui_Dialog(object) - класс диалога и объектов на нем. Автоматически сгенерирован Qt Designer
4. graph.py - class Graph - На объектах ui (widget и его layout) создает объекты matplotlib (axis, figure, canvas, toolbar) для отображения данных через методы класса  Drawer
5. drawer.py - class Drawer - На объектах Graph, строит графики через статичные методы. Имея метода - определяет вид графика; Переданный объект Graph - место отрисовки; Переданный объект DataAndProcessing - данные для отрисовки; 
6. data_and_processing.py -> Field, ButtonField и IntensityField.
   1. Класс Field является базовым для классов полей, создает поле заданного размера и хранит его границы
   2. ButtonField позволяет получить координаты ячеек со значением True
   3. IntensityField позволяет рассчитать интенсивности, на основе переданных координат поля ButtonField