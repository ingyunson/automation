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
    sheet = book.worksheets[0]
    data = []
    for row in sheet.rows:
        data.append([row[0].value, row[9].value])
    print(data)


open_file('267290')