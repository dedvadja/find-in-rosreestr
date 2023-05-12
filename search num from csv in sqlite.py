import csv
import sqlite3

def get_rosreestr_info(id):
    try:
        sqlite_connection = sqlite3.connect('db/test csv to sqlite.db')
        cursor = sqlite_connection.cursor()

        sql_select_query = """select * from rosreestrDb where numFrom <= ? and numTo >= ?"""
        cursor.execute(sql_select_query, (id, id,))
        records = cursor.fetchall()
        if records:
            for row in records:
                print(f'Номер {id} принадлежит {row[3]}')
        else:
            print(f'Номер {id} не найден')

        cursor.close()
    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()

dannye=csv.reader(open('csv/dannyeHR.csv'), delimiter=';') #read data from csv
next(dannye, None) #skip header

for row_d in dannye:
    get_rosreestr_info(row_d[0])