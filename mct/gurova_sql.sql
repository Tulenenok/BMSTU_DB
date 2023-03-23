-- РК 3
-- ЗАДАНИЕ 1

create table employee (
      id int not null primary key,
      fio varchar,
      birthdate date,
      department varchar
);

create table record(
       employee_id int references employee(id) not null,
       rdate date,
       dayweek varchar,
       rtime time,
       rtype int
);

insert into employee(
    id,
    fio,
    birthdate,
    department
) values
      (1, 'FIO1', '1995-09-25', 'IT'),
      (2, 'FIO2', '1999-09-30', 'IT'),
      (3, 'FIO3', '1990-09-25', 'Fin'),
      (4, 'FIO4', '1997-09-15', 'Fin'),
      (5, 'FIO5', '1995-09-25', 'IT'),
      (6, 'FIO6', '1999-09-30', 'IT'),
      (7, 'FIO7', '1990-09-25', 'Fin'),
      (8, 'FIO8', '1997-09-15', 'Fin'),
      (9, 'FIO9', '1990-09-25', 'Fin'),
      (10, 'FIO10', '1991-09-25', 'Fin'),
      (11, 'FIO11', '1992-09-22', 'Fin'),
      (12, 'FIO12', '1993-09-26', 'Fin'),
      (13, 'FIO13', '1994-09-25', 'Fin'),
      (14, 'FIO14', '1995-09-15', 'Fin'),
      (15, 'FIO15', '1996-09-24', 'Fin'),
      (16, 'FIO16', '1996-09-22', 'Fin'),
      (17, 'FIO17', '1994-05-25', 'Fin'),
      (18, 'FIO18', '1997-04-25', 'Fin');


select * from employee;

insert into record(
    employee_id,
    rdate,
    dayweek,
    rtime,
    rtype
) values
      (1, '2019-12-20', 'Понедельник', '09:01', 1),
      (1, '2019-12-20', 'Понедельник', '09:12', 2),
      (1, '2019-12-20', 'Понедельник', '09:40', 1),
      (1, '2019-12-20', 'Понедельник', '12:01', 2),
      (1, '2019-12-20', 'Понедельник', '13:40', 1),
      (1, '2019-12-20', 'Понедельник', '20:40', 2),

      (1, '2019-12-21', 'Понедельник', '09:01', 1),
      (1, '2019-12-21', 'Понедельник', '09:12', 2),
      (1, '2019-12-21', 'Понедельник', '09:40', 1),
      (1, '2019-12-21', 'Понедельник', '12:01', 2),
      (1, '2019-12-21', 'Понедельник', '13:40', 1),
      (1, '2019-12-21', 'Понедельник', '20:40', 2),

      (1, '2019-12-22', 'Понедельник', '09:01', 1),
      (1, '2019-12-22', 'Понедельник', '09:12', 2),
      (1, '2019-12-22', 'Понедельник', '09:40', 1),
      (1, '2019-12-22', 'Понедельник', '12:01', 2),
      (1, '2019-12-22', 'Понедельник', '13:40', 1),
      (1, '2019-12-22', 'Понедельник', '20:40', 2),


      (3, '2019-12-21', 'Понедельник', '09:01', 1),
      (3, '2019-12-21', 'Понедельник', '09:12', 2),
      (3, '2019-12-21', 'Понедельник', '09:40', 1),
      (3, '2019-12-21', 'Понедельник', '12:01', 2),
      (3, '2019-12-21', 'Понедельник', '13:40', 1),
      (3, '2019-12-21', 'Понедельник', '20:40', 2),

      (2, '2019-12-21', 'Понедельник', '08:51', 1),
      (2, '2019-12-21', 'Понедельник', '20:31', 2),

      (4, '2019-12-21', 'Понедельник', '09:51', 1),
      (4, '2019-12-21', 'Понедельник', '20:31', 2),

      (6, '2019-12-21', 'Понедельник', '09:51', 1),
      (6, '2019-12-21', 'Понедельник', '20:31', 2),

      (1, '2019-12-23', 'Среда', '09:11', 1),
      (1, '2019-12-23', 'Среда', '09:12', 2),
      (1, '2019-12-23', 'Среда', '09:40', 1),
      (1, '2019-12-23', 'Среда', '20:01', 2),

      (3, '2019-12-23', 'Среда', '09:01', 1),
      (3, '2019-12-23', 'Среда', '09:12', 2),
      (3, '2019-12-23', 'Среда', '09:50', 1),
      (3, '2019-12-23', 'Среда', '20:01', 2),

      (2, '2019-12-23', 'Среда', '08:41', 1),
      (2, '2019-12-23', 'Среда', '20:31', 2),

      (4, '2019-12-23', 'Среда', '09:51', 1),
      (4, '2019-12-23', 'Среда', '20:31', 2);


select * from record;


-- Написать функцию, возвращающую сотрудников, не пришедщих сегодня на работу.
-- Сегодня передается в качестве параметра.

create or replace function emp_that_not_come(check_day date)
    returns table(id int, fio varchar) as '
    with emp_in as
    (
        select employee_id
        from record
        where rdate = check_day and rtype = 1
    )
    select id, fio
    from employee
    where not exists(select 1 from emp_in where employee_id = id);
' language SQL;

select * from emp_that_not_come('2022-12-24');

insert into record
values (1, '2022-12-24', 'Суббота', '9:00', 1);

select * from emp_that_not_come('2022-12-24');

select * from emp_that_not_come('2019-12-23');



-- ЗАДАНИЕ 2
-- 1. Найти сотрудников, опаздавших сегодня меньше чем на 5 минут
select fio
from employee inner join record on id = employee_id
where rdate = '2019-12-21' and rtype = 1
group by id, fio
having min(rtime) < '09:05:00';


-- 2. Найти сотрудников, которые выходили больше чем на 10 минут
with t_2 as
(
    select employee_id,
           rtime as first_time,
           lag(rtime) over (partition by employee_id order by rtime) as second_time,
           rtype
    from record
    where rdate = '2019-12-23'
)
select employee_id, fio
from t_2, employee
where rtype = 1 and
      second_time is not null and
      first_time - second_time > cast('00:10:00' as time) and
      employee_id = id;


-- 3. Найти сотрудников бугалтерии, приходящих раньше 8 утра
-- Добавим записей про 8 утра
insert into record(
    employee_id,
    rdate,
    dayweek,
    rtime,
    rtype
) values
      (10, '2019-12-20', 'Понедельник', '09:02', 1),
      (11, '2019-12-20', 'Понедельник', '07:40', 1),
      (14, '2019-12-20', 'Понедельник', '09:00', 1),
      (10, '2019-12-20', 'Понедельник', '20:40', 2),

      (11, '2019-12-20', 'Понедельник', '18:00', 2),
      (14, '2019-12-20', 'Понедельник', '18:10', 2),
      (15, '2019-12-20', 'Понедельник', '07:55', 1),
      (15, '2019-12-20', 'Понедельник', '17:20', 2),
      (10, '2019-12-21', 'Вторник', '08:40', 1),
      (10, '2019-12-21', 'Вторник', '18:00', 2),

      (11, '2019-12-21', 'Вторник', '09:05', 1),
      (11, '2019-12-21', 'Вторник', '18:20', 2),
      (14, '2019-12-21', 'Вторник', '09:00', 1),
      (14, '2019-12-21', 'Вторник', '19:00', 2),
      (15, '2019-12-21', 'Вторник', '17:55', 2),

      (15, '2019-12-21', 'Вторник', '07:50', 1);


with t_3 as
(
    select employee_id, cast('08:00:00' AS time) as begin_time, min(rtime) as first_time
    from record
    where rdate = '2019-12-20'
    group by employee_id, cast('08:00:00' as time)
)
select employee_id, fio, department, first_time
from t_3, employee
where begin_time > first_time and employee_id = id and department = 'Fin';


-- Если не нужно было привязываться к дате 
select y.employee_id, y.rdate, e.fio, e.department, y.first_time
from 
    (
    select x.employee_id, x.rdate, 
            cast('08:00:00' AS time) as begin_time, 
            min(x.rtime) as first_time 
    from record x
    group by x.employee_id, x.rdate, cast('08:00:00' as time)
    ) y, employee e
where y.begin_time > y.first_time and y.employee_id = e.id and e.department = 'Fin'