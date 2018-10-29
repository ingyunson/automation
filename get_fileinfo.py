import os
import openpyxl


def search(dirname):
    filenames = os.listdir(dirname)
    filelist = []
    for filename in filenames:
        ext = os.path.splitext(filename)[-1]
        if ext == '.xlsx':
            filelist.append(filename)
    return filelist


def get_file(stock_code):
    file_list = search(r"c:\Users\Seimei\Jupyter")
    for s in file_list:
        if stock_code in s:
            return (s)


def open_file(stock_code):
    filename = get_file(stock_code)
    book = openpyxl.load_workbook(filename)
    sheet = book.worksheets[1]
    data = []
    data2 = []
    for row in sheet.rows:
        data.append([row[0].value, row[200].value])  # GS
        # data2.append([row[0].value, row[188].value]) #GG / 자본총계
    del data[0:3]

    for i in range(len(data)):
        if data[i][0]:
            years = data[i][0].year
            data[i][0] = years
        else:
            pass
    print(data)
    # print(data2)


open_file('267290')




