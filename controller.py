import eel
from calculator import *
import os


@eel.expose
def collect_data(array):
    print(array)
    calc = Calculator()
    res = calc.solve(array)
    print_solution(solution=res)
    return array


def start_programm():
    eel.init('web')
    eel.start('index.html')


def template_begin(root):
    path = root + '/template_begin.txt'
    beggining = open(path, 'r', encoding="utf-8")
    b = []
    e = []
    for line in beggining:
        b.append(line)
    beggining.close()
    path = root + '/template_end.txt'
    ending = open(path, 'r', encoding="utf-8")
    for line in ending:
        e.append(line)
    ending.close()
    return b, e


def print_table(rows, f):
    # open("output.html", 'w')
    table_begin = '<table>'
    table_end = '</table>'
    table = ''
    table += table_begin
    for index_y, row in enumerate(rows):
        table += '<tr>'

        for index_x, value in enumerate(row):
            table += f'<td> {value} </td>'

        table += '</tr>'

    table += table_end
    f.write(table)
    # f.close()


# def begin_doc(rows):
#     b, e = template_begin()
#     for line in b:
#         f.write(line)
#     print_table(rows)
#     for line in e:
#         f.write(line)
#     # f.close()


def open_solution(root):
    path = root + "\web\\" + "solution.html"
    f = open(path, 'w', encoding="utf-8")
    return f


def close_solution(root, f):
    path = root + "\web\\" + "solution.html"
    f.close()


def print_solution(solution):
    root = os.getcwd()
    beg, end = template_begin(root=root)

    f = open_solution(root=root)
    for line in beg:
        f.write(line)
    # beginnig_data(f=f, solution=solution)
    for index in range(len(solution)):
        if index == 0:
            beginnig_data(f=f, solution=solution)
            continue
        if index == len(solution) - 1:
            print_sum(solution=solution, f=f)
            continue
        print_highlitedTable(rows=solution[index]["tax"], f=f, circles=solution[index]["circles"])
        print_temp(f=f, solution=solution, index=index)
    close_solution(root=root, f=f)


def mid_iterations(solutoin, index, f):
    pass

def print_highlitedTable(rows, f, circles):
    # open("output.html", 'w')
    highlite = []
    for row in circles:
        for index, cirlce in enumerate(row):
            if index == 0:
                continue
            highlite.append(cirlce)
    table_begin = '<table>'
    table_end = '</table>'
    table = ''
    table += table_begin
    for index_y, row in enumerate(rows):
        table += '<tr>'

        for index_x, value in enumerate(row):
            if (index_y, index_x) in highlite:
                table += f'<td bgcolor= "#fc0"> {value} </td>'
                continue
            table += f'<td> {value} </td>'

        table += '</tr>'

    table += table_end
    f.write("<h1 align=\"center\">В каждом из столбцов таблицы находим минимальные тарифы (они выделены)</h1>")
    f.write(table)

def print_temp(f, solution, index):
    data = solution[index]
    table = []
    table.append(['-'])
    for index_y in range(len(data["temp"])):
        table.append([])
        table[index_y + 1].append(f'A{index_y + 1}')
    for index_x in range(len(data["temp"][0])):
        table[0].append(f'B{index_x + 1}')
    table[0].append("Запасы")
    table.append([])
    table[-1].append("Потребности")
    for index, value in enumerate(data["temp"]):
        table[index + 1] += value
        table[index + 1] += [data["surpluss"][index]]
    table[-1] += data["needs"]
    table.append([])
    table[-1].append("Разницы")
    table[-1] += data["mindiff"]
    f.write("<h1 align=\"center\">Заполняем клетки, в которых стоят указанные числа. Для этого находим столбцы (строки), в которых имеется лишь одна клетка для заполнения. Определив и заполнив некоторую клетку, исключаем из рассмотрения соответствующий столбец (строку) и переходим к заполнению следующей клетки.</h1>")
    f.write("<h1 align=\"center\">После получения условно-оптимального плана определяем избыточные и недостаточные строки.  </h1>")
    f.write(
        "<h1 align=\"center\">После определения избыточных и недостаточных строк по каждому из столбцов находим разности между минимальными тарифами, записанными в избыточных строках, и тарифами, стоящими в заполненных клетках.  </h1>")

    print_table(rows=table, f=f)
    diff = data["diff"]
    f.write(
        f"<h1 align=\"center\">Выбираем наименьшую из найденных разностей, которая является промежуточной рентой. В данном случае промежуточная рента равна {diff} . После этого прибавляем ее к каждрой отрицательной строке</h1>")


def beginnig_data(f, solution):
    data = solution[0]
    table = []
    table.append(['-'])
    for index_y in range(len(data["tax"])):
        table.append([])
        table[index_y + 1].append(f'A{index_y + 1}')
    for index_x in range(len(data["tax"][0])):
        table[0].append(f'B{index_x + 1}')
    table[0].append("Запасы")
    table.append([])
    table[-1].append("Потребности")
    for index, value in enumerate(data["tax"]):
        table[index + 1] += value
        table[index + 1] += [data["goods"][index]]
    table[-1] += data["needs"]
    f.write("<h1 align=\"center\">Занесем исходные данные в распределительную таблицу.</h1>")
    print_table(table, f)


def print_sum(solution, f):
    data = solution[-1]
    number = len(data["temp"]) + len(data["temp"][0]) - 1
    f.write(f"<h1 align=\"center\">В результате все имеющиеся запасы поставщиков распределяются в соответствии с фактическими потребностями пунктов назначения. Число заполненных клеток равно {number}, и все они имеют наименьший показатель cij. Следовательно, получен оптимальный план исходной транспортной задачи:</h1>")
    print_table(rows=data["tax"], f=f)
    print_table(rows=data["temp"], f=f)
    sum_string = ''
    res = None
    for index, data1 in enumerate(data["sum"]):
        if index + 1 == len(data["sum"]):
            res = data["sum"][-1]
            continue
        if index == len(data["sum"]) - 2:
            sum_string += f"{data1[0]} * {data1[1]}"
            continue
        sum_string += f"{data1[0]} * {data1[1]} + "

    f.write(f"<h1 align=\"center\">При этом плане перевозок общие затраты таковы: F(x) ={sum_string} = {res}</h1>")


test_data = [[7, 12, 4, 8, 5, 180],
             [1, 8, 6, 5, 3, 350],
             [6, 13, 8, 7, 4, 20],
             [110, 90, 120, 80, 150, '']
             ]

# root = os.getcwd()
# print(root)
# f = open_solution()
# begin_doc(test_data)
# close_solution()
calc = Calculator()
sol = calc.solve(test_data)
print_solution(sol)

# start_programm()
