-- ЗАДАНИЕ 2
-- Найти средний возраст сотрудников, не находящихся на рабочем месте 8 часов в день

-- учтем, что задание сформулировано мягко говоря отвратительно, и уточним его
-- во-первых будет <= 8 часов
-- во-вторых сделаем сводную таблицу "день - средний возраст"

-- сделаем сводную таблицу время прихода - время ухода
select rdate, employee_id, rtype, rtime, lead(rtime) over(partition by (rdate, employee_id) order by rtime)
from record;

-- найдем сколько каждый сотрудник провел времени за работой в каждый день
with emp_time as
(
    select rdate, employee_id, rtype,
           rtime as iin, lead(rtime) over(partition by (rdate, employee_id) order by rtime) as out
    from record
)
select rdate, employee_id, sum(extract(epoch from out - iin)) / 3600 as minuts
from emp_time
where rtype = 1
group by rdate, employee_id
order by rdate, employee_id;

-- сделаем сводную таблицу день - средний возраст работников, проработавших меньше 8 часов
with lox_table as
(
    with emp_time as
     (
         select rdate, employee_id, rtype,
                rtime as iin, lead(rtime) over(partition by (rdate, employee_id) order by rtime) as out
         from record
     )
    select rdate, employee_id, sum(extract(epoch from out - iin)) / 3600 as cnt_work_hours
    from emp_time
    where rtype = 1
    group by rdate, employee_id
)
select rdate, avg(date_part('year', age(birthdate))) as avg_agee
from lox_table inner join employee on lox_table.employee_id = employee.id
where cnt_work_hours < 10
group by rdate;
