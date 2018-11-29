CREATE TABLE "Places" (
    "PlaceId"   serial PRIMARY key,
    "Name"      VARCHAR(100) NOT NULL,
    "Address"   varchar(150) NOT NULL,
    "City"      varchar(40),
    "GooglePin" varchar(27) NOT NULL,
    "CoordinateX" REAL NOT NULL,
    "CoordinateY" REAL NOT NULL,
    "Website"     varchar(100) NOT NULL,
    "Phone"       varchar(12)
);

CREATE TABLE "WorkingTime" (
    "TimeId" serial PRIMARY key,
    "PlaceId" INT4 NOT NULL,
    "Days" INT NOT NULL,
    "OpenTime" varchar(17) NOT NULL
);
