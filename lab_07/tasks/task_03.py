import peewee
from support.tools import (
    bcolors,
    print_long_result_like_table
)

DB_CONNECT = peewee.PostgresqlDatabase(
    database="lab_1",
    user="",
    password="",
    host="127.0.0.1",
    port="5432"
)


class BaseModel(peewee.Model):
    class Meta:
        database = DB_CONNECT


class Persons(BaseModel):
    LIST_SCHEMA = [int, str, str, str, str, str]
    FIELD_SCHEMA = ['id', 'name', 'sub_name', 'pat_name', 'inp_date', 'notes']
    DICT_SCHEMA = {field: type_field for field, type_field in zip(FIELD_SCHEMA, LIST_SCHEMA)}

    id = peewee.IntegerField(column_name='person_id')       # Обязательно именно id
    name = peewee.CharField(column_name='name')
    pat_name = peewee.CharField(column_name='pat_name')
    sub_name = peewee.CharField(column_name='sub_name')
    inp_date = peewee.CharField(column_name='inp_date')
    notes = peewee.CharField(column_name='notes')

    class Meta:
        table_name = 'persons'                              # Таблица должна лежать в public


class Orders(BaseModel):
    LIST_SCHEMA = [int, str, int, int, str, int, int, str, str, int]
    FIELD_SCHEMA = ['id', 'order_date', 'order_no', 'order_state', 'shipment_date', 'price',
                    'shipment_price', 'note', 'inp_date', 'person_id']
    DICT_SCHEMA = {field: type_field for field, type_field in zip(FIELD_SCHEMA, LIST_SCHEMA)}

    id = peewee.IntegerField(column_name='order_id')  # Обязательно именно id
    order_date = peewee.CharField(column_name='order_date')
    order_no = peewee.IntegerField(column_name='order_no')
    order_state = peewee.IntegerField(column_name='order_state')
    shipment_date = peewee.CharField(column_name='shipment_date')
    price = peewee.IntegerField(column_name='price')
    shipment_price = peewee.IntegerField(column_name='shipment_price')
    note = peewee.CharField(column_name='note')
    inp_date = peewee.CharField(column_name='inp_date')
    person_id = peewee.IntegerField(column_name='person_id')

    class Meta:
        table_name = 'orders'


# В какой-то момент я отчаялась разобраться с проблемой поля id в этой библиотеке
# Поэтому создала эту максимально топорную таблицу
class Factories(BaseModel):
    LIST_SCHEMA = [int, str, str]
    FIELD_SCHEMA = ['id', 'material', 'note']
    DICT_SCHEMA = {field: type_field for field, type_field in zip(FIELD_SCHEMA, LIST_SCHEMA)}

    id = peewee.IntegerField(column_name='id')
    material = peewee.IntegerField(column_name='material')
    note = peewee.IntegerField(column_name='note')

    class Meta:
        table_name = 'factories'


def request_01():
    print(f"\n{bcolors.BOLD}\t\t  {bcolors.UNDERLINE}ЗАПРОС №1{bcolors.ENDC}"
          f"\n{bcolors.BOLD}однотабличный запрос на выборку{bcolors.ENDC}\n")

    """ Первые 10 человек с фамилией Иванов"""
    query = Persons.select().where(Persons.name == 'Иванов').limit(10).order_by(Persons.id)
    result = query.dicts().execute()

    print_long_result_like_table(result, Persons.FIELD_SCHEMA)


def request_02():
    print(f"\n{bcolors.BOLD}\t\t  {bcolors.UNDERLINE}ЗАПРОС №2{bcolors.ENDC}"
          f"\n{bcolors.BOLD}многотабличный запрос на выборку{bcolors.ENDC}\n")

    query = Orders \
        .select(Orders.person_id, Orders.order_date, Orders.order_no, Orders.price) \
        .join(Persons, on=(Orders.person_id == Persons.id)) \
        .where(Persons.id == 3008) \
        .order_by(Orders.order_date)

    result = query.dicts().execute()
    print_long_result_like_table(result, ['person_id', 'order_date', 'order_no', 'price'])


def request_03():
    global DB_CONNECT

    print(f"\n{bcolors.BOLD}\t{bcolors.UNDERLINE}ЗАПРОС №3{bcolors.ENDC}"
          f"\n{bcolors.BOLD}добавление данных{bcolors.ENDC}\n")

    try:
        with DB_CONNECT.atomic() as atomic_connect:
            new_f = Factories.create(id=11, material='bb', note="nnn")
            print('Запись добавлена\n')
            new_f.save()
    except:
        print('Не удалось добавить запись (такой id уже существует)')
        atomic_connect.rollback()
        # P.S. Обработка добавления происходит, так как у меня id выставлен как первичный ключ

    query = Factories.select().order_by(Factories.id)
    result = query.dicts().execute()
    print_long_result_like_table(result, Factories.FIELD_SCHEMA)


def request_04():
    global DB_CONNECT

    print(f"\n{bcolors.BOLD}\t{bcolors.UNDERLINE}ЗАПРОС №4{bcolors.ENDC}"
          f"\n{bcolors.BOLD}обновление данных{bcolors.ENDC}\n")

    upd_f = Factories(id=11)
    upd_f.note = 'примите лабу, пожалуйста'
    upd_f.save()
    print('Запись обновлена\n')

    query = Factories.select().order_by(Factories.id)
    result = query.dicts().execute()
    print_long_result_like_table(result, Factories.FIELD_SCHEMA)


def request_05():
    global DB_CONNECT

    print(f"\n{bcolors.BOLD}  {bcolors.UNDERLINE}ЗАПРОС №5{bcolors.ENDC}"
          f"\n{bcolors.BOLD}удаление данных{bcolors.ENDC}\n")

    del_f = Factories(id=11)
    del_f.delete_instance()
    print('Запись удалена\n')

    query = Factories.select().order_by(Factories.id)
    result = query.dicts().execute()
    print_long_result_like_table(result, Factories.FIELD_SCHEMA)


def request_06():
    global DB_CONNECT

    print(f"\n{bcolors.BOLD}\t\t\t\t     {bcolors.UNDERLINE}ЗАПРОС №6{bcolors.ENDC}"
          f"\n{bcolors.BOLD}получение доступа к данным с помощью хранимой процедуры{bcolors.ENDC}\n")

    cursor = DB_CONNECT.cursor()
    cursor.execute("call change_note_in_factories(%s, %s);", (2, "я молодец"))
    DB_CONNECT.commit()
    cursor.close()

    query = Factories.select().order_by(Factories.id)
    result = query.dicts().execute()
    print_long_result_like_table(result, Factories.FIELD_SCHEMA)


def task_03():
    request_01()
    request_02()
    request_03()
    request_04()
    request_05()
    request_06()
