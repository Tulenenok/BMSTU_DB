from peewee import *


DB_CONNECT = PostgresqlDatabase(
    database="lab_1",
    user="",
    password="",
    host="127.0.0.1",
    port="5432"
)


class BaseModel(Model):
    class Meta:
        database = DB_CONNECT


class Employee(BaseModel):
    id = IntegerField(column_name='id')
    fio = CharField(column_name='fio')
    birthdate = DateField(column_name='birthdate')
    department = CharField(column_name='department')

    class Meta:
        table_name = 'employee'


class Record(BaseModel):
    employee_id = ForeignKeyField(Employee, on_delete="cascade")
    rdate = DateField(column_name='rdate')
    dayweek = CharField(column_name='dayweek')
    rtime = TimeField(column_name='rtime')
    rtype = IntegerField(column_name='rtype')

    class Meta:
        table_name = 'record'