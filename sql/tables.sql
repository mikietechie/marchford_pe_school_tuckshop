CREATE TABLE IF NOT EXISTS "users" (
    "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
    "password" varchar(128) NOT NULL,
    "username" varchar(150) NOT NULL UNIQUE
);
CREATE TABLE IF NOT EXISTS "products" (
    "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
    "name" varchar(150) NOT NULL UNIQUE,
    "price" float NOT NULL,
    "qty" integer NOT NULL
);
CREATE TABLE IF NOT EXISTS "sales" (
    "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
    "timestamp" datetime NOT NULL,
    "customer" varchar(150) NOT NULL,
    "cashier" varchar(150) NOT NULL,
    "total" float NOT NULL
);
CREATE TABLE IF NOT EXISTS "sale_items" (
    "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
    "unit_price" float NOT NULL,
    "qty" integer NOT NULL,
    "total" float NOT NULL,
    "product_id" bigint NOT NULL REFERENCES "products" ("id") DEFERRABLE INITIALLY DEFERRED,
    "sale_id" bigint NOT NULL REFERENCES "sales" ("id") DEFERRABLE INITIALLY DEFERRED
);
CREATE TABLE IF NOT EXISTS "purchases" (
    "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
    "unit_price" float NOT NULL,
    "qty" integer NOT NULL,
    "total" float NOT NULL,
    "product_id" bigint NOT NULL REFERENCES "products" ("id") DEFERRABLE INITIALLY DEFERRED
);