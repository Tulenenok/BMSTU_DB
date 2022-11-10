/*
 * Лабораторная работа №5
 * Использование XML/JSON с базами данных
 */


/* --------------------- ЗАДАНИЕ № 1, 2 (считать в json и записать из него) --------------------- */

-- Тестим как работает json
select row_to_json(o) result from lab_1.order_detail o;

-- Сохраняем таблицы в файлы
copy
(
    select row_to_json(od) result from lab_1.order_detail od
)
to '/users/gurovana/documents/scripts/lab_05/order_details.json';

copy
(
    select row_to_json(o) result from lab_1.orders o
) to '/users/gurovana/documents/scripts/lab_05/orders.json';

copy
(
    select row_to_json(p) result from lab_1.persons p
) to '/users/gurovana/documents/scripts/lab_05/persons.json';

-- Создам новую схему, чтобы в нее положить копии таблиц
create schema if not exists lab_5;

-- Создаю таблицы, в которые буду восстанавливать данные из json
create table if not exists lab_5.orders(
   ORDER_ID             SERIAL               not null,
   ORDER_DATE           DATE                 not null,
   ORDER_NO             INT4                 not null,
   ORDER_STATE          INT2                 not null,
   SHIPMENT_DATE        DATE                 null,
   PRICE                INT4                 null,
   SHIPMENT_PRICE       INT4                 null,
   NOTE                 VARCHAR(2000)        null,
   INP_DATE             DATE                 null
);

create table if not exists lab_5.order_details(
  ID                   SERIAL               not null,
  ORDER_ID             INT4                 not null,
  MAT_ID               INT4                 not null,
  QUANT                INT2                 not null,
  PRICE                INT4                 not null,
  INP_DATE             DATE                 null
);

create table if not exists lab_5.persons(
    PERSON_ID            SERIAL               not null,
    NAME                 VARCHAR(64)          not null,
    SUB_NAME             VARCHAR(64)          not null,
    PAT_NAME             VARCHAR(64)          not null,
    INP_DATE             CHAR(10)             null
);

-- Будем записывать в json через промежуточную таблицу
create table if not exists lab_5.orders_import(doc json);
copy lab_5.orders_import from '/users/gurovana/documents/scripts/lab_05/orders.json';
select * from lab_5.orders_import;

create table if not exists lab_5.od_imports(doc json);
copy lab_5.od_imports from '/users/gurovana/documents/scripts/lab_05/order_details.json';
select * from lab_5.od_imports;

create table if not exists lab_5.p_imports(doc json);
copy lab_5.p_imports from '/users/gurovana/documents/scripts/lab_05/persons.json';
select * from lab_5.p_imports;

-- Теперь считаем результаты в основные таблицы
insert into lab_5.persons(person_id, name, sub_name, pat_name, inp_date)
select
    cast(doc ->> 'person_id' as int),
    doc ->> 'name',
    doc ->> 'sub_name',
    doc ->> 'pat_name',
    doc ->> 'inp_date'
from lab_5.p_imports;

insert into lab_5.order_details(id, order_id, mat_id, quant, price, inp_date)
select
    cast(doc ->> 'id' as int),
    cast(doc ->> 'order_id' as int),
    cast(doc ->> 'mat_id' as int),
    cast(doc ->> 'quant' as int),
    cast(doc ->> 'price' as int),
    cast(doc ->> 'inp_date' as date)
from lab_5.od_imports;

insert into lab_5.orders(order_id, order_date, order_no, order_state, shipment_date,
                         price, shipment_price, note, inp_date)
select
    cast(doc ->> 'order_id' as int),
    cast(doc ->> 'order_date' as date),
    cast(doc ->> 'order_no' as int),
    cast(doc ->> 'order_state' as smallint),
    cast(doc ->> 'shipment_date'as date),
    cast(doc ->> 'price' as int),
    cast(doc ->> 'shipment_price'as int),
    doc ->> 'note',
    cast(doc ->> 'inp_date' as date)
from lab_5.orders_import;

-- Проверяем, что все добавилось
select * from lab_5.orders;
select * from lab_5.order_details;
select * from lab_5.persons;

-- Выставляем primary key для таблиц
alter table lab_5.orders add primary key (order_id);
alter table lab_5.order_details add primary key (id);
alter table lab_5.persons add primary key (person_id);

-- Удаляем промежуточные таблицы
drop table if exists lab_5.p_imports;
drop table if exists lab_5.od_imports;
drop table if exists lab_5.orders_import;

-- drop table if exists lab_5.persons;
-- drop table if exists lab_5.orders;
-- drop table if exists lab_5.order_details;


/* ---------------------------------------------------------------------------------------------- */

