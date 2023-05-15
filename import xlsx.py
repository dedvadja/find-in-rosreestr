import os
import sqlite3
import pandas
import win32com.client as win32

fileRezultat = r'C:\Users\samylovskiy-vs\PycharmProjects\csv to sqlite\Rezultat\rezultat.xlsx'
outputDir = r'C:\Users\samylovskiy-vs\Downloads'


def get_rosreestr_info(id):
    try:
        sqlite_connection = sqlite3.connect('db/test csv to sqlite.db')
        cursor = sqlite_connection.cursor()
        sql_select_query = """select * from rosreestrDb where numFrom <= ? and numTo >= ?"""
        cursor.execute(sql_select_query, (id, id,))
        records = cursor.fetchall()
        if records:
            for row in records:
                operator = row[3]
        else:
            operator = 'не обнаружен'
        cursor.close()
    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)
    finally:
        return operator
        if sqlite_connection:
            sqlite_connection.close()


def get_email():
    outlook = win32.Dispatch('outlook.application')
    mapi = outlook.GetNamespace('MAPI')
    inbox = mapi.GetDefaultFolder(6)  # первая папка по умолчанию папка входящих писем
    email = inbox.Items
    email = email.Restrict("[Subject] = 'Rosreestr'")
    email = email.Restrict('[UnRead] = True')
    return email


def send_email(file):
    outlook = win32.Dispatch('outlook.application')
    mail = outlook.CreateItem(0)
    mail.Subject = 'RE: Rosreestr'
    mail.To = 'samylovskiy.v.s@mail.ca.sbrf.ru'
    # mail.To = 'samylovskiy-vs@sberbank.ru'
    mail.HTMLBody = r"""
    Дорогой Вадим,<br><br>
    С величайшей радостью отправляю тебе плод моей кропотливой работы.<br><br>
    С наилучшими пожеланиями,<br>
    Вадим
    """
    mail.Attachments.Add(file)
    mail.Send()


def find_data(fileA, fileR):
    print('Анализ данных запущен')
    dannye = pandas.read_excel(fileA)
    dannye['Operator'] = [get_rosreestr_info(numTel) for numTel in dannye['Номер телефона']]
    dannye.to_excel(fileR, index=False)


def main():
    messages = get_email()
    if len(messages) != 0:
        print('Обнаружено непрочитанное письмо с темой Rosreestr')
        for message in list(messages):
            for attachment in message.Attachments:
                if attachment:
                    attachment.SaveAsFile(os.path.join(outputDir, attachment.FileName))
                    print(f"Вложене {attachment.FileName} сохранено")
                    fileToAnalyze = f'{outputDir}\{attachment.FileName}'
                    find_data(fileToAnalyze, fileRezultat)
                    send_email(fileRezultat)
                    print('Письмо отправлено')
                else:
                    print('Вложений не обнаружено')
    else:
        print('Новых писем не обнаружено')


if __name__ == '__main__':
    main()
