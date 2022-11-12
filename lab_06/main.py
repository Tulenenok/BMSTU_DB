import psycopg2

from tools import (
    bcolors,
    is_int
)
from tasks import LIST_TASKS


def menu():
    print(f"{bcolors.HEADER}Меню{bcolors.ENDC}\n"
          f"  {bcolors.HEADER}0.{bcolors.ENDC} Выход\n"
          f"  {bcolors.HEADER}1.{bcolors.ENDC} Выполнить скалярный запрос\n" 
          f"  {bcolors.HEADER}2.{bcolors.ENDC} Выполнить запрос с несколькими соединениями(JOIN)\n"
          f"  {bcolors.HEADER}3.{bcolors.ENDC} Выполнить запрос с ОТВ(CTE) и оконными функциями\n"
          f"  {bcolors.HEADER}4.{bcolors.ENDC} Выполнить запрос к метаданным\n"
          f"  {bcolors.HEADER}5.{bcolors.ENDC} Вызвать скалярную функцию(написанную в третьей лабораторной работе)\n"
          f"  {bcolors.HEADER}6.{bcolors.ENDC} Вызвать многооператорную или табличную функцию(написанную в третьей лабораторной работе)\n"
          f"  {bcolors.HEADER}7.{bcolors.ENDC} Вызвать хранимую процедуру(написанную в третьей лабораторной работе)\n"
          f"  {bcolors.HEADER}8.{bcolors.ENDC} Вызвать системную функцию или процедуру\n"
          f"  {bcolors.HEADER}9.{bcolors.ENDC} Создать таблицу в базе данных, соответствующую тематике БД\n"
          f"  {bcolors.HEADER}10.{bcolors.ENDC} Выполнить вставку данных в созданную таблицу с использованием инструкции INSERT или COPY\n")

    while True:
        command = input(f'{bcolors.HEADER}Введите номер команды:{bcolors.ENDC} ')

        if is_int(command) and 0 <= int(command) <= 10:
            return int(command)

        print('Неверный номер команды')


def open_db(db="lab_1", usr="", password="", host="127.0.0.1", port="5432"):
    try:
        connect = psycopg2 \
            .connect(
                database=db,
                user=usr,
                password=password,
                host=host,
                port=port
            )
    except:
        print(f"Подключение к БД --> {bcolors.FAIL}FAILURE{bcolors.ENDC}\n")
        return -1, -1

    print(f"Подключение к БД --> {bcolors.OKGREEN}SUCCESS{bcolors.ENDC}\n")
    return connect, connect.cursor()


def close_db(connect, cursor):
    cursor.close()
    connect.close()

    print(f"\nПодключение к БД закрыто --> {bcolors.OKGREEN}SUCCESS{bcolors.ENDC}\n")


def main():
    connect, cursor = open_db()
    if connect == -1:
        exit()

    command = menu()
    while command != 0:
        LIST_TASKS[command - 1](cursor, connect)

        command = menu()

    close_db(connect, cursor)


if __name__ == "__main__":
    main()
