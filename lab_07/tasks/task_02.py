import json
from support.tools import (
    bcolors,
    DIR_JSON_FILES,
    print_long_result_like_table
)
from support.support_db import (
    input_objects_from_json
)
from tasks.class_system import (
    Person,
    Order
)


def input_data_from_json():
    person_table = input_objects_from_json(f'{DIR_JSON_FILES}/persons.json', Person)
    order_table = input_objects_from_json(f'{DIR_JSON_FILES}/orders.json', Order)

    return person_table, order_table


def request_01(persons, orders):
    print(f"\n{bcolors.BOLD}\t\t\t{bcolors.UNDERLINE}ЗАПРОС №1{bcolors.ENDC}"
          f"\n{bcolors.BOLD}прочитать таблицу из json-документа{bcolors.ENDC}\n")

    print(f"{bcolors.OKCYAN}Результат{bcolors.ENDC}\nТаблица persons")
    print_long_result_like_table([p.get() for p in persons], Person.FIELD_SCHEMA, 5)

    print(f"{bcolors.OKCYAN}Результат{bcolors.ENDC}\nТаблица orders")
    print_long_result_like_table([o.get() for o in orders], Order.FIELD_SCHEMA, 5)


def request_02(persons):
    print(f"\n{bcolors.BOLD}\t\t{bcolors.UNDERLINE}ЗАПРОС №2{bcolors.ENDC}"
          f"\n{bcolors.BOLD}обновление json-документа{bcolors.ENDC}\n")

    """ Поменять человеку с id = 3002 имя на Пафнутий 🐁"""

    for p in persons:
        if p.person_id == 3002:
            p.name = 'Пафнутий 🐁'

    with open(f'{DIR_JSON_FILES}/persons_update.json', 'w') as f:
        for elem in persons:
            f.write(json.dumps(elem.get()))

    print(f"{bcolors.OKCYAN}Результат{bcolors.ENDC}\nТаблица persons")
    print_long_result_like_table([p.get() for p in persons], Person.FIELD_SCHEMA, 5)


def request_03(persons):
    print(f"\n{bcolors.BOLD}\t\t{bcolors.UNDERLINE}ЗАПРОС №3{bcolors.ENDC}"
          f"\n{bcolors.BOLD}добавление в json-документ{bcolors.ENDC}\n")

    persons.append(Person(1, 'Alex', 'TMO', 'TMO', '2022-11-18', None))

    with open(f'{DIR_JSON_FILES}/persons_update.json', 'w') as f:
        for elem in persons:
            f.write(json.dumps(elem.get()))

    print(f"{bcolors.OKCYAN}Результат{bcolors.ENDC}\nТаблица persons")
    print_long_result_like_table([p.get() for p in persons], Person.FIELD_SCHEMA, 5)


def task_02():
    persons, orders = input_data_from_json()

    request_01(persons, orders)
    request_02(persons)
    request_03(persons)

