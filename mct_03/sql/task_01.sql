-- ЗАДАНИЕ 1
-- Найти отделы, в которых хоть один сотрудник опаздывает больше 3-х раз в неделю

-- Как найти неделю (но это правда не точно)
select extract(week from rdate) as week
from record;

-- Как найти сотрудников, которые опаздали в конкретный день
select rdate, employee_id
from record
where rtype = 1
group by rdate, employee_id
having min(rtime) > '09:30:00';


-- Как найти сотрудников, опаздывающих более 3-х раз в неделю
-- (ради теста стоит больше 1)
with date_emp as
(
    select rdate, employee_id
    from record
    where rtype = 1
    group by rdate, employee_id
    having min(rtime) > '09:30:00'
)
select distinct employee_id
from date_emp
group by extract(week from rdate), employee_id
having count(rdate) >= 1;


-- Остается добавить сюда отделы
with lox_emp as (
    with date_emp as
             (
                 select rdate, employee_id
                 from record
                 where rtype = 1
                 group by rdate, employee_id
                 having min(rtime) > '09:30:00'
             )
    select distinct employee_id
    from date_emp
    group by extract(week from rdate), employee_id
    having count(rdate) >= 1
)
select department
from lox_emp l inner join employee e on l.employee_id = e.id


