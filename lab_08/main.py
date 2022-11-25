import datetime
import json
import os
import time

from faker import Faker
from tools import bcolors

PERSON_ID = 1

class Person:
    """ Структура класса соответствует структуре таблицы persons """

    LIST_SCHEMA = [int, str, str, str, str, str]
    FIELD_SCHEMA = ['person_id', 'name', 'sub_name', 'pat_name', 'inp_date', 'notes']
    DICT_SCHEMA = {field: type_field for field, type_field in zip(FIELD_SCHEMA, LIST_SCHEMA)}

    def __init__(self, p_id: int, name: str, sub_name: str, pat_name: str, input_date: str, notes: str):
        self.person_id = p_id
        self.name = name
        self.sub_name = sub_name
        self.pat_name = pat_name
        self.inp_date = input_date
        self.notes = notes

    def get(self) -> dict:
        return {
            'person_id': self.person_id,
            'name': self.name,
            'sub_name': self.sub_name,
            'pat_name': self.pat_name,
            'inp_date': self.inp_date,
            'notes': self.notes
        }

    def __str__(self) -> str:
        return f'person_id: {self.person_id}, ' \
               f'name: {self.name}, ' \
               f'sub_name: {self.sub_name}, ' \
               f'pat_name: {self.pat_name}, ' \
               f'inp_date: {self.inp_date}, ' \
               f'notes: {self.notes}\n'


def main():
    global PERSON_ID
    print(f"\n{bcolors.BOLD}\t\t\t\t\t\t\t   {bcolors.UNDERLINE}{bcolors.HEADER}ЗАДАНИЕ №1{bcolors.ENDC}"
          f"\n{bcolors.BOLD}Разработать приложение, генерирующее файл в формате JSON/XML/CSV с данными, "
          f"\nсоответствующими теме БД. С частотой раз в 5 минут необходимо создавать "
          f"\nновый файл, имя которого соответствует разработанной маске.{bcolors.ENDC}\n")

    faker = Faker()
    while True:
        date_now = datetime.datetime.now()

        # Создать директорию, если она не существует
        work_directory = "json/" + date_now.strftime("%Y-%m-%d")
        if not os.path.exists(work_directory):
            os.makedirs(work_directory)

        work_file = work_directory + '/' + date_now.strftime('%H-%M-%S') + '.json'

        f = open(work_file, 'w')

        for i in range(100):
            name, sub_name = faker.name().split()[:2]
            pat_name = faker.text()[:7]
            inp_date = date_now.strftime("%Y-%m-%d")
            some_text = faker.text()[:20]

            new_obj = Person(PERSON_ID, name, sub_name, pat_name, inp_date, some_text)
            f.write(json.dumps(new_obj.get()))
            f.write('\n')

            PERSON_ID += 1

        f.close()
        print(f"{bcolors.OKGREEN}Файл успешно создан{bcolors.ENDC}\nИмя файла - {work_file}\n")

        time.sleep(5)


if __name__ == "__main__":
    main()