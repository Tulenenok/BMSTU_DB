import random
from prettytable import PrettyTable, ALL
from tools import (
    bcolors,
    input_int_number
)


# ЗАДАНИЕ №1.
# Выполнить скалярный запрос
def task1(cursor, *params):
    print(f"\n{bcolors.BOLD}\t\t\t\t\t\t{bcolors.UNDERLINE}ЗАДАНИЕ №1{bcolors.ENDC}"
          f"\n{bcolors.BOLD}cкалярный запрос - по номеру заказала определить его цену{bcolors.ENDC}\n")

    order_no = input_int_number(f"{bcolors.OKCYAN}Введите номер заказа{bcolors.ENDC} "
                                f"(или E, если хотите вернуться в меню): ",
                                f"Номер заказа был введен {bcolors.FAIL}неправильно{bcolors.ENDC}"
                                f" (должно быть целое число)\n")

    if order_no is None:
        return

    cursor.execute(
        "select o.price from lab_1.orders o where o.order_no = %s",
        (order_no,)
    )

    ans = cursor.fetchall()
    if not ans:
        print(f"Заказа с номером {bcolors.OKCYAN}{order_no}{bcolors.ENDC} в базе {bcolors.OKCYAN}не найдено{bcolors.ENDC}\n")
        return


    print(f"\n{bcolors.OKCYAN}Результат{bcolors.ENDC}\n"
          f"Цена заказа с номером {bcolors.OKCYAN}{order_no}{bcolors.ENDC} равна {bcolors.OKCYAN}{ans[0][0]}{bcolors.ENDC}\n")


# ЗАДАНИЕ №2.
# Выполнить запрос с несколькими соединениями(JOIN)
def task2(cursor, *params):
    print(f"\n{bcolors.BOLD}\t\t\t\t\t\t{bcolors.UNDERLINE}ЗАДАНИЕ №2{bcolors.ENDC}"
          f"\n{bcolors.BOLD}соединения - по id человека определить количество его заказов {bcolors.ENDC}\n")

    person_id = input_int_number(f"{bcolors.OKCYAN}Введите ID человека{bcolors.ENDC} "
                                f"(или E, если хотите вернуться в меню): ",
                                f"ID был введен {bcolors.FAIL}неправильно{bcolors.ENDC}"
                                f" (должно быть целое число)\n")
    if person_id is None:
        return

    cursor.execute(
        "select p.person_id, p.name, p.sub_name, p.pat_name, count(order_id) "
        "from lab_1.persons p left join lab_1.orders o using(person_id) "
        "where p.person_id = %s"
        "group by p.person_id, p.name, p.sub_name, p.pat_name",

        (person_id, )
    )

    ans = cursor.fetchall()
    if not ans:
        print(f"Человека с ID {bcolors.OKCYAN}{person_id}{bcolors.ENDC} в базе {bcolors.OKCYAN}не найдено{bcolors.ENDC}\n")
        return

    print(f"{bcolors.OKCYAN}Результат{bcolors.ENDC}")
    tb = PrettyTable()
    tb.field_names = ["ID", 'Фамилия', 'Имя', 'Отчество', 'Количество заказов']
    tb.add_row(ans[0])
    print(tb, '\n')


# ЗАДАНИЕ №3.
# Выполнить запрос с ОТВ(CTE) и оконными функциями
def task3(cursor, *params):
    print(f"\n{bcolors.BOLD}\t\t\t\t\t\t\t\t  {bcolors.UNDERLINE}ЗАДАНИЕ №3{bcolors.ENDC}"
          f"\n{bcolors.BOLD}ОТВ и оконки - определить минимальную, среднюю и максимальную цену каждого материала {bcolors.ENDC}\n")

    cursor.execute(
        "with cle as ("
        "   select distinct "
        "       m.material, "
        "       min(m.price) over(partition by m.material),           "
        "       round(avg(m.price) over(partition by m.material), 2), "
        "       max(m.price) over(partition by m.material)            "
        "   from lab_1.building_materials m "
        ") "
        "select * from cle "
        "order by material"
    )

    ans = cursor.fetchall()

    print(f"{bcolors.OKCYAN}Результат{bcolors.ENDC}")
    tb = PrettyTable()
    tb.field_names = ["Материал", 'Минимальная цена', "Средняя цена", 'Максимальная цена']
    for row in ans:
        tb.add_row(row)
    print(tb, '\n')


# ЗАДАНИЕ №4.
# Выполнить запрос к метаданным
def task4(cursor, *params):
    print(f"\n{bcolors.BOLD}\t\t\t\t\t{bcolors.UNDERLINE}ЗАДАНИЕ №4{bcolors.ENDC}"
          f"\n{bcolors.BOLD}метаданные - получить информацию о схемах в бд{bcolors.ENDC}\n")

    cursor.execute(
        "select * from information_schema.schemata inf "
        "where inf.schema_name not in ('information_schema', 'pg_catalog', 'pg_toast') "
        "order by inf.schema_name"
    )

    schemas_inf = list(map(lambda x: list(x[:3]), cursor.fetchall()))

    # print(schemas_inf)

    for i, schema in enumerate(schemas_inf):
        cursor.execute(
            "select inf.table_name "
            "from information_schema.tables inf "
            "where inf.table_schema = %s "
            "order by inf.table_name ",

            (schema[1], )
        )

        tables_inf = []
        for tpl in cursor.fetchall():
            tables_inf += [t for t in tpl]

        schemas_inf[i].append('\n'.join(tables_inf) if tables_inf else [])

    # print(schemas_inf)

    print(f"{bcolors.OKCYAN}Результат{bcolors.ENDC}")
    tb = PrettyTable()
    tb.hrules = ALL
    tb.field_names = ["БД", 'Схема', "Владелец", 'Список таблиц']
    for row in schemas_inf:
        tb.add_row(row)
    print(tb, '\n')


# ЗАДАНИЕ №5.
# Вызвать скалярную функцию из ЛР 3
def task5(cursor, *params):
    # Пример для ввода 4, 1, '2022-10-26'
    print(f"\n{bcolors.BOLD}\t\t\t\t\t  {bcolors.UNDERLINE}ЗАДАНИЕ №5{bcolors.ENDC}"
          f"\n{bcolors.BOLD}скалярная функция - количество материала на складе на дату{bcolors.ENDC}\n")

    no_st = input_int_number(f"{bcolors.OKCYAN}Введите номер склада{bcolors.ENDC} (или E, если хотите вернуться в меню): ",
                             f"Номер склада был введен {bcolors.FAIL}неправильно{bcolors.ENDC} (должно быть целое число)\n")

    if no_st is None:
        return

    id_mat = input_int_number(f"{bcolors.OKCYAN}Введите ID материала{bcolors.ENDC} (или E, если хотите вернуться в меню): ",
                              f"Номер склада был введен {bcolors.FAIL}неправильно{bcolors.ENDC} (должно быть целое число)\n")

    if id_mat is None:
        return

    dt = input(f"{bcolors.OKCYAN}Введите дату{bcolors.ENDC} в формате год-месяц-день (например, 2022-10-26): ").strip()
    try:
        cursor.execute(
            "select * from public.get_count_material_on_stock(%s, %s, %s)",
            (no_st, id_mat, dt)
        )
    except:
        print(f'\nДата была введена {bcolors.FAIL}неверно{bcolors.ENDC}, не удалось посчитать ответ\n')
        return

    print(
        f"\n{bcolors.OKCYAN}Результат{bcolors.ENDC}\n"
        f"Количество материала с ID {bcolors.OKCYAN}{id_mat}{bcolors.ENDC} "
        f"на складе с номером {bcolors.OKCYAN}{no_st}{bcolors.ENDC} "
        f"на дату {bcolors.OKCYAN}{dt}{bcolors.ENDC} "
        f"равна {bcolors.OKCYAN}{cursor.fetchone()[0]}{bcolors.ENDC}\n")


# ЗАДАНИЕ №6.
# Вызвать многооператорную или табличную функцию из ЛР 3
def task6(cursor, *params):
    # Пример для ввода 4, 1, '2022-10-26'
    print(f"\n{bcolors.BOLD}\t\t\t\t\t               {bcolors.UNDERLINE}ЗАДАНИЕ №6{bcolors.ENDC}"
          f"\n{bcolors.BOLD}табличная функция - вывести все отгрузки такого-то исполнителя или с такой-то ценой{bcolors.ENDC}\n")

    person_id = input_int_number(f"{bcolors.OKCYAN}Введите ID человека{bcolors.ENDC} (или E, если хотите вернуться в меню): ",
                                 f"ID был введен {bcolors.FAIL}неправильно{bcolors.ENDC} (должно быть целое число)\n")
    if person_id is None:
        return

    min_price = input_int_number(f"{bcolors.OKCYAN}Введите минимальную цену{bcolors.ENDC} (или E, если хотите вернуться в меню): ",
                                 f"Минимальная цена была введена {bcolors.FAIL}неправильно{bcolors.ENDC} (должно быть целое число)\n")
    if min_price is None:
        return

    max_price = input_int_number(f"{bcolors.OKCYAN}Введите максимальную цену{bcolors.ENDC} (или E, если хотите вернуться в меню): ",
                                 f"Максимальная цена была введена {bcolors.FAIL}неправильно{bcolors.ENDC} (должно быть целое число)\n")
    if max_price is None:
        return

    cursor.execute(
        "select * from public.shipments_filter_person_date_price(%s, %s, %s)",
        (person_id, min_price, max_price)
    )

    print(f"{bcolors.OKCYAN}Результат{bcolors.ENDC}")
    tb = PrettyTable()
    tb.field_names = ["№", "ID отгрузки", 'Дата отгрузки', "ID материала", 'Кол-во материала', 'Цена', 'Имя отгрузщика']

    ans = cursor.fetchall()
    if len(ans) < 20:
        for i, row in enumerate(ans):
            tb.add_row([i + 1] + list(row))

    else:
        for i, row in enumerate(ans[:10]):
            tb.add_row([i] + list(row))
        tb.add_row(['...', '...', '...', '...', '...', '...', '...'])
        for i in range(len(ans) - 10, len(ans)):
            tb.add_row([i + 1] + list(ans[i]))

    print(tb, '\n')


# ЗАДАНИЕ №7.
# Вызвать хранимую процедуру из ЛР 3
def task7(cursor, *params):
    print(f"\n{bcolors.BOLD}\t\t\t\t\t{bcolors.UNDERLINE}ЗАДАНИЕ №7{bcolors.ENDC}"
          f"\n{bcolors.BOLD}хранимая процедура - поменять номер склада по его id{bcolors.ENDC}\n")

    no_st = input_int_number(
        f"{bcolors.OKCYAN}Введите ID склада{bcolors.ENDC} (или E, если хотите вернуться в меню): ",
        f"ID склада был введен {bcolors.FAIL}неправильно{bcolors.ENDC} (должно быть целое число)\n")
    if no_st is None:
        return

    new_no_st = input_int_number(
        f"{bcolors.OKCYAN}Введите новый номер склада{bcolors.ENDC} (или E, если хотите вернуться в меню): ",
        f"Номер склада был введен {bcolors.FAIL}неправильно{bcolors.ENDC} (должно быть целое число)\n")

    if new_no_st is None:
        return

    print(f"\n{bcolors.OKCYAN}Сейчас в таблице{bcolors.ENDC}")
    cursor.execute(
        "select whs_id, whs_no from lab_1.wh_stocks where whs_id = %s ",
        (no_st,)
    )

    ans = cursor.fetchall()
    tb = PrettyTable()
    tb.field_names = ["ID склада", 'Номер склада']
    for row in ans:
        tb.add_row(row)
    print(tb, '\n')

    if not ans:
        print(f"Склада с таким ID {bcolors.FAIL}не существует{bcolors.ENDC}, "
              f"процедура {bcolors.FAIL}не вызвана{bcolors.ENDC}\n")
        return


    cursor.execute(
        "call public.change_no_stocks(%s, %s)",
        (no_st, new_no_st)
    )

    print(f"{bcolors.OKCYAN}Процедура выполнена{bcolors.ENDC}")

    connect = params[0]
    connect.commit()


    print(f"\n{bcolors.OKCYAN}Проверка{bcolors.ENDC}")
    cursor.execute(
        "select whs_id, whs_no from lab_1.wh_stocks where whs_id = %s ",
        (no_st,)
    )

    tb = PrettyTable()
    tb.field_names = ["ID склада", 'Номер склада']
    for row in cursor.fetchall():
        tb.add_row(row)
    print(tb, '\n')


# ЗАДАНИЕ №8.
# Вызвать системную функцию или процедуру
# https://postgrespro.ru/docs/postgrespro/10/functions-info
def task8(cursor, *params):
    print(f"\n{bcolors.BOLD}\t\t\t\t\t{bcolors.UNDERLINE}ЗАДАНИЕ №8{bcolors.ENDC}"
          f"\n{bcolors.BOLD}системные функции - получить имя бд и имя пользователя{bcolors.ENDC}\n")

    cursor.execute(
        "select current_database(), current_user;"
    )

    ans = cursor.fetchall()
    print(f"{bcolors.OKCYAN}Результат{bcolors.ENDC}")
    print(f"Имя текущей базы данных: {bcolors.OKCYAN}{ans[0][0]}{bcolors.ENDC}, "
          f"имя пользователя: {bcolors.OKCYAN}{ans[0][1]}{bcolors.ENDC}\n")


# ЗАДАНИЕ №9.
# Создать таблицу в базе данных, соответствующую тематике БД
def task9(cursor, *params):
    print(f"\n{bcolors.BOLD}\t\t\t\t\t{bcolors.UNDERLINE}ЗАДАНИЕ №9{bcolors.ENDC}"
          f"\n{bcolors.BOLD}создать таблицу - таблица заводов, поставляющих материалы {bcolors.ENDC}\n")

    cursor.execute(
        "create table if not exists lab_1.factories("
        "   factoty_id serial primary key,"
        "   material varchar(64),"
        "   note varchar(64)"
        ")"
    )

    connect = params[0]
    connect.commit()

    print(f"{bcolors.OKCYAN}Таблица успешно создана{bcolors.ENDC}\n")


# ЗАДАНИЕ №10.
# Выполнить вставку данных в созданную таблицу с использованием инструкции INSERT или COPY
def task10(cursor, *params):
    connect = params[0]

    print(f"\n{bcolors.BOLD}\t\t\t\t\t{bcolors.UNDERLINE}ЗАДАНИЕ №10{bcolors.ENDC}"
          f"\n{bcolors.BOLD}вставить данные в созданную таблицу {bcolors.ENDC}\n")

    cursor.execute(
        "select distinct m.material from lab_1.building_materials m order by material"
    )

    unique_mat_id = []
    for tpl in cursor.fetchall():
        unique_mat_id += [t for t in tpl]

    # Почистить таблицу перед вставкой
    cursor.execute(
        "delete from lab_1.factories; "
        "ALTER SEQUENCE lab_1.factories_factoty_id_seq RESTART WITH 1;"
    )

    count_factories = 10
    for i in range(count_factories):
        cursor.execute(
            "insert into lab_1.factories(material, note) "
            "values (%s, %s)",

            (random.choice(unique_mat_id), random.choice(['very important',
                                                          'unimportant',
                                                          'need to bring',
                                                          'mriak']))
        )

    connect.commit()
    print(f'{bcolors.OKCYAN}Данные успешно загружены{bcolors.ENDC}\n')

    cursor.execute(
        "select * from lab_1.factories"
    )

    tb = PrettyTable()
    tb.field_names = ["ID завода", 'Материал', 'Заметка']
    for row in cursor.fetchall():
        tb.add_row(row)
    print(tb, '\n')


LIST_TASKS = [task1, task2, task3, task4, task5, task6, task7, task8, task9, task10]