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