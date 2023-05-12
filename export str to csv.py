import sqlite3
import pandas
import csv

def get_rosreestr_info(id):
    try:
        sqlite_connection = sqlite3.connect('db/test csv to sqlite.db')
        cursor = sqlite_connection.cursor()

        sql_select_query = """select * from rosreestrDb where numFrom <= ? and numTo >= ?"""
        cursor.execute(sql_select_query, (id, id,))
        records = cursor.fetchall()
        if records:
            for row in records:
                data = f'Номер {id} принадлежит {row[3]}'
                #print(data)
        else:
            data = f'Номер {id} не найден'
            #print(data)

        cursor.close()
    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)
    finally:
        return data
        if sqlite_connection:
            sqlite_connection.close()

dannye = pandas.read_csv('csv/dannyeHR.csv', delimiter=';', encoding='windows-1251', usecols=[0], index_col='number')
#print(dannye)
with open('csv/rezultat.csv', mode="w", newline='') as w_file:
    writer = csv.writer(w_file)
    for rowD in dannye.index:
        #print(rowD)
        str = get_rosreestr_info(rowD)
        writer.writerow([str])