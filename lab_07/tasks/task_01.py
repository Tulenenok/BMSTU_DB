import py_linq
from tasks.class_system import (
    Person,
    Order,
    OrderDetail,
    Material
)
from support.tools import (
    bcolors,
    DIR_CSV_FILES,
    print_result_like_table,
    print_long_result_like_table
)
from support.support_db import (
    input_objects_from_csv
)


def input_data_from_csv():
    persons = py_linq.Enumerable(input_objects_from_csv(f'{DIR_CSV_FILES}/persons.csv', Person))
    orders = py_linq.Enumerable(input_objects_from_csv(f'{DIR_CSV_FILES}/orders.csv', Order))
    order_details = py_linq.Enumerable(input_objects_from_csv(f'{DIR_CSV_FILES}/order_details.csv', OrderDetail))
    materials = py_linq.Enumerable(input_objects_from_csv(f'{DIR_CSV_FILES}/materials.csv', Material))

    print(f"{bcolors.OKGREEN}\nДанные из CSV-файлов успешно загружены{bcolors.ENDC}\n")
    return persons, orders, order_details, materials


def request_01(orders):
    print(f"\n{bcolors.BOLD}\t\t\t\t\t\t\t{bcolors.UNDERLINE}ЗАПРОС №1{bcolors.ENDC}"
          f"\n{bcolors.BOLD}найти все заказы, у которых цена < 3000 и которые еще не отгружали{bcolors.ENDC}\n")

    result = orders \
        .select(lambda x: x) \
        .where(lambda x: x['shipment_price'] == 0 and x['price'] < 3000) \
        .order_by(lambda x: x['price'])

    print_result_like_table(result, Order.FIELD_SCHEMA)


def request_02(persons):
    print(f"\n{bcolors.BOLD}\t\t\t  {bcolors.UNDERLINE}ЗАПРОС №2{bcolors.ENDC}"
          f"\n{bcolors.BOLD}количество людей в базе с именем Иван{bcolors.ENDC}\n")

    result = persons \
        .count(lambda x: x['sub_name'] == 'Иван') \

    print(f"{bcolors.OKCYAN}Результат{bcolors.ENDC}\n"
          f"Количество людей с именем Иван: {bcolors.OKCYAN}{result}{bcolors.ENDC}\n")


def request_03(order_details, materials):
    print(f"\n{bcolors.BOLD}\t\t\t\t\t  {bcolors.UNDERLINE}ЗАПРОС №3{bcolors.ENDC}"
          f"\n{bcolors.BOLD}какие материалы и в каком количестве требуются в заказе{bcolors.ENDC}\n")

    mat_selection = py_linq.Enumerable(
        materials.select(lambda x: {'title': x['title'], 'material': x['material'], 'mat_id': x['mat_id']})
    )
    od_selection = py_linq.Enumerable(
        order_details.select(lambda x: {'order_id': x['order_id'], 'mat_id': x['mat_id'], 'quant': x['quant']})
    )

    result = od_selection \
        .join(mat_selection, lambda o_k: o_k['mat_id'], lambda i_k: i_k['mat_id']) \
        .take(10)

    dst = list()
    for tpl in result:
        tpl[1].pop('mat_id')
        dst.append(tpl[0] | tpl[1])

    print_result_like_table(dst, ['order_id', 'mat_id', 'title', 'material', 'quant'])


def request_04(orders):
    print(f"\n{bcolors.BOLD}\t\t\t {bcolors.UNDERLINE}ЗАПРОС №4{bcolors.ENDC}"
          f"\n{bcolors.BOLD}какие детали производит фабрика с id{bcolors.ENDC}\n")\

    define_id = 2

    result = orders \
        .group_by(key_names=['person_id'], key=lambda x: x['person_id']) \
        .select(lambda x: {'person_id': x.key.person_id, 'count': x.count()}) \
        .order_by(lambda x: x['person_id'])

    print_long_result_like_table(result.to_list(), ['person_id', 'count'], 7)


def request_05(order_details):
    print(f"\n{bcolors.BOLD}\t\t\t {bcolors.UNDERLINE}ЗАПРОС №5{bcolors.ENDC}"
          f"\n{bcolors.BOLD}скольким заказам требуется материал с id{bcolors.ENDC}\n")\

    define_id = 181

    result = order_details \
        .count(lambda x: x['mat_id'] == define_id)

    print(f"{bcolors.OKCYAN}Результат{bcolors.ENDC}\n"
          f"Количество заказов, которым требуется материал с id = {define_id}: {bcolors.OKCYAN}{result}{bcolors.ENDC}\n")


def task_01():
    # Считываем таблицы из csv-файлов
    persons, orders, order_details, materials = input_data_from_csv()

    # Фигачим запросы
    request_01(orders)
    request_02(persons)
    request_03(order_details, materials)
    request_04(orders)
    request_05(order_details)
