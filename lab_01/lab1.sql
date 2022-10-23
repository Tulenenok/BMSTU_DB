CREATE DATABASE "lab-1" WITH OWNER = postgres ENCODING = 'UTF8' TABLESPACE = pg_default TEMPLATE = postgres;

/*==============================================================*/
/* Table: BUILDING_MATERIALS                                    */
/*==============================================================*/
create table BUILDING_MATERIALS (
   MAT_ID               SERIAL               not null,
   CODE                 VARCHAR(32)          not null,
   TITLE                VARCHAR(250)         not null,
   MATERIAL             VARCHAR(64)          not null,
   PRICE                INT4                 not null,
   MIN_QUANT            INT2                 null,
   IS_DELETED           VARCHAR(1)           null,
   INP_DATE             DATE                 null,
   constraint PK_BUILDING_MATERIALS primary key (MAT_ID)
);

/*==============================================================*/
/* Index: IDX0_BUILDING_MATERIAL                                */
/*==============================================================*/
create unique index IDX0_BUILDING_MATERIAL on BUILDING_MATERIALS (
CODE
);

/*==============================================================*/
/* Table: ORDERS                                                */
/*==============================================================*/
create table ORDERS (
   ORDER_ID             SERIAL               not null,
   ORDER_DATE           DATE                 not null,
   ORDER_NO             INT4                 not null,
   ORDER_STATE          INT2                 not null,
   SHIPMENT_DATE        DATE                 null,
   PRICE                INT4                 null,
   SHIPMENT_PRICE       INT4                 null,
   NOTE                 VARCHAR(2000)        null,
   INP_DATE             DATE                 null,
   constraint PK_ORDERS primary key (ORDER_ID)
);

/*==============================================================*/
/* Table: ORDER_DETAIL                                          */
/*==============================================================*/
create table ORDER_DETAIL (
   ID                   SERIAL               not null,
   ORDER_ID             INT4                 not null,
   MAT_ID               INT4                 not null,
   QUANT                INT2                 not null,
   PRICE                INT4                 not null,
   INP_DATE             DATE                 null,
   constraint PK_ORDER_DETAIL primary key (ID)
);

/*==============================================================*/
/* Table: ORDER_SHIPMENTS                                       */
/*==============================================================*/
create table ORDER_SHIPMENTS (
   SHIPMENT_ID          SERIAL               not null,
   ORDER_ID             INT4                 not null,
   MAT_ID               INT4                 not null,
   WHS_NO               INT2                 not null,
   SHIPMENT_DATE        DATE                 not null,
   QUANT                INT2                 not null,
   PRICE                INT4                 not null,
   INP_DATE             DATE                 null,
   constraint PK_ORDER_SHIPMENTS primary key (SHIPMENT_ID)
);

/*==============================================================*/
/* Table: WH_STOCKS                                             */
/*==============================================================*/
create table WH_STOCKS (
   WHS_ID               SERIAL               not null,
   WHS_DATE             DATE                 not null,
   WHS_NO               INT2                 not null,
   MAT_ID               INT4                 not null,
   TOTAL                INT4                 not null,
   INP_DATE             DATE                 null,
   constraint PK_WH_STOCKS primary key (WHS_ID)
);

alter table ORDER_DETAIL
   add constraint FK_MATERIAL_IN_ORDER foreign key (MAT_ID)
      references BUILDING_MATERIALS (MAT_ID)
      on delete restrict on update restrict;

alter table ORDER_DETAIL
   add constraint FK_ORDER_OF_DETAILS foreign key (ORDER_ID)
      references ORDERS (ORDER_ID)
      on delete restrict on update restrict;

alter table ORDER_SHIPMENTS
   add constraint FK_MATERIAL_IN_SHIPMENT foreign key (MAT_ID)
      references BUILDING_MATERIALS (MAT_ID)
      on delete restrict on update restrict;

alter table ORDER_SHIPMENTS
   add constraint FK_ORDER_OF_SHIPMENT foreign key (ORDER_ID)
      references ORDERS (ORDER_ID)
      on delete restrict on update restrict;

alter table WH_STOCKS
   add constraint FK_MATERIAL_ON_WHAREHOUSE foreign key (MAT_ID)
      references BUILDING_MATERIALS (MAT_ID)
      on delete restrict on update restrict;
