import threading
import redis
import json
from support.tools import *
import datetime


# Выполнять запрос на стороне бд каждые 5 секунд
def task_02_01(cursor):
    threading.Timer(5.0, task_02_01, [cursor]).start()

    cursor.execute("select person_id, count(*) "
                   "from orders "
                   "group by person_id "
                   "order by person_id;")

    result = cursor.fetchall()

    with open(f"{LOG_DB}", 'a') as f:
        date_now = datetime.datetime.now()
        f.write(f"{date_now.strftime('%H-%M-%S')} ::: запрос на стороне бд выполнен {bcolors.OKGREEN}успешно{bcolors.ENDC}\n")


# Выполнять выполняет запрос каждые 5 секунд через Redis в качестве кэша.
def task_02_02(cursor):
    threading.Timer(5.0, task_02_02, [cursor]).start()

    redis_client = redis.Redis(host="localhost", port=6379, db=0)

    cache_value = redis_client.get("task_02_02")
    if cache_value is None:
        cursor.execute("select person_id, count(*) "
                       "from orders "
                       "group by person_id "
                       "order by person_id;")

        res = cursor.fetchall()
        redis_client.set("task_02_02", json.dumps(res))

    else:
        json.loads(cache_value)

    redis_client.close()

    with open(f"{LOG_REDIS}", 'a') as f:
        date_now = datetime.datetime.now()
        f.write(f"{date_now.strftime('%H-%M-%S')} ::: запрос через Redis выполнен {bcolors.OKGREEN}успешно{bcolors.ENDC}\n")
