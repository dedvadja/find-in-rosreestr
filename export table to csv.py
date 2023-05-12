import sqlite3
import pandas

def get_rosreestr_info(id):
    global dataTable
    try:
        sqlite_connection = sqlite3.connect('db/test csv to sqlite.db')
        cursor = sqlite_connection.cursor()

        sql_select_query = """select * from rosreestrDb where numFrom <= ? and numTo >= ?"""
        cursor.execute(sql_select_query, (id, id,))
        records = cursor.fetchall()
        if records:
            for row in records:
                dataTable = [id, row[3]]
        else:
            dataTable = [id, 'не обнаружен']

        cursor.close()
    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)
    finally:
        return dataTable
        if sqlite_connection:
            sqlite_connection.close()

dannye = pandas.read_csv('csv/dannyeHR.csv', delimiter=';', encoding='windows-1251', usecols=[0], index_col='number')
with open(r'csv/rezultat.csv', mode='w') as w_file:
    for rowD in dannye.index:
        str = get_rosreestr_info(rowD)
        w_file.writelines("%s;" % line for line in str)
        w_file.write('\n')