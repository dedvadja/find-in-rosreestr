import sqlite3
import pandas
import win32com.client as win32
import os

global fileToAnalyze
fileRezultat = 'C:/Users/samylovskiy-vs/PycharmProjects/csv to sqlite/csv/rezultat.csv'
outputDir = r"C:\Users\samylovskiy-vs\Downloads"


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


def find_data(fileA, fileR):
    dannye = pandas.read_csv(fileA, delimiter=';', encoding='windows-1251', usecols=[0], index_col=0)
    with open(fileR, mode='w') as w_file:
        for rowD in dannye.index:
            str = get_rosreestr_info(rowD)
            w_file.writelines("%s;" % line for line in str)
            w_file.write('\n')


def send_email(file):
    outlook = win32.Dispatch('outlook.application')
    mail = outlook.CreateItem(0)
    mail.Subject = 'RE: Rosreestr'
    mail.To = 'samylovskiy.v.s@mail.ca.sbrf.ru'
    mail.HTMLBody = r"""
    Дорогой Вадим,<br><br>
    С величайшей радостью отправляю тебе плод моей кропотливой работы.<br><br>
    С наилучшими пожеланиями,<br>
    Вадим
    """
    mail.Attachments.Add(file)
    mail.Send()


def save_attachments():
    outlook = win32.Dispatch('outlook.application')
    mapi = outlook.GetNamespace('MAPI')
    inbox = mapi.GetDefaultFolder(6)  # первая папка по умолчанию папка входящих писем
    mess = inbox.Items
    mess = mess.Restrict("[Subject] = 'Rosreestr'")
    mess = mess.Restrict('[UnRead] = True')
    return mess


def main():
    messages = save_attachments()
    if len(messages) != 0:
        for message in list(messages):
            for attachment in message.Attachments:
                if attachment:
                    attachment.SaveAsFile(os.path.join(outputDir, attachment.FileName))
                    print(f"Вложене {attachment.FileName} сохранено")
                    fileToAnalyze = 'C:/Users/samylovskiy-vs/Downloads/' + attachment.FileName
                    find_data(fileToAnalyze, fileRezultat)
                    send_email(fileRezultat)
                    print('Письмо отправлено')
                else:
                    print('Вложений не обнаружено')
    else:
        print('Непрочитанных писем не обнаружено')


if __name__ == '__main__':
    main()
