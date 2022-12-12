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


-- Написать функцию, возвращающую количество опаздавших сотрудников.
-- Дата опаздания передается в качестве параметра.

create or replace function count_emp(late_date date, late_time time)
    returns integer as '
    select count(*)
    from (
        select employee_id
        from record
        where rdate = late_date and rtype = 1
        group by employee_id, rtype
        having min(rtime) > late_time
    ) t_1;
' language SQL;

create or replace function check_count_emp(late_date date, late_time time)
    returns table(id int, cdate date, ctime time, ctype int) as '
        select employee_id, rdate, rtime, rtype
        from record
        where rdate = late_date and rtype = 1
        order by employee_id, rtime
' language SQL;

select * from count_emp('2019-12-20', '10:00');
select * from check_count_emp('2019-12-20', '10:00');