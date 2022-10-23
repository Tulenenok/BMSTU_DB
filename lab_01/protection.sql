create table PERSONS (
   PERSON_ID            SERIAL               not null,
   NAME                 VARCHAR(64)          not null,
   SUB_NAME             VARCHAR(64)          not null,
   PAT_NAME             VARCHAR(64)          not null,
   INP_DATE             CHAR(10)             null,
   constraint PK_PERSONS primary key (PERSON_ID)
);


ALTER TABLE orders ADD COLUMN person_id INT4;
ALTER TABLE order_shipments ADD COLUMN person_id INT4;

ALTER TABLE orders ADD CONSTRAINT FK_PERSON_OF_ORDERS FOREIGN KEY (person_id) REFERENCES persons (person_id);
ALTER TABLE order_shipments ADD CONSTRAINT FK_PERSON_OF_SHIPMENT FOREIGN KEY (person_id) REFERENCES persons (person_id);