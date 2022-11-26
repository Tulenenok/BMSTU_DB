drop table public.persons_nifi;

create table if not exists public.persons_nifi(
      person_id serial primary key,
      name varchar(64),
      pat_name varchar(64),
      sub_name varchar(64),
      inp_date date,
      notes varchar(64)
);

------------------

drop table if exists nifi_log;

create table nifi_log(
     id Serial PRIMARY KEY,
     person_id INTEGER NOT NULL,
     event_type varchar(16) NOT NULL,
     event_date DATE NOT NULL,
     event_time TIME NOT NULL,
     FOREIGN KEY(person_id) REFERENCES persons_nifi(person_id)
);


create or replace function nifi_insert_trigger_proc() returns trigger AS $emp_stamp$
begin
    insert into nifi_log(person_id, event_type, event_date, event_time)
    values (new.person_id, 'INSERT', (select current_date), (SELECT current_time));
    RETURN new;
END;
$emp_stamp$ LANGUAGE plpgsql;

drop trigger if exists nifi_insert_trigger on persons_nifi;

create trigger nifi_insert_trigger
    after insert
    on persons_nifi
    for each row
execute procedure nifi_insert_trigger_proc();

insert into persons_nifi
VALUES(1, 'me', 'again', 'test', Null, Null);

select *
from persons_nifi
order by person_id;

select *
from nifi_log
order by  event_date, event_time;


-----------------------------


drop table if exists nifi_file_log;

create table if not exists nifi_file_log(
    id serial primary key,
    filename varchar(40) not null,
    load_time timestamp
);


create or replace function nifi_fl_insert_trigger_proc() returns trigger AS $emp_stamp$
begin
    update nifi_file_log
    set load_time = (select current_timestamp)
    where id = new.id;
    return new;
END;
$emp_stamp$ language plpgsql;

drop trigger if exists nifi_fl_insert_trigger on nifi_file_log;

create trigger nifi_fl_insert_trigger
    after insert
    on nifi_file_log
    for each row
execute procedure nifi_fl_insert_trigger_proc();

insert into nifi_file_log(filename)
values ('filename');

select * from nifi_file_log;