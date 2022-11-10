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


/*
 ЗАДАНИЕ №3

 Создать таблицу, в которой будет атрибут(-ы) с типом XML или JSON,
 или добавить атрибут с типом XML или JSON к уже существующей таблице.
 Заполнить атрибут правдоподобными данными с помощью команд INSERT или UPDATE.
 */

create table if not exists lab_5.persons_json(data json);

insert into lab_5.persons_json
select * from json_object('{person_id, name, sub_name, pat_name, inp_date, notes}',
                          '{1, "Хлеб", "Хлебов", "Хлебушкевич", null, null}'
);

select * from lab_5.persons_json;

-- Другой вариант
create table if not exists lab_5.person_json_2(
    id              serial       primary key,
    note            varchar(64)             ,
    important_data  json
);

insert into lab_5.person_json_2(note, important_data) values
('мяу', '{"pet": "кошка", "age": 5}'::json),
('гаф', '{"pet": "собака", "age": 10}'::json),
(null, '{"pet": "неизвестный объект", "age": 100}'::json);

select * from lab_5.person_json_2;

/* ------------------------------------------------------------------------------------ */


/* ------------------------------------ ЗАДАНИЕ №4 ------------------------------------ */
-- 4.1. Извлечь XML/JSON фрагмент из XML/JSON документа

create table if not exists lab_5.person_fragment(
    name     varchar(64),
    sub_name varchar(64)
);

create table if not exists lab_5.p_imports(doc json);
copy lab_5.p_imports from '/users/gurovana/documents/scripts/lab_05/persons.json';

select * from lab_5.p_imports,
             json_populate_record(NULL::lab_5.person_fragment, doc);

select doc ->> 'name' name from lab_5.p_imports;
select doc ->> 'sub_name' sub_name from lab_5.p_imports;

-- 4.2. Извлечь значения конкретных узлов или атрибутов XML/JSON документа
create table if not exists lab_5.pets(data json);

insert into lab_5.pets values
('{"id": 1, "params": {"type": "cat", "age": 5, "color": "orange"}}'::json),
('{"id": 2, "params": {"type": "dog", "age": 1, "color": "white"}}'::json),
('{"id": 3, "params": {"type": "parrot", "age": 2, "color": "blue"}}'::json),
('{"id": 4, "params": {"type": "parrot", "age": 0.5, "color": "green"}}'::json);

select * from lab_5.pets;

select data->'params'->'type' from lab_5.pets;

-- 4.3 Выполнить проверку существования узла или атрибута jsonb

--  jsonb -- данные хранятся в разложенном двоичном формате, что немного замедляет ввод
--  из-за дополнительных затрат на преобразование, но значительно ускоряет обработку,
--  поскольку повторная обработка не требуется. jsonb также поддерживается индексация,
--  что может быть существенным преимуществом.

create table if not exists lab_5.pets_b(data jsonb);

insert into lab_5.pets_b values
    ('{"id": 1, "params": {"type": "cat", "age": 5, "color": "orange"}}'::jsonb),
    ('{"id": 2, "params": {"type": "dog", "age": 1, "color": "white"}}'::jsonb),
    ('{"id": 3, "params": {"type": "parrot", "age": 2, "color": "blue"}}'::jsonb),
    ('{"id": 4, "params": {"type": "parrot", "age": 0.5, "color": "green"}}'::jsonb);

create or replace function is_key_exists(some_json jsonb, key text)
returns bool as '
    select some_json::jsonb ? key
' language sql;

select 1
from lab_5.pets_b
where cast(lab_5.pets_b.data -> 'id' as int) = 1;

with one_json as
(
    select lab_5.pets_b.data
    from lab_5.pets_b
    where cast(lab_5.pets_b.data -> 'id' as int) = 1
)
select is_key_exists((select * from one_json),'key_a');


-- 4.4 Изменить XML/JSON документ
create table if not exists lab_5.for_update(data jsonb);

insert into lab_5.for_update values
   ('{"id": 1, "type": "cat", "age": 5, "color": "orange"}'::jsonb),
   ('{"id": 2, "type": "dog", "age": 1, "color": "white"}'::jsonb);

update lab_5.for_update
set data = data || '{"age": 6}'::jsonb
where (data->'age')::int = 5;

select * from lab_5.for_update;


-- 4.5 Разделить XML/JSON документ на несколько строк по узлам
create table lab_5.last_test(doc json);

insert into lab_5.last_test values
('[{"id": 1, "type": "cat", "age": 5, "color": "orange"},
   {"id": 2, "type": "dog", "age": 1, "color": "white"}]');

-- Развернуть JSON-массив верхнего уровня в набор значений JSON.
select jsonb_array_elements(doc::jsonb) from lab_5.last_test;
select * from lab_5.last_test;

-- select * from json_array_elements('[1,true, [2,false]]');

/* ------------------------------------------------------------------------------------ */
