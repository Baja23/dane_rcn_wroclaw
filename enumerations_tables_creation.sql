CREATE TABLE rodzaj_transakcji(
    id INT PRIMARY KEY,
    nazwa  VARCHAR(255) NOT NULL
    );

CREATE TABLE rodzaj_rynku(
    id INT PRIMARY KEY,
    nazwa  VARCHAR(255) NOT NULL
    );

CREATE TABLE strona_transakcji(
    id INT PRIMARY KEY,
    nazwa  VARCHAR(255) NOT NULL
    );

CREATE TABLE rodzaj_prawa_wlasnosci(
    id INT PRIMARY KEY,
    nazwa  VARCHAR(255) NOT NULL
    );

CREATE TABLE rodzaj_nieruchomosci(
    id INT PRIMARY KEY,
    nazwa  VARCHAR(255) NOT NULL
    );

CREATE TABLE rodzaj_budynku(
    id INT PRIMARY KEY,
    nazwa  VARCHAR(255) NOT NULL
    );

CREATE TABLE funkcja_lokalu(
    id INT PRIMARY KEY,
    nazwa  VARCHAR(255) NOT NULL
    );

CREATE TABLE sposob_uzytkowania(
    id INT PRIMARY KEY,
    nazwa  VARCHAR(255) NOT NULL
    );