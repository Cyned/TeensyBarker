CREATE TABLE "Places" (
    "PlaceId"   serial PRIMARY key,
    "Name"      VARCHAR(100) NOT null,
    "Address"   varchar(150) NOT null,
    "City"      varchar(40),
    "GooglePin" varchar(27) NOT NULL,
    "CoordinateX" REAL NOT NULL,
    "CoordinateY" REAL NOT NULL,
    "Website"     varchar(100),
    "Phone"       varchar(12)
);

CREATE TABLE "WorkingTime" (
    "TimeId" serial PRIMARY key,
    "PlaceId" INT4 NOT null,
    "Days" INT NOT NULL,
    "OpenTime" varchar(17) NOT NULL
);
