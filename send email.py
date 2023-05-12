import sqlite3
import pandas
import win32com.client as win32
from datetime import datetime

def send_email(f):
    outlook = win32.Dispatch('outlook.application')
    mail = outlook.CreateItem(0)
    mail.Subject = 'Проверка номеров в росреестре ' + datetime.now().strftime('%#d %b %Y %H:%M')
    mail.To = "samylovskiy-vs@sberbank.ru"
    mail.HTMLBody = r"""
    Дорогой Вадим,<br><br>
    С величайшей радостью отправляю тебе плод моей кропотливой работы.<br><br>
    С наилучшими пожеланиями,<br>
    Вадим
    """
    mail.Attachments.Add(f)
    mail.Send()

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

fileRezultat = 'C:/Users/samylovskiy-vs/PycharmProjects/csv to sqlite/csv/rezultat.csv'
dannye = pandas.read_csv('csv/dannyeHR.csv', delimiter=';', encoding='windows-1251', usecols=[0], index_col='number')
with open(fileRezultat, mode='w') as w_file:
    for rowD in dannye.index:
        str = get_rosreestr_info(rowD)
        w_file.writelines("%s;" % line for line in str)
        w_file.write('\n')
send_email(fileRezultat)