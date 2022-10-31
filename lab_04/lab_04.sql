/*
 * Лабораторная работа №4
 * SQL CLR
 */

select * from pg_language;

-- В pg_available_extensions перечислены расширения, доступные для установки.
select name, default_version, installed_version
from pg_available_extensions;

create extension plpython3u;

-- Определяемую пользователем скалярную функцию CLR
-- Вывести имя пользователя по его id
create or replace function get_name_person(id int)
returns varchar
as $$
    res = plpy.execute(f" \
        select name \
        from lab_1.persons \
        where person_id = {id};", 2
    )
    if res:
        return res[0]['name']
$$ language plpython3u;

select * from get_name_person(7);

-- Пользовательскую агрегатную функцию CLR
-- (агрегатные функции получают единственный результат из набора входных значений)
-- Вывести количество материалов с кодом
create or replace function count_materials_with_code(mat_code varchar)
returns int
as $$
    distinct_codes = plpy.execute(f"select code from lab_1.building_materials;")

    cnt = 0
    for i in distinct_codes:
        if i["code"] == mat_code:
            cnt += 1

    return cnt
$$ language plpython3u;

select * from count_materials_with_code('170488489');

-- Определяемую пользователем табличную функцию CLR
-- Вывести все заказы пользователя с id...
create or replace function orders_by_person(id int)
returns table (
    order_id int,
    order_date date,
    price int,
    person_id int
)
as $$
    buf = plpy.execute(f" \
        select order_id, order_date, price, person_id \
        from lab_1.persons inner join lab_1.orders using (person_id) \
    ")

    result = []
    for i in buf:
        if i["person_id"] == id:
            result.append(i)
    return result
$$ language plpython3u;

select * from orders_by_person(15);

-- Хранимую процедуру CLR
-- Поменять номер склада по его id
create or replace function change_no_stk(w_id int, new_no int)
returns void
as $$
    plan = plpy.prepare("update lab_1.wh_stocks set whs_no = $2 where whs_id = $1", ["int", "int"])
    plpy.execute(plan, [w_id, new_no])
$$ language plpython3u;

select * from change_no_stk(19028, 15);

-- Триггер CLR
-- Вместо удаления пользователя, пометим его как удаленного
alter table lab_1.persons add column notes varchar(64);

create view test_persons as
select *
from lab_1.persons;

-- drop trigger del_per_trigger on public.test_persons;

create or replace function del_p()
returns trigger
as $$
    del_id = TD["old"]["person_id"]
    plpy.execute(f" \
        update public.test_persons               \
        set notes = \'del\'                      \
        where test_persons.person_id = {del_id}; \
    ")
    return TD["new"]
$$ language plpython3u;

create trigger del_per_trigger
instead of delete on public.test_persons
for each row execute procedure del_p();

delete from public.test_persons t
where t.person_id = 2;

-- Определяемый пользователем тип данных CLR
-- Тип - заказ - общая стоимость
-- nrows - возвращает число строк, обработанных командой.
create type order_sum as
(
    order_id int,
    general_sum int
);

-- Функция подсчета общей стоимости
create or replace function get_general_sums(id int)
returns order_sum
as $$
    plan = plpy.prepare("                         \
        select order_id, sum(quant * price) s     \
        from lab_1.order_detail                   \
        where order_id = $1                       \
        group by order_id;", ["int"])

    run = plpy.execute(plan, [id])

    if (run.nrows()):
        return (run[0]["order_id"], run[0]["s"])
$$ language plpython3u;

select * from get_general_sums(5213);
