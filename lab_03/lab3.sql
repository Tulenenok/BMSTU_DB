-- ФУНКЦИИ

-- Скалярная функция
-- Количество заказов, закрепленное за человеком с именем ...
create or replace function count_orders(name varchar(64),
                                        sub_name varchar(64),
                                        pat_name varchar(64))
returns integer as '
    select count(order_id)
    from lab_1.orders o inner join lab_1.persons p using(person_id)
    where p.sub_name like $2 and p.name like $1 and p.pat_name like $3
' language SQL;

select public.count_orders('Иванов', 'Василий', 'Васильевич');

-- Подставляемая табличная функция
-- Сколько каждого материала осталось на скдаде с номером ...  на дату
create or replace function count_material_on_stock_by_date(stock_no int, stock_date date)
returns table (mat_id int4, count_mat int4) as
'
    select
        wh.mat_id as mat_id, sum(wh.total) as count_mat
    from lab_1.wh_stocks wh inner join lab_1.building_materials bm using (mat_id)
    where wh.whs_no = $1 and wh.whs_date = $2
    group by wh.mat_id
    order by wh.mat_id, count_mat
' language SQL;

select * from public.count_material_on_stock_by_date(4, '2022-10-23');

-- Многооператорная табличная функция
-- Вывести все отгрузки такого то исполнителя или с такой-то ценой
create or replace function shipments_filter_person_date_price(p_id int,
                                                              min_price int,
                                                              max_price int)
returns table (
                  shipment_id int4,
                  shipment_date date,
                  mat_id int4,
                  quant int2,
                  price int4,
                  name varchar(64)
              ) as
'
    begin
        RETURN QUERY
            select o.shipment_id, o.shipment_date, o.mat_id, o.quant, o.price, p.name
            from lab_1.order_shipments o inner join lab_1.persons p using (person_id)
            where o.price > $2 and o.price < $3;

        RETURN QUERY
            select o.shipment_id, o.shipment_date, o.mat_id, o.quant, o.price, p.name
            from lab_1.order_shipments o inner join lab_1.persons p using (person_id)
            where o.person_id = $1;
    end;
' language plpgsql;

select * from public.shipments_filter_person_date_price(3023, 10, 800);

-- Рекурсивная функция
-- Числа Фибоначи
create or replace function fib(first int, second int, max int)
    returns table (x int) as
'
    begin
        return QUERY
            select first;
        if second <= max then
            return QUERY
                select *
                from fib(second, first + second, max);
        end if;
    end
' language plpgsql;

select * from fib(1,1, 13);

-- Вывести всех людей с id c .. по ..
create or replace function filter_persons_by_id(start_id int4, end_id int4)
    returns table(p_id int4,
                  name varchar(64),
                  sub_name varchar(64),
                  pat_name varchar(64)) as
'
    begin
        return QUERY
            select o.person_id, o.name, o.sub_name, o.pat_name
            from lab_1.persons o
            where o.person_id = start_id;

        if start_id < end_id then
            return QUERY
                select * from filter_persons_by_id(start_id + 1, end_id);
        end if;
    end;
' language plpgsql;

select * from public.filter_persons_by_id(3002, 3010);

-- Получить даты с по
create or replace function get_dates(date_from date, date_to date)
    returns table (tdate date)
    language plpgsql
as $$
begin
    return query select date_from;
    if date_from < date_to then
        return query select * from get_dates(date_from + 1, date_to);
    end if;
end $$;

select * from public.get_dates('2022-09-01', '2022-10-31');


-- ПРОЦЕДУРЫ

-- Хранимая процедура c параметрами
-- Поменять номер склада по его id
create or replace procedure change_no_stocks(w_id int4, new_no int4) as
'
    update lab_1.wh_stocks
    set whs_no = new_no
    where whs_id = w_id
' language sql;

call public.change_no_stocks(446, 10);

select * from lab_1.wh_stocks where whs_id = 446;

-- Хранимая процедура без параметров
-- Поменять всем товарам с кодом 22099043 минимальное количество на 40
create or replace procedure change_min_quant() as
'
    update lab_1.building_materials
    set min_quant = 40
    where cast(code as int) = 525643912
' language sql;

call public.change_min_quant();

select min_quant from lab_1.building_materials where code = '525643912';

-- Рекурсивную хранимую процедуру или хранимую процедур с рекурсивным ОТВ
-- Числа Фибоначчи
create or replace procedure fib_index
(
    res inout int,
    index int,
    _start int default 1,
    _end int default 1
)
as '
    begin
        if index > 0 then
            res = _start + _end;
            call fib_index(res, index - 1, _end, _start + _end);
        END IF;
    end;
' language plpgsql;

CALL fib_index(1, 5);

-- Вычисление факториала
create or replace procedure get_factorial(n in int, fact inout int default 1)
as '
    declare
        res int;
    begin
        if n = 0 then
            fact = 1;
        else
            call get_factorial(n - 1, res);
            fact = n * res;
        end if;
    end;
' language plpgsql;

call get_factorial(4);

-- Хранимая процедура с курсором
-- Получить id заказов на заданную дату
create or replace procedure order_list (order_d date, lst out refcursor)
as '
    begin
        open lst for select * from lab_1.orders where order_date = order_d;
    end;
' language plpgsql;


drop table public.test_data;
create table public.test_data (
    k INTEGER
) ;

do $$
    declare
        lst refcursor;

        x lab_1.orders%rowtype;
    begin
        call order_list('2022-10-25', lst);
        fetch lst into x;
        loop
            insert into test_data (k) values (x.order_id);
            fetch lst into x;
            exit when not found;
        end loop;
        commit;
    end $$;

select * from public.test_data;

-- Хранимая процедура доступа к метаданным
-- Существует ли столбец с таким названием в таблице
create or replace procedure is_exist_col (
    tab_name in varchar,
    col_name in varchar,
    res out int
)
    language plpgsql
as $$
begin
    select coalesce(sum(1), 0) into res from information_schema.columns x
    where x.table_schema = 'lab_1' and
            lower(x.table_name) = lower(tab_name) and
            lower(x.column_name) = lower(col_name);
end $$;

call public.is_exist_col('order_detail', 'order_date', 2);
call public.is_exist_col('order_detail', 'id', 2);


-- ТРИГГЕРЫ
/* BEFORE */
-- При удалении заказа удалить все связанные с ним записи из других таблиц
create or replace function before_order_delete() returns trigger as $tr_bd_orders$
begin
    delete from lab_1.order_shipments x where x.order_id = old.order_id;
    delete from lab_1.order_detail y where y.order_id = old.order_id;
    return old;
end;
$tr_bd_orders$ language plpgsql;

create trigger tr_bd_orders before delete on lab_1.orders
for each row execute procedure before_order_delete();

select count(*) from lab_1.order_detail where order_id = 9;

delete from lab_1.orders
where order_id = 9;

/* AFTER */
-- После вставки новой позиции в заказ пересчитать стоимость заказа
create or replace function after_order_detail_insert() returns trigger as $tr_ai_order_detail$
begin
    update lab_1.orders x set price = x.price + new.price * new.quant where x.order_id = new.order_id;
    return null;
end;
$tr_ai_order_detail$ language plpgsql;

create trigger tr_ai_order_detail after insert on lab_1.order_detail
for each row execute procedure after_order_detail_insert();

insert into lab_1.order_detail(order_id, mat_id, quant, price, inp_date)
values (7, 43, 15, 1000, '2022-10-28');


/* INSTEAD OF */
-- Не удалять человека из базы, а помечать его как удаленного
alter table lab_1.persons add column notes varchar(64);

create view test_persons as
select *
from lab_1.persons;

create or replace function del_per()
    returns trigger
as '
    begin
        update public.test_persons
        set notes = ''del''
        where test_persons.person_id = old.person_id;
        return new;
    end;
' language plpgsql;

create trigger del_persons instead of delete on public.test_persons
for each row execute procedure del_per();

delete from public.test_persons t
where t.person_id = 3001;
