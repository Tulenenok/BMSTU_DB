-- 1. Инструкция SELECT, использующая предикат сравнения.
select distinct title
from lab_1.building_materials
where price > 100
order by title;

-- 2. Инструкция SELECT, использующая предикат BETWEEN.
select order_id
from lab_1.order_detail
where quant between 10 and 20;

-- 3. Инструкция SELECT, использующая предикат LIKE
select distinct name, sub_name, pat_name
from lab_1.persons
where name like 'И%';

-- 4. Инструкция SELECT, использующая предикат IN с вложенным подзапросом.
select order_id, order_date
from lab_1.orders
where person_id in (
    select person_id
    from lab_1.persons
    where sub_name like 'Иван'
);

-- 5. Инструкция SELECT, использующая предикат EXISTS с вложенным подзапросом.
select bm.mat_id, title, material, price, whs_id, total
from lab_1.building_materials bm, lab_1.wh_stocks wh1
where exists (
    select 1
    from lab_1.wh_stocks wh2
    where wh1.whs_id = wh2.whs_id and bm.mat_id = wh2.mat_id and total < 10
);

-- 6.Инструкция SELECT, использующая предикат сравнения с квантором.
select order_id, order_date, price, shipment_price, person_id
from lab_1.orders
where price > ALL (
    select price
    from lab_1.orders
    where shipment_price = 0
);

-- 7. Инструкция SELECT, использующая агрегатные функции в выражениях столбцов.
select max(price) as max_price, min(price) as min_price
from lab_1.orders
where shipment_price = 0
group by shipment_price;

-- 8. Инструкция SELECT, использующая скалярные подзапросы в выражениях столбцов.
select
    order_id,
    shipment_price,
    (
    select max(shipment_price) from lab_1.orders
    ) as max_sh_price,
    (
    select min(shipment_price) as min_sh_price from lab_1.orders
    ) as min_sh_price,
    person_id
from lab_1.orders;

-- 9. Инструкция SELECT, использующая простое выражение CASE.
select
    name,
    sub_name,
    case name
         when 'Иванов' then 'Наш человек'
         when 'Петров' then 'Мутный товарищ'
         else 'Надо уволить'
    end
    as result
from lab_1.persons;

-- 10. Инструкция SELECT, использующая поисковое выражение CASE
select
    mat_id,
    material,
    case
        when min_quant < 10 then 'Маловато будет'
        when min_quant < 30 then 'Ну норм'
        else 'Милота!'
    end
from lab_1.building_materials
limit 20;

-- 11. Создание новой временной локальной таблицы из результирующего набора данных инструкции SELECT. 
select mat_id, title, material
into bm_copy
from lab_1.building_materials
where price > 100 and min_quant > 10;
select * from bm_copy;

-- 12. Инструкция SELECT, использующая вложенные коррелированные подзапросы в качестве производных таблиц в предложении FROM.
select name, sub_name
from lab_1.persons
where sub_name like '%Иван%' and name not like '%Иван%'

union

select name, sub_name
from lab_1.persons
where name like '%Иван%' and sub_name not like '%Иван%'
order by name;

-- 12. Инструкция SELECT, использующая вложенные коррелированные подзапросы в качестве производных таблиц в предложении FROM.
select person_id, name, sub_name, pat_name, cnt
from lab_1.persons ps inner join (
    select
        person_id,
        count(order_id) as cnt
    from lab_1.orders
    group by person_id
) as person_count_orders using (person_id)
order by person_id

-- 13. Инструкция SELECT, использующая вложенные подзапросы с уровнем вложенности 3.
select mat_id, material, price
from lab_1.building_materials
where price > 200 and mat_id in (
    select mat_id
    from lab_1.order_detail
    where order_id in (
        select order_id
        from lab_1.orders
        where price - shipment_price < 100
        )
    group by mat_id
    having sum(quant) > 50
    )
order by price DESC;

-- 14. Инструкция SELECT, консолидирующая данные с помощью предложения GROUP BY, но без предложения HAVING.
select
    material,
    min(price) as min_price,
    max(price) as max_price,
    avg(price) as avg_price
from lab_1.building_materials
group by material
order by material, min_pri;

-- 15. Инструкция SELECT, консолидирующая данные с помощью предложения GROUP BY и предложения HAVING.
select order_id, min(quant) as min_quant
from lab_1.order_detail
group by order_id
having min(quant) > 40;

-- 16. Однострочная инструкция INSERT, выполняющая вставку в таблицу одной строки значений.
insert into lab_1.persons (name, sub_name, pat_name, inp_date)
values ('Бурых', 'Наталия', 'Николаевна', '2022-10-01');

-- 17. Многострочная инструкция INSERT, выполняющая вставку в таблицу результирующего набора данных вложенного подзапроса.
insert into lab_1.wh_stocks(whs_date, whs_no, mat_id, total, inp_date)
select
    '2022-01-10',
    floor(random() * 20),
    (select min(mat_id) from lab_1.building_materials),
    (select max(total) from lab_1.wh_stocks),
    '2022-01-10';
    
-- 18. Простая инструкция UPDATE.
update lab_1.persons
set pat_name = 'Михайловна'
where name = 'Бурых' and sub_name = 'Наталия';

-- 19. Инструкция UPDATE со скалярным подзапросом в предложении SET.
update lab_1.wh_stocks
set mat_id = (select max(mat_id) from lab_1.building_materials)
where whs_id = 25627;

-- 20. Простая инструкция DELETE
delete from lab_1.wh_stocks
where  whs_id = 25627;

-- 21. Инструкция DELETE с вложенным коррелированным подзапросом в предложении WHERE.
delete from lab_1.orders
where person_id in (
    select person_id
    from lab_1.persons
    where name = 'Бурых'
);

-- 22. Инструкция SELECT, использующая простое обобщенное табличное выражение
with person_ivan as
(
    select person_id, name, sub_name, pat_name
    from lab_1.persons
    where name = 'Иван%' or sub_name = 'Иван'
)
select name, sub_name, pat_name, count(order_id) as cnt_orders
from person_ivan p left join lab_1.orders o on p.person_id = o.person_id
group by name, sub_name, pat_name;

-- 23. Инструкция SELECT, использующая рекурсивное обобщенное табличное
-- выражение.
with recursive pr(n) as
(
    select 10
    union all
    select n + 1 from pr
    where n < 20
)
select n from pr;


-- 24. Оконные функции. Использование конструкций MIN/MAX/AVG OVER()
select distinct
    material,
    avg(price) over(partition by material) as avg_price,
    min(price) over(partition by material) as min_price,
    max(price) over(partition by material) as max_price
from lab_1.building_materials;

-- 25. Оконные фукции для устранения дублей
create table tmp_table (
    field_1 int2,
    field_2 int4
);

insert into public.tmp_table(field_1, field_2)
values (1, 1);
insert into public.tmp_table(field_1, field_2)
values (1, 1);
insert into public.tmp_table(field_1, field_2)
values (2, 2);
insert into public.tmp_table(field_1, field_2)
values (2, 2);
insert into public.tmp_table(field_1, field_2)
values (2, 2);
insert into public.tmp_table(field_1, field_2)
values (3, 3);
insert into public.tmp_table(field_1, field_2)
values (3, 1);

select * from public.tmp_table;

create table tmp_table_2 as
    (with cle as
              (select row_number() over (partition by field_1, field_2) as r_n,
                      field_1,
                      field_2
               from tmp_table)
     select *
     from cle
     where r_n = 1);

drop table public.tmp_table;
select * from public.tmp_table_2;


