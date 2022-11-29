from support.tools import (
    bcolors,
    is_int,
    clean_log
)
from support.support_db import (
    open_db_use_psycopg,
    close_db_use_psycopg
)
from tasks.task_01 import task_01
from tasks.task_02 import *
from tasks.task_03 import task_04


def menu():
    print(f"{bcolors.HEADER}Меню{bcolors.ENDC}\n"
          f"  {bcolors.HEADER}0.{bcolors.ENDC} Выход\n"
          f"  {bcolors.HEADER}1.{bcolors.ENDC} Задание 1 (простой запрос)\n"
          f"  {bcolors.HEADER}2.{bcolors.ENDC} Задание 2 (рег запрос на стороне бд)\n"
          f"  {bcolors.HEADER}3.{bcolors.ENDC} Задание 3 (рег запрос на стороне redis)\n"
          f"  {bcolors.HEADER}4.{bcolors.ENDC} Задание 4 (сравнительный анализ)\n"
          f"  {bcolors.HEADER}5.{bcolors.ENDC} Очистить лог файл\n")

    while True:
        command = input(f'{bcolors.HEADER}Введите номер команды:{bcolors.ENDC} ')

        if is_int(command) and 0 <= int(command) <= 5:
            return int(command)

        print('Неверный номер команды')


def main():
    connect, cursor = open_db_use_psycopg()

    command = menu()
    while command != 0:
        if command == 1:
            task_01(cursor)

        if command == 2:
            task_02_01(cursor)
            print(f"Выполнение запроса каждые 5 секунд настроено {bcolors.OKGREEN}успешно{bcolors.ENDC}")
            print(f"Информацию о выполнении запроса можно смотреть "
                  f"в лог файле {bcolors.OKCYAN}./log/log_db.txt{bcolors.ENDC}\n")

        if command == 3:
            task_02_02(cursor)
            print(f"Выполнение запроса каждые 5 секунд настроено {bcolors.OKGREEN}успешно{bcolors.ENDC}")
            print(f"Информацию о выполнении запроса можно смотреть "
                  f"в лог файле {bcolors.OKCYAN}./log/log_redis.txt{bcolors.ENDC}\n")

        if command == 4:
            task_04(cursor, connect)

        if command == 5:
            clean_log()

        command = menu()

    close_db_use_psycopg(connect, cursor)
    exit()


if __name__ == "__main__":
    main()
