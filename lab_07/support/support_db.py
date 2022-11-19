import psycopg2, peewee
from support.tools import bcolors


def open_db_use_psycopg(db="lab_1", usr="", password="", host="127.0.0.1", port="5432"):
    """ Открыть подключение к базе данных """
    """ Возвращает 'дескриптор подключения' и курсор в случае успеха и -1, -1 в случае ошибки"""

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
        print(f"\nПодключение к БД --> {bcolors.FAIL}FAILURE{bcolors.ENDC}\n")
        return -1, -1

    print(f"\nПодключение к БД --> {bcolors.OKGREEN}SUCCESS{bcolors.ENDC}\n")
    return connect, connect.cursor()


def close_db_use_psycopg(connect, cursor):
    """ Закрыть подключение к базе данных """

    cursor.close()
    connect.close()

    print(f"\nЗакрыть подключение к БД --> {bcolors.OKGREEN}SUCCESS{bcolors.ENDC}\n")


def open_db_use_peewee(db="lab_1", usr="", password="", host="127.0.0.1", port="5432"):
    """ Открыть подключение к базе данных """
    """ Возвращает 'дескриптор подключения' и курсор в случае успеха и -1, -1 в случае ошибки"""

    try:
        connect = peewee.PostgresqlDatabase(
                database=db,
                user=usr,
                password=password,
                host=host,
                port=port
            )
    except:
        print(f"\nПодключение к БД --> {bcolors.FAIL}FAILURE{bcolors.ENDC}\n")
        return -1, -1

    print(f"\nПодключение к БД --> {bcolors.OKGREEN}SUCCESS{bcolors.ENDC}\n")
    return connect


def close_db_use_peewee(connect):
    """ Закрыть подключение к базе данных """
    connect.close()

    print(f"\nЗакрыть подключение к БД --> {bcolors.OKGREEN}SUCCESS{bcolors.ENDC}\n")


def put_from_db_to_csv(cursor, table_name: str, filename: str):
    """ Записать таблицу с именем table_name в файл filename (CSV формат)"""

    cursor.execute(
        f"copy (select * from {table_name}) to '{filename}' with csv delimiter ',';"
    )


def put_from_db_to_json(cursor, table_name: str, filename: str):
    """ Записать таблицу с именем table_name в файл filename (JSON формат)"""

    cursor.execute(
        f"copy "
        f"(select row_to_json(t) result from {table_name} t) "
        f"to '{filename}';"
    )


def input_list_from_csv(filename):
    """ Функция возвращает массив массивов, каждый внутренний массив - распершеная стрка csv-файла """
    file = open(filename, 'r')
    dst_list = [list(line.strip().split(',')) for line in file]
    file.close()

    return dst_list


def input_objects_from_csv(filename, class_object):
    """ Функция возвращает массив объектов, считанных из csv-файла """
    list_rows = input_list_from_csv(filename)
    dst_list = []

    for params in list_rows:
        new_object = class_object(*[func(p) if p != '' else None for func, p in zip(class_object.LIST_SCHEMA, params)])
        dst_list.append(new_object.get())  # Использование здесь метода get - говнокод, но накручивать логику не буду

    return dst_list


def input_list_from_json(filename):
    """ Функция возвращает массив словарей, каждый словарь - строка из json-файла """
    file = open(filename, 'r')
    dst_list = [eval(line.strip().replace('null', 'None')) for line in file]
    file.close()

    return dst_list


def input_objects_from_json(filename, class_object):
    """ Функция возвращает массив объектов, считанных из json-файла"""

    list_rows = input_list_from_json(filename)
    dst_list = []

    for row in list_rows:
        tmp = []
        for field in class_object.FIELD_SCHEMA:
            tmp.append(class_object.DICT_SCHEMA[field](row[field]) if row != '' else None)

        new_object = class_object(*tmp)
        dst_list.append(new_object)  # А здесь метода get нет !

    return dst_list