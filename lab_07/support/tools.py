from prettytable import PrettyTable, ALL

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


DIR_CSV_FILES = '/users/gurovana/Documents/scripts/lab_07/csv'
DIR_JSON_FILES = '/users/gurovana/Documents/scripts/lab_07/json'


def is_int(x: str) -> bool:
    try:
        int(x)
        return True
    except:
        return False


def input_int_number(input_str, fail_str):
    while True:
        order_no = input(input_str)
        if order_no == 'E' or order_no == 'e' or order_no == 'е' or order_no == 'Е':
            print()
            return

        if is_int(order_no):
            return int(order_no)

        print(fail_str)


def print_result_like_table(list_result: list, schema: list):
    """ Вывести полученную в результате запроса таблицу в красивом виде """

    print(f"{bcolors.OKCYAN}Результат{bcolors.ENDC}")

    tb = PrettyTable()
    tb.field_names = schema

    for dt in list_result:
        row = [dt[field] for field in schema]
        tb.add_row(row)

    print(tb, '\n')


def print_long_result_like_table(list_result: list, schema: list, count_show=10):
    if len(list_result) <= 2 * count_show:
        print_result_like_table(list_result, schema)
        return

    tb = PrettyTable()
    tb.field_names = schema

    for dt in list_result[0:count_show]:
        row = [dt[field] for field in schema]
        tb.add_row(row)

    tb.add_row(['...' for _ in schema])

    for dt in list_result[len(list_result) - count_show:]:
        row = [dt[field] for field in schema]
        tb.add_row(row)

    print(tb, '\n')
