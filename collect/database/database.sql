CREATE TABLE "Places" (
    "PlaceId"     serial primary key,
    "Name"        varchar(100) not null,
    "Website"     varchar(100) not null,
    "Address"     varchar(150) not null,
    "City"        varchar(40),
    "GooglePin"   varchar(27) not null,
    "CoordinateX" real not null,
    "CoordinateY" real not null,
    "Phone"       varchar(12)
);

CREATE TABLE "WorkingTime" (
    "TimeId"   serial primary key,
    "PlaceId"  int4 not null,
    "Days"     int not null,
    "OpenTime" varchar(17) not null
);

CREATE TABLE "Menus" (
    "MenuId"          serial primary key,
    "PlaceId"         int4 not null,
    "MenuLinkToFS"    varchar(100) not null,
    "DateMenuUpdated" timestamp not null
);
