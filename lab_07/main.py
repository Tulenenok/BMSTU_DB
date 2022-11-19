from support.tools import (
    bcolors,
    is_int,
    DIR_CSV_FILES,
    DIR_JSON_FILES
)
from support.support_db import (
    open_db_use_psycopg,
    open_db_use_peewee,
    close_db_use_psycopg,
    close_db_use_peewee,
    put_from_db_to_csv,
    put_from_db_to_json
)
from tasks.task_01 import task_01
from tasks.task_02 import task_02
from tasks.task_03 import task_03


def menu():
    print(f"{bcolors.HEADER}Меню{bcolors.ENDC}\n"
          f"  {bcolors.HEADER}0.{bcolors.ENDC} Выход\n"
          f"  {bcolors.HEADER}1.{bcolors.ENDC} Задание 1\n"
          f"  {bcolors.HEADER}2.{bcolors.ENDC} Задание 2\n"
          f"  {bcolors.HEADER}3.{bcolors.ENDC} Задание 3\n"
          f"  {bcolors.HEADER}4.{bcolors.ENDC} Обновить csv-файлы\n"
          f"  {bcolors.HEADER}5.{bcolors.ENDC} Обновить json-файлы\n")

    while True:
        command = input(f'{bcolors.HEADER}Введите номер команды:{bcolors.ENDC} ')

        if is_int(command) and 0 <= int(command) <= 5:
            return int(command)

        print('Неверный номер команды')


def update_csv_files(cursor):
    put_from_db_to_csv(cursor, 'lab_1.persons', f'{DIR_CSV_FILES}/persons.csv')
    put_from_db_to_csv(cursor, 'lab_1.orders', f'{DIR_CSV_FILES}/orders.csv')
    put_from_db_to_csv(cursor, 'lab_1.order_detail', f'{DIR_CSV_FILES}/order_details.csv')
    put_from_db_to_csv(cursor, 'lab_1.building_materials', f'{DIR_CSV_FILES}/materials.csv')

    print(f"{bcolors.OKGREEN}CSV-файлы успешно обновлены{bcolors.ENDC}")


def update_json_files(cursor):
    put_from_db_to_json(cursor, 'lab_1.persons', f'{DIR_JSON_FILES}/persons.json')
    put_from_db_to_json(cursor, 'lab_1.orders', f'{DIR_JSON_FILES}/orders.json')
    put_from_db_to_json(cursor, 'lab_1.order_detail', f'{DIR_JSON_FILES}/order_details.json')
    put_from_db_to_json(cursor, 'lab_1.building_materials', f'{DIR_JSON_FILES}/materials.json')

    print(f"{bcolors.OKGREEN}JSON-файлы успешно обновлены{bcolors.ENDC}")


def main():
    command = menu()
    while command != 0:
        if command == 1:
            task_01()

        if command == 2:
            task_02()

        if command == 3:
            task_03()

        if command in (4, 5):
            connect, cursor = open_db_use_psycopg()

            if connect == -1:
                exit()

            if command == 4:
                update_csv_files(cursor)
            if command == 5:
                update_json_files(cursor)

            close_db_use_psycopg(connect, cursor)

        command = menu()


if __name__ == "__main__":
    main()
