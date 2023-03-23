from peewee import fn, SQL
import peewee
import datetime

from tools import (
    bcolors,
    print_result_like_table_use_list,
    print_long_result_like_table
)
from class_system import Employee, Record


def task_01(connect):
    print(f"\n{bcolors.BOLD}\t\t\t\t\t\t\t\t  {bcolors.UNDERLINE}ЗАПРОС №1{bcolors.ENDC}"
          f"\n{bcolors.BOLD}Найти отделы, в которых хоть один сотрудник опаздывает больше 3-х раз в неделю{bcolors.ENDC}\n")

    cur = connect.cursor()
    cur.execute(
        "with lox_emp as (                          "
        "    with date_emp as                       "
        "    (                                      "
        "        select rdate, employee_id          "
        "        from record                        "
        "        where rtype = 1                    "
        "        group by rdate, employee_id        "
        "        having min(rtime) > '09:30:00'     "
        "   )                                       "
        "   select distinct employee_id             "
        "   from date_emp                           "
        "   group by extract(week from rdate), employee_id "
        "   having count(rdate) >= 1                       "
        ")                                                 "
        "select department                                 "
        "from lox_emp l inner join employee e on l.employee_id = e.id "
    )

    print(f"Запрос {bcolors.HEADER}через SQL{bcolors.ENDC} выполнен {bcolors.OKGREEN}успешно{bcolors.ENDC}")
    print_result_like_table_use_list(cur.fetchall(), ['department'])

    # найти сотрудников, которые опоздали в конкретный день
    q1 = Record \
        .select(Record.rdate, Record.employee_id) \
        .where(Record.rtype == 1) \
        .group_by(Record.rdate, Record.employee_id) \
        .having(fn.min(Record.rtime) > '09:30:00')

    # найти сотрудников, опаздывающих более 3-х раз в неделю (конкретно здесь одного)
    q2 = q1 \
        .select(SQL('employee_id')) \
        .group_by(fn.Date_part('week', SQL('rdate')), SQL('employee_id')) \
        .having(fn.count(SQL('rdate')) >= 1)

    # остается добавить сюда отделы
    q3 = Employee \
        .select(Employee.department).distinct() \
        .join(q2, on=Employee.id == SQL('employee_id'))

    result = q3.dicts().execute()

    print(f"Запрос {bcolors.HEADER}через Python{bcolors.ENDC} выполнен {bcolors.OKGREEN}успешно{bcolors.ENDC}")
    print_long_result_like_table(result, ['department'])


def task_02(connect):
    print(f"\n{bcolors.BOLD}\t\t\t\t\t\t\t\t  {bcolors.UNDERLINE}ЗАПРОС №2{bcolors.ENDC}"
          f"\n{bcolors.BOLD}Найти средний возраст сотрудников, не находящихся на рабочем месте 8 часов в день{bcolors.ENDC}\n")

    cur = connect.cursor()
    cur.execute(
        "with lox_table as                                                                                     "
        "(                                                                                                     "
        "   with emp_time as                                                                                   "
        "   (                                                                                                  "
        "       select rdate, employee_id, rtype,                                                              "
        "              rtime as iin, lead(rtime) over(partition by (rdate, employee_id) order by rtime) as out "
        "       from record                                                                                    "
        "   )                                                                                                  "
        "   select rdate, employee_id, sum(extract(epoch from out - iin)) / 3600 as cnt_work_hours             "
        "   from emp_time                                                                                      "
        "   where rtype = 1                                                                                    "
        "   group by rdate, employee_id                                                                        "
        ")                                                                                                     "
        "select rdate, avg(date_part('year', age(birthdate))) as avg_agee                                      "
        "from lox_table inner join employee on lox_table.employee_id = employee.id                             "
        "where cnt_work_hours < 10                                                                             "
        "group by rdate;                                                                                       "
    )

    print(f"Запрос {bcolors.HEADER}через SQL{bcolors.ENDC} выполнен {bcolors.OKGREEN}успешно{bcolors.ENDC}")
    print_result_like_table_use_list(cur.fetchall(), ['rdate', 'avg_agree'])

    # query = (Employee
    #          .select(peewee.fn.AVG(
    #     peewee.fn.EXTRACT(peewee.fn.YEAR, datetime.date.today()) - peewee.fn.EXTRACT(peewee.fn.YEAR,
    #                                                                                  Employee.birthdate)).alias(
    #     'average_age'))
    #          .join(Record)
    #          .where(Record.rdate == datetime.date.today())
    #          .group_by(Employee.id)
    #          .having(peewee.fn.SUM(peewee.fn.EXTRACT(peewee.fn.HOUR, peewee.fn.LEAD(Record.rtime).over(
    #     partition_by=Record.employee_id)) - peewee.fn.EXTRACT(peewee.fn.HOUR, Record.rtime)) < 8))


    query = Employee.select().where(peewee.Expression(lambda: Employee.fio == 'John'))

    for employee in query:
        print(f'The average age of employees who are not in the workplace 8 hours a day is {employee.average_age}')

    # сделаем сводную таблицу время прихода - время ухода
    # q1 = Record \
    #     .select(
    #         Record.rdate,
    #         Record.employee_id,
    #         Record.rtype,
    #         Record.rtime.alias('iin'),
    #         fn.lead(Record.rdate).over(
    #             partition_by=[Record.rdate, Record.employee_id],
    #             order_by=[Record.rtime]
    #         )
    #     )
    #
    # result = q1.dicts().execute()
    # print_long_result_like_table(result, ['rdate', 'employee_id', 'rtype', 'iin', 'lead'])
    #
    # q2 = q1 \
    #     .select(
    #         # q1.c.rdate,
    #         SQL('lead'),
    #         # SQL('employee_id'),
    #         # SQL('out') - SQL('iin')
    #     )
    # result = q2.dicts().execute()
    # print_long_result_like_table(result, ['lead'])

    # q2 = q1 \
    #     .select(
    #         SQL('rdate'),
    #         SQL('employee_id'),
    #         ((SQL('out') - SQL('iin')) / 3600).alias('cnt_work_hours')
    #     ) \
    #     .where(SQL('rtype') == 1) \
    #     .group_by(SQL('rdate'), SQL('employee_id'))

    # result = q2.dicts().execute()
    # print_long_result_like_table(result, ['rdate', 'employee_id', 'cnt_work_hours'])
    # print(result)

    #
    # # найти сотрудников, опаздывающих более 3-х раз в неделю (конкретно здесь одного)
    # q2 = q1 \
    #     .select(SQL('employee_id')) \
    #     .group_by(fn.Date_part('week', SQL('rdate')), SQL('employee_id')) \
    #     .having(fn.count(SQL('rdate')) >= 1)
    #
    # # остается добавить сюда отделы
    # q3 = Employee \
    #     .select(Employee.department).distinct() \
    #     .join(q2, on=Employee.id == SQL('employee_id'))
    #
    # result = q3.dicts().execute()
    #
    # print(f"Запрос {bcolors.HEADER}через Python{bcolors.ENDC} выполнен {bcolors.OKGREEN}успешно{bcolors.ENDC}")
    # print_long_result_like_table(result, ['department'])
