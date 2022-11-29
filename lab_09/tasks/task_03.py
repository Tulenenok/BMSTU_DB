import threading
from random import randint

import redis
import json
from support.tools import *
import datetime
import matplotlib.pyplot as plt
from time import time

N_REPEATS = 10

# Провести сравнительный анализ времени выполнения запросов
def draw_plots(d1: list = None, d2: list = None, d3: list = None, d4: list = None):
    """ d1 - результат без изменения данных """
    """ d2 - результат при добавлении новых строк """
    """ d3 - результат при удалении строк """
    """ d4 - результат при изменении строк """

    if d1 is not None:
        index = ["БД", "Redis"]
        # values = [0.013663472843170166, 0.010023893350323242]
        plt.bar(index, d1)
        plt.title("Без изменения данных")
        plt.show()

    if d2 is not None:
        index = ["БД", "Redis"]
        # values = [0.00035931119918823245, 0.0013577041625976562]
        plt.bar(index, d2)
        plt.title("При добавлении новых строк каждые 10 секунд")
        plt.show()

    if d3 is not None:
        index = ["БД", "Redis"]
        # values = [0.0019226646423339843, 0.0015000951766967773]
        plt.bar(index, d3)
        plt.title("При удалении строк каждые 10 секунд")
        plt.show()

    if d4 is not None:
        index = ["БД", "Redis"]
        # values = [0.000199527530670166, 0.0010328336715698242]
        plt.bar(index, d4)
        plt.title("При изменении строк каждые 10 секунд")
        plt.show()


def request_01(cursor):
    """ Запрос без изменения """
    t1 = time()
    cursor.execute("select person_id, count(*) "
                   "from orders "
                   "group by person_id "
                   "order by person_id;")
    t2 = time()

    result = cursor.fetchall()

    redis_client = redis.Redis()        #host="localhost", port=6379, db=0)
    data = json.dumps(result)
    cache_value = redis_client.get("r1")
    if cache_value is None:
        redis_client.set("r1", data)

    t11 = time()
    redis_client.get("r1")
    t22 = time()

    redis_client.close()
    return t2 - t1, t22 - t11


def request_02(cursor, con):
    redis_client = redis.Redis()

    t1 = time()
    cursor.execute("select person_id, count(*) "
                   "from orders "
                   "group by person_id "
                   "order by person_id;")
    t2 = time()

    wid = randint(100000, 1000000)

    t11 = time()
    redis_client.delete(f"r{wid}")
    t22 = time()

    redis_client.close()
    con.commit()

    return t2 - t1, t22 - t11


def request_02(cur, con):
    redis_client = redis.Redis()

    wid = randint(100000, 1000000)

    t1 = time()
    cur.execute(f"delete from orders where order_id = {wid};")
    t2 = time()

    t11 = time()
    redis_client.delete(f"w{wid}")
    t22 = time()

    redis_client.close()

    con.commit()

    return t2 - t1, t22 - t11


def request_03(cur, con):
    redis_client = redis.Redis()

    wid = 1
    val = randint(100000, 1000000)
    p = randint(100000, 1000000)

    t1 = time()
    cur.execute(f"insert into orders(order_id, order_date, order_no, order_state, "
                f"shipment_date, price, shipment_price, note, inp_date, person_id)"
                f"values ({val}, Null, 1, 2, Null, 100, 50, Null, '2022-11-29', {p});")
    t2 = time()

    cur.execute("select person_id, count(*) "
                "from orders "
                "group by person_id "
                "order by person_id;")

    result = cur.fetchall()
    data = json.dumps(result)

    t11 = time()
    redis_client.set(f"w{wid}", data)
    t22 = time()

    redis_client.close()

    con.commit()
    return t2 - t1, t22 - t11


def request_04(cur, con):
    redis_client = redis.Redis()
    wid = randint(1, 1000)

    t1 = time()
    cur.execute(f"UPDATE orders SET person_id = 1 WHERE order_id = {wid}")
    t2 = time()

    cur.execute("select person_id, count(*) "
                "from orders "
                "group by person_id "
                "order by person_id;")

    result = cur.fetchall()
    data = json.dumps(result)

    t11 = time()
    redis_client.set(f"w{wid}", data)
    t22 = time()

    redis_client.close()

    con.commit()
    return t2 - t1, t22 - t11


def task_04(cursor, connect):
    d1 = [0, 0]
    d2 = [0, 0]
    d3 = [0, 0]
    d4 = [0, 0]
    for i in range(N_REPEATS):
        tmp = request_01(cursor)
        d1[0] += tmp[0]
        d1[1] += tmp[1]

        tmp = request_02(cursor, connect)
        d2[0] += tmp[0]
        d2[1] += tmp[1]

        tmp = request_03(cursor, connect)
        d3[0] += tmp[0]
        d3[1] += tmp[1]

        tmp = request_04(cursor, connect)
        d4[0] += tmp[0]
        d4[1] += tmp[1]

    d1 = [d1[0] / N_REPEATS, d1[1] / N_REPEATS]
    d2 = [d2[0] / N_REPEATS, d2[1] / N_REPEATS]
    d3 = [d3[0] / N_REPEATS, d3[1] / N_REPEATS]
    d3 = [d4[0] / N_REPEATS, d4[1] / N_REPEATS]

    draw_plots(d1, d3, d2, d4)
