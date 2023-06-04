from abc import abstractmethod
import numpy as np
from math import *


class Calculator:
    def __init__(self):
        """инициализация основных массивов"""

        self.tax_array = []         # массив тарифов на перевозку
        self.needs_array = []       # строка потребностей пунктов
        self.goods_array = []       # столбец наличия товара
        self.temp_array = []        # изменяемая таблица промежуточных итогов


        self.surpluss_array = []        # столбец переизбытка/недостатка товара для обеспечения потребностей
        self.circles_array = []         # массив для отмечения изменяемых клеток в матрице
        self.min_array = []             # трансонированный массив для поиска минимумов и разных проверок
        self.mindiff_array = []         # строка минимальных разностей
        self.mindiff_array_temp = []    # транспонированный массив для определения необходимости перестановок
        self.booleam_array = []         # строка, чтобы понять нужно ли искать минимальную разницу

    def calculate_shortage(self):
        """вычислить избыток или недостаток по строке относительно запасов поставщика"""

        self.surpluss_array = []

        for index, row in enumerate(self.temp_array):
            sum_of_list = sum(row)
            difference = self.goods_array[index] - sum_of_list
            self.surpluss_array.append(difference)

        # print(self.surpluss_array)


    def add_minDif(self, dif):
        pass



    def calculate_minDif(self):
        """вычисление минимальных разностей тарифов"""

        # print(self.min_array)
        for index_x, row in enumerate(self.min_array):

            index_min_1 = (self.circles_array[index_x][0], self.circles_array[index_x][1])
            mimimum_1 = self.tax_array[self.circles_array[index_x][0]][self.circles_array[index_x][1]]

            index_min_2 = None
            mimimum_2 = np.inf

            for index_y, value in enumerate(row):
                # print(self.temp_array[index_y][index_x])
                if index_min_1 == (index_y, index_x):
                    continue
                # print(index_min_1, (index_y, index_x), "indexes", index_min_1 == (index_y, index_x))

                if (mimimum_2 >= value) and (value > 0) and (not None) and (self.temp_array[index_y][index_x] == 0) and (self.surpluss_array[index_y] > 0):
                    mimimum_2 = value
                    # print(index_min_1, (index_y, index_x), "indexes", index_min_1 == (index_y, index_x))

                    index_min_2 = index_y


            if mimimum_2 == np.inf:
                self.mindiff_array[index_x] = None
            else:
                difference = mimimum_2 - mimimum_1

                self.mindiff_array[index_x] = [difference, index_min_1, (index_min_2, index_x)]

        self.need_toMinDIf()


    def need_toMinDIf(self):
        """определяет нужно ли искать минимальную разницу"""

        self.mindiff_array_temp = self.transpose_matrix(self.temp_array)
        for index_x, column in enumerate(self.mindiff_array_temp):

            if self.booleam_array[index_x] is None:
                continue

            indicator = True

            for index_y, value in enumerate(column):

                if value is None:
                    continue

                if value > 0 and self.surpluss_array[index_y] < 0:
                    indicator = False

            if indicator:
                self.booleam_array[index_x] = None

        for index in range(len(self.booleam_array)):

            if self.booleam_array[index] is None or self.mindiff_array[index] is None:

                self.booleam_array[index] = None
                self.mindiff_array[index] = None

        # print(self.booleam_array)


    def loop_checker(self):
        indicator = True
        for value in self.surpluss_array:
            if value < 0:
                indicator = False
        return indicator


    @abstractmethod
    def results_finding(self):
        """нахождение финальных матриц и результата с записью шагов"""

        results = []
        for i in range(30):


            self.calculate_shortage()
            self.calculate_minDif()
            self.print_anyArray(calc.temp_array)
            # print(self.booleam_array)
            print(self.mindiff_array)
            print()
            results.append([self.temp_array.copy(), self.mindiff_array, self.surpluss_array])
            if self.loop_checker():
                break

            min_dif = np.inf
            min_index = None
            min_data = None
            for index, value in enumerate(self.mindiff_array):
                if value is None:
                    continue
                if value[0] < min_dif:
                    min_index = index
                    min_dif = value[0]

                    min_data = value
                    # print(min_data, value[0], min_dif, "-----------")

            if abs(self.surpluss_array[min_data[1][0]]) >= abs(self.temp_array[min_data[1][0]][min_data[1][1]]):
                diff = min(abs(self.surpluss_array[min_data[2][0]]), abs(self.temp_array[min_data[1][0]][min_data[1][1]]))
                self.temp_array[min_data[2][0]][min_data[2][1]] += diff
                self.temp_array[min_data[1][0]][min_data[1][1]] -= diff
            else:
                diff = min(abs(self.surpluss_array[min_data[2][0]]), abs(self.surpluss_array[min_data[1][0]]))
                self.temp_array[min_data[2][0]][min_data[2][1]] += diff
                self.temp_array[min_data[1][0]][min_data[1][1]] -= diff

            # if self.temp_array[min_data[1][0]][min_data[1][1]] > self.surpluss_array[min_data[2][0]]:
            #
            #     self.temp_array[min_data[1][0]][min_data[1][1]] -= self.surpluss_array[min_data[2][0]]
            #     self.temp_array[min_data[2][0]][min_data[2][1]] += self.surpluss_array[min_data[2][0]]
            #
            # else:
            #
            #     self.temp_array[min_data[2][0]][min_data[2][1]] = self.temp_array[min_data[1][0]][min_data[1][1]]
            #     self.temp_array[min_data[1][0]][min_data[1][1]] = 0

        return results





    def find_mins(self):
        """одноразовый поиск минимумов относительно столбцов для изначального заполнения"""
        transposed = self.transpose_matrix(self.tax_array)
        for index, row in enumerate(transposed):

            mimimum = np.inf

            for value in row:
                if mimimum > value > 0 and not None:
                    mimimum = value

            if mimimum != np.inf:
                index_min = row.index(mimimum)
                self.circles_array.append((index_min, index))

        # print(self.circles_array)


    def fill_allNeeds(self):
        """заполнение промежуточного массива максимумом всего по минимальной цене"""
        for item in self.circles_array:
            self.temp_array[item[0]][item[1]] = self.needs_array[item[1]]

        self.mindiff_array_temp = self.transpose_matrix(self.temp_array)
        # print(self.temp_array)


    @abstractmethod
    def add_listToArray(self):
        """используемый метод"""
        self.tax_array.append([])   # добавить строку в масив
        self.temp_array.append([])  # добавить строку в масив

    @abstractmethod
    def transpose_matrix(self, array):
        """транспонирование матрицы"""

        temp_array = []
        length_y = len(array)
        length_x = len(array[0])
        for index_y in range(0, length_x):
            temp_array.append([])

            for index_x in range(0, length_y):
                temp_array[index_y].append(array[index_x][index_y])

        return temp_array



    @abstractmethod
    def create_arrays(self, rows):
        """создать массивы необходимой формы и конструкции"""
        for index, row in enumerate(rows):
            if index == len(rows) - 1:

                for value in row:
                    if value < 1:
                        value = None
                    self.needs_array.append(value)

                    self.mindiff_array.append(0)
                    self.booleam_array.append(0)
                continue

            self.add_listToArray()

            for last, value in enumerate(row):

                if last == len(row) - 1:
                    if value < 1:
                        value = None
                    self.goods_array.append(value)

                    continue

                if value < 1:
                    value = None

                self.tax_array[index].append(value)
                self.temp_array[index].append(0)

        self.min_array = self.transpose_matrix(self.tax_array)


    @abstractmethod
    def print_arrays(self):
        """вывод массивов в читаемой форме"""

        for i in range(len(self.tax_array)):
            print(self.tax_array[i], self.goods_array[i])
        print(self.needs_array)

    @abstractmethod
    def print_anyArray(self, rows):
        """вывод любого массива"""

        for index, row in enumerate(rows):
            print(row, self.surpluss_array[index])

    @abstractmethod
    def count_sum(self):
        """посчитать сумму"""
        result = []
        summ = 0
        for index_x, value in enumerate(self.temp_array):
            for index_y, value in enumerate(value):
                if value == 0:
                    continue
                summ += value * self.tax_array[index_x][index_y]
                result.append((value, self.tax_array[index_x][index_y]))
        result.append(summ)
        return result


    def initialise_calc(self, rows):
        """основная функция инициализаци"""

        self.create_arrays(rows=rows)
        self.print_arrays()
        self.find_mins()
        self.fill_allNeeds()
        result = self.results_finding()
        summ = self.count_sum()
        print(summ)
        return result, summ

# test_data = [[7, 12, 4, 8, 5, 180],
#              [1, 8, 6, 5, 3, 350],
#              [6, 13, 8, 7, 4, 20],
#              [110, 90, 120, 80, 150, 550]
#              ]
test_data = [[7, 12, 4, 8, 5, 180],
             [1, 8, 6, 5, 3, 350],
             [6, 13, 8, 7, 4, 20],
             [110, 90, 120, 80, 150]
             ]
test_data2 = [[1,	6,	7,	12,	90],
[5,	2,	3,	8,	100],
[9,	10,	11,	4,	310],
[100,	150,	160,	90],
              ]
test_data3 = [[23,	12,	56,	12,	90],
             [32,	43,	54,	23,	150],
             [43,	21,	23,	12,	120],
             [23,	76,	24,	57,	300],
              [100,	200,50,	300]
             ]
calc = Calculator()
# print(test_data)
# calc.create_arrays(rows=test_data)
# calc.print_arrays()
# calc.find_mins()
# calc.fill_allNeeds()
# calc.print_anyArray(calc.temp_array)
# calc.calculate_shortage()
# calc.calculate_minDif()
# # print(calc.mindiff_array)
# # calc.need_toMinDIf()
# calc.results_finding()
calc.initialise_calc(test_data3)