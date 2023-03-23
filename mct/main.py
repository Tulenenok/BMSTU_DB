from support_db import (
    open_db_use_peewee,
    close_db_use_peewee
)
from tasks import (
    task_01,
    task_02
)


def main():
    connect = open_db_use_peewee()

    task_01(connect)
    task_02(connect)

    close_db_use_peewee(connect)


if __name__ == '__main__':
    main()

