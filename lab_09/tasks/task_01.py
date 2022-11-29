import redis
import json
from support.tools import *


def simple_request(cursor):
    redis_client = redis.Redis(host="localhost", port=6379, db=0)

    cache_value = redis_client.get("simple_request")
    if cache_value is not None:
        redis_client.close()
        return json.loads(cache_value)

    cursor.execute("select person_id, count(*) "
                "from orders "
                "group by person_id "
                "order by person_id;")
    res = cursor.fetchall()

    redis_client.set("simple_request", json.dumps(res))
    redis_client.close()

    return res


def task_01(cursor):
    print(f"\n{bcolors.BOLD}\t\t\t\t\t{bcolors.UNDERLINE}ЗАПРОС №1{bcolors.ENDC}"
          f"\n{bcolors.BOLD}простой запрос: id человека - количество его заказов{bcolors.ENDC}\n")

    res = simple_request(cursor)

    print(f"Запрос выполнен {bcolors.OKGREEN}успешно{bcolors.ENDC}\nРезультат:")
    print_long_result_like_table_use_list(res, ['person_id', 'count_orders'], 5)

