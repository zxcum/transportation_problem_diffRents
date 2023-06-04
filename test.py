import os

def template_begin():
    path = root + '/template_begin.txt'
    beggining = open(path, 'r')
    b = []
    e = []
    for line in beggining:
        b.append(line)
    beggining.close()
    path = root + '/template_end.txt'
    ending = open(path, 'r')
    for line in ending:
        e.append(line)
    ending.close()
    return b, e


def print_table(rows):
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


def begin_doc(rows):
    b, e = template_begin()
    for line in b:
        f.write(line)
    print_table(rows)
    for line in e:
        f.write(line)
    f.close

def open_solution():
    path = root +"\web\\" + "solution2.html"
    f = open(path, 'w')
    return f

def close_solution():
    path = root +"\web\\" + "solution2.html"
    f.close

test_data = [[7, 12, 4, 8, 5, 180],
             [1, 8, 6, 5, 3, 350],
             [6, 13, 8, 7, 4, 20],
             [110, 90, 120, 80, 150]
             ]

root = os.getcwd()
print(root)
f = open_solution()
begin_doc(test_data)
close_solution()





