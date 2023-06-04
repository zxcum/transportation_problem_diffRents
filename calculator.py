import copy
from abc import abstractmethod
import numpy as np
from math import *


class Calculator:
    def __init__(self):
        """инициализация основных массивов"""

        self.tax_array = []  # изначальный массив тарифов на перевозку
        self.tax_temp_array = []  # изменяемый массив тарифов на перевозку
        self.needs_array = []  # строка потребностей пунктов
        self.goods_array = []  # столбец наличия товара
        self.temp_array = []  # изменяемая таблица промежуточных итогов распределения
        self.goods_temp_array = [] # для посчета того, сколько удоволетворено
        self.saved_taxes = []
        self.solution = []

        self.surpluss_array = []  # столбец переизбытка/недостатка товара для обеспечения потребностей
        self.circles_array = []  # массив для отмечения изменяемых клеток в матрице
        self.min_array = []  # трансонированный массив для поиска минимумов и разных проверок
        self.mindiff_array = []  # строка минимальных разностей
        self.mindiff_array_temp = []  # транспонированный массив для определения необходимости перестановок
        self.booleam_array = []  # строка, чтобы понять нужно ли искать минимальную разницу

    # в этом куске кода реализуется организация данных для дальнейшей работы

    @abstractmethod
    def add_listToArray(self):
        """используемый метод"""
        self.tax_array.append([])  # добавить строку в масив
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

                for index_x, value1 in enumerate(row):
                    if index_x + 1 == len(row):
                        continue
                    value = int(value1)
                    if value < 1:
                        value = None
                    self.needs_array.append(value)

                    self.mindiff_array.append(0)
                    self.booleam_array.append(0)
                continue

            self.add_listToArray()

            for last, value1 in enumerate(row):
                value = int(value1)
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
        self.tax_temp_array = self.tax_array.copy()
        self.save_taxes(rows)
        self.goods_temp_array = self.goods_array.copy()
        self.print_arrays()
        # self.solution.append([self.tax_array, self.goods_array, self.needs_array])
        self.solution.append({
            "tax": copy.deepcopy(self.tax_array),
            "goods": copy.deepcopy(self.goods_array),
            "needs": copy.deepcopy(self.needs_array)
        })

    def save_taxes(self, rows):
        for index, line in enumerate(rows):
            self.saved_taxes.append([])
            for value in line:
                if value != '':
                    self.saved_taxes[index].append(int(value))
                else:
                    self.saved_taxes[index].append(value)


    # первая итерация для нахождения изначальных условий

    def find_mins(self):
        """поиск минимумов относительно столбцов для изначального заполнения"""

        transposed = self.transpose_matrix(self.tax_array)
        for index, row in enumerate(transposed):

            mimimum = np.inf

            for value in row:
                if mimimum > value > 0 and not None:
                    mimimum = value

            if mimimum != np.inf:
                index_min = row.index(mimimum)
                self.circles_array.append([mimimum, (index_min, index)])

    def fill_allNeeds(self):
        """заполнение промежуточного массива максимумом всего по минимальной цене"""
        temp_goods = self.goods_array.copy()

        for list in self.circles_array:
            item = list[1]
            self.temp_array[item[0]][item[1]] = min(self.needs_array[item[1]], temp_goods[item[0]])

            temp_goods[item[0]] -= min(self.needs_array[item[1]], temp_goods[item[0]])

        # self.mindiff_array_temp = self.transpose_matrix(self.temp_array)

    # выполнение подсчета избытков или недостатков в использовании ресурсов

    def calculate_shortage(self):
        """вычислить избыток или недостаток по строке относительно запасов поставщика"""

        self.surpluss_array = []

        for index, row in enumerate(self.temp_array):
            sum_of_list = sum(row)
            difference = self.goods_array[index] - sum_of_list

            if difference == 0:
                temp_array = self.transpose_matrix(self.temp_array)
                for index_temp, row in enumerate(temp_array):
                    if sum(row) != self.needs_array[index_temp]:
                        difference = str('-' + str(difference))
                        break

            self.surpluss_array.append(difference)

    # вычисление минимумальных разностей и минимумов

    # def calculate_minDif(self):
    #     """вычисление минимальных разностей тарифов"""
    #
    #     # print(self.min_array)
    #     for index_x, row in enumerate(self.min_array):
    #
    #         index_min_1 = (self.circles_array[index_x][0], self.circles_array[index_x][1])
    #         mimimum_1 = self.tax_array[self.circles_array[index_x][0]][self.circles_array[index_x][1]]
    #
    #         index_min_2 = None
    #         mimimum_2 = np.inf
    #
    #         for index_y, value in enumerate(row):
    #             # print(self.temp_array[index_y][index_x])
    #             if index_min_1 == (index_y, index_x):
    #                 continue
    #             # print(index_min_1, (index_y, index_x), "indexes", index_min_1 == (index_y, index_x))
    #
    #             if (mimimum_2 >= value) and (value > 0) and (not None) and (
    #                     self.temp_array[index_y][index_x] == 0) and (self.surpluss_array[index_y] > 0):
    #                 mimimum_2 = value
    #                 # print(index_min_1, (index_y, index_x), "indexes", index_min_1 == (index_y, index_x))
    #
    #                 index_min_2 = index_y
    #
    #         if mimimum_2 == np.inf:
    #             self.mindiff_array[index_x] = None
    #         else:
    #             difference = mimimum_2 - mimimum_1
    #
    #             self.mindiff_array[index_x] = [difference, index_min_1, (index_min_2, index_x)]

    def calculate_minDif(self):
        """посчитать минимальные разницы для каждого слобца"""

        temp_diff = self.transpose_matrix(self.tax_temp_array)
        self.mindiff_array = []
        for index, row in enumerate(temp_diff):
            minimum = self.circles_array[index][0]
            min_diff = np.inf
            for index_y, value in enumerate(row):
                if str(self.surpluss_array[index_y])[0] == '-':
                    continue
                # print(value, minimum)
                diff = value - minimum

                if min_diff >= diff > 0:
                    min_diff = diff

            if min_diff == np.inf:
                self.mindiff_array.append(None)
            else:
                self.mindiff_array.append(min_diff)


    def find_circles(self):
        """поиск минимумов относительно столбцов"""

        transposed = self.transpose_matrix(self.tax_temp_array)
        self.circles_array = []
        for index_x, row in enumerate(transposed):

            mins = []
            mimimum = np.inf

            for index_y, value in enumerate(row):
                if mimimum > value > 0 and not None:
                    mins = []
                    mimimum = value
                    mins.append(mimimum)
                    mins.append((index_y, index_x))
                    continue
                if value == mimimum:
                    mins.append((index_y, index_x))

            if mins != []:
                self.circles_array.append(mins)


    def add_minDif(self):
        """добавить минималькую разницу к тарифам"""
        diff = np.inf

        for value in self.mindiff_array:
            if value is None:
                continue
            if(diff > value > 0):
                diff = value
        # print(self.mindiff_array)
        # print(diff, "diff")
        for index_y, value in enumerate(self.surpluss_array):
            if str(value)[0] == '-':
                for index_x in range(0, len(self.tax_temp_array[index_y])):
                    self.tax_temp_array[index_y][index_x] += diff
            else:
                continue

    def fill_needs(self):
        temp_goods = self.goods_array.copy()
        temp_needs = self.needs_array.copy()
        # print(temp_needs, temp_goods)
        self.empty_needs()

        first_needs = []
        second_needs = []

        # define order
        for index, item in enumerate(self.circles_array):
            if len(item) == 2:
                first_needs.append(index)
            else:
                second_needs.append(index)

        for index in first_needs:
            list = self.circles_array[index]
            for index_1, item in enumerate(list):
                # print(item)
                if index_1 == 0:
                    continue
                # if str(temp_goods)[item[0]] == '-':
                #     continue
                # self.temp_array[item[0]][item[1]] = min(temp_needs[item[1]], temp_goods[item[0]])
                # print(min(temp_needs[item[1]], temp_goods[item[0]]), "min first", temp_needs[item[1]], temp_goods[item[0]])
                # print(temp_needs[item[1]], 'before')
                # temp_goods[item[0]] -= min(temp_needs[item[1]], temp_goods[item[0]])
                #
                # temp_needs[item[1]] -= min(temp_needs[item[1]], temp_goods[item[0]])
                # print(temp_needs[item[1]], "afetr")

                mindiff = min(temp_needs[item[1]], temp_goods[item[0]])
                index_goods = item[0]
                index_needs = item[1]
                good = temp_goods[index_goods]
                need = temp_needs[index_needs]
                self.temp_array[index_goods][index_needs] = mindiff
                temp_goods[index_goods] = good - mindiff
                temp_needs[index_needs] = need - mindiff

            # print()
        # print(temp_needs, temp_goods)
        for index in second_needs:
            list = self.circles_array[index]
            for index_1, item in enumerate(list):
                # print(item)
                if index_1 == 0:
                    continue


                # self.temp_array[item[0]][item[1]] = min(temp_needs[item[1]], temp_goods[item[0]])
                # print(min(temp_needs[item[1]], temp_goods[item[0]]), "min second", temp_needs[item[1]], temp_goods[item[0]])
                # print(temp_needs[item[1]], 'before')
                # temp_goods[item[0]] = temp_goods[item[0]] - min(temp_needs[item[1]], temp_goods[item[0]])
                #
                # temp_needs[item[1]] = temp_needs[item[1]] - min(temp_needs[item[1]], temp_goods[item[0]])
                # print(temp_needs[item[1]], "afetr")

                mindiff = min(temp_needs[item[1]], temp_goods[item[0]])
                index_goods = item[0]
                index_needs = item[1]
                good = temp_goods[index_goods]
                need = temp_needs[index_needs]
                self.temp_array[index_goods][index_needs] = mindiff
                temp_goods[index_goods] = good - mindiff
                temp_needs[index_needs] = need - mindiff
            # print()
        # print(temp_needs, temp_goods)

        # for list in self.circles_array:
        #     for index, item in enumerate(list):
        #         if index == 0:
        #             continue
        #         self.temp_array[item[0]][item[1]] = min(temp_needs[item[1]], temp_goods[item[0]])
        #
        #         temp_goods[item[0]] -= min(temp_needs[item[1]], temp_goods[item[0]])
        #         temp_needs[item[1]] -= min(temp_needs[item[1]], temp_goods[item[0]])

        # self.mindiff_array_temp = self.transpose_matrix(self.temp_array)

    @abstractmethod
    def empty_needs(self):
        for index_y in range(len(self.temp_array)):
            for index_x in range(len(self.temp_array[index_y])):
                self.temp_array[index_y][index_x] = 0


    def is_optimised(self):
        for value in self.surpluss_array:
            if str(value)[0] == '-':
                return False

        return True

    def solve(self, data):
        self.create_arrays(rows=data)
        if sum(self.goods_array) < sum(self.needs_array):
            return "Невозможно найти решение, так как потребности превышают запасы!"
        self.find_circles()
        self.fill_needs()
        self.calculate_shortage()
        self.calculate_minDif()
        while 1:
            # self.print_anyArray(self.temp_array)
            # print('temp')
            # print()
            # self.print_anyArray(self.tax_temp_array)
            # print("tax")
            # print()
            # print(self.circles_array)
            diff = np.inf

            for value in self.mindiff_array:
                if value is None:
                    continue
                if (diff > value > 0):
                    diff = value
            self.solution.append({"tax": copy.deepcopy(self.tax_temp_array),
                                  "circles": copy.deepcopy(self.circles_array),
                                  "temp": copy.deepcopy(self.temp_array),
                                  "surpluss": copy.deepcopy(self.surpluss_array),
                                  "needs": copy.deepcopy(self.needs_array),
                                  "mindiff": copy.deepcopy(self.mindiff_array),
                                  "diff": diff})
            if self.is_optimised():
                break
            self.calculate_minDif()
            # print(self.mindiff_array)

            # diff = np.inf
            #
            # for value in self.mindiff_array:
            #     if value is None:
            #         continue
            #     if (diff > value > 0):
            #         diff = value

            # self.solution.append({"tax": copy.deepcopy(self.tax_temp_array),
            #                       "circles":  copy.deepcopy(self.circles_array),
            #                       "temp": copy.deepcopy(self.temp_array),
            #                       "surpluss": copy.deepcopy(self.surpluss_array),
            #                       "needs": copy.deepcopy(self.needs_array),
            #                       "mindiff": copy.deepcopy(self.mindiff_array),
            #                       "diff": diff})
            self.add_minDif()
            self.find_circles()
            self.fill_needs()
            self.calculate_shortage()
        sumall = self.count_sum()
        self.solution.append({
            "tax": self.saved_taxes,
            "temp": self.temp_array,
            "sum": sumall})
        print(self.solution)
        return self.solution


    def count_sum(self):
        """посчитать сумму"""
        result = []
        summ = 0
        # print(self.saved_taxes)
        for index_x, value in enumerate(self.temp_array):
            for index_y, value in enumerate(value):
                if value == 0:
                    continue
                summ += value * self.saved_taxes[index_x][index_y]
                result.append((value, self.saved_taxes[index_x][index_y]))
        result.append(summ)
        return result

    # вывод массивов на всякий

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
        print(self.needs_array)



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
             [23,	76,	23,	57,	300],
              [100,	200,50,	300, '']
             ]
# calc = Calculator()
# # # print(test_data)
# # calc.create_arrays(rows=test_data3)
# # calc.print_arrays()
# # calc.find_mins()
# # calc.fill_allNeeds()
# # calc.calculate_shortage()
# # print()
# # calc.print_anyArray(calc.temp_array)
# calc.solve(test_data3)
# print(calc.count_sum())
# calc.calculate_minDif()
# # print(calc.mindiff_array)
# # calc.need_toMinDIf()
# calc.results_finding()
# calc.initialise_calc(test_data3)