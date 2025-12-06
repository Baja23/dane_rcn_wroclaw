CREATE TABLE adres(
    id INT GENERATED AS IDENTITY PRIMARY KEY,
    miejscowosc VARCHAR(255) NOT NULL,
    ulica VARCHAR(255) NOT NULL,
    nr_porzadkowy VARCHAR(255) NOT NULL
    );

CREATE TABLE transakcje(
    id VARCHAR(255) PRIMARY KEY,
    rodzaj_transakcji INT NOT NULL,
    rodzaj_rynku INT NOT NULL,
    strona_sprzedajaca INT NOT NULL,
    strona_kupujaca INT NOT NULL,
    cena_transakcji DECIMAL NOT NULL,
    data_sporzadzenia_dokumentu DATE NOT NULL,
    rodzaj_prawa_wlasnosci INT NOT NULL,
    udzial_w_nieruchomosci TEXT NOT NULL,
    pole_powierzchni_gruntowej NUMERIC,
    cena_nieruchomosci DECIMAL NOT NULL,
    FOREIGN KEY (rodzaj_transakcji) REFERENCES rodzaj_transakcji(id),
    FOREIGN KEY (rodzaj_rynku) REFERENCES rodzaj_rynku(id),
    FOREIGN KEY (strona_sprzedająca) REFERENCES strona_transakcji(id),
    FOREIGN KEY (strona_kupująca) REFERENCES strona_transakcji(id),
    FOREIGN KEY (rodzaj_prawa_wlasnosci) REFERENCES rodzaj_prawa_wlasnosci(id)
    );

CREATE TABLE dzialka(
    id VARCHAR(255) PRIMARY KEY,
    adres_id INT NOT NULL,
    pole_powierzchni NUMERIC NOT NULL,
    sposob_uzytkowania INT NOT NULL,
    cena_dzialki DECIMAL NOT NULL,
    dodatkowe_informacje TEXT,
    FOREIGN KEY (sposob_uzytkowania) REFERENCES sposob_uzytkowania(id),
    FOREIGN KEY (adres_id) REFERENCES adres(id)
    );

CREATE TABLE budynek(
    id VARCHAR(255) PRIMARY KEY,
    adres_id INT NOT NULL,
    rodzaj_budynku INT NOT NULL,
    powierzchnia_uzytkowa NUMERIC NOT NULL,
    cena_budynku DECIMAL,
    dodatkowe_informacje TEXT,
    FOREIGN KEY (rodzaj_budynku) REFERENCES rodzaj_budynku(id),
    FOREIGN KEY (adres_id) REFERENCES adres(id)
    );

CREATE TABLE lokal(
    id VARCHAR(255) PRIMARY KEY,
    adres_id INT NOT NULL,
    funkcja_lokalu INT NOT NULL,
    liczba_izb INT NOT NULL,
    nr_kondygnacji INT NOT NULL,
    powierzchnia_uzytkowa_lokalu NUMERIC NOT NULL,
    powierzchnia_uzytkowa_pomieszczen_przynal NUMERIC NOT NULL,
    cena_lokalu DECIMAL NOT NULL,
    dodatkowe_informacje TEXT,
    FOREIGN KEY (adres_id) REFERENCES adres(id),
    FOREIGN KEY (funkcja_lokalu) REFERENCES funkcja_lokalu(id)
    );

    CREATE TABLE identyfikatory(
    gml_id VARCHAR(255) PRIMARY KEY,
    id_transakcji VARCHAR(255) NOT NULL,
    id_dzialki VARCHAR(255),
    id_budynku VARCHAR(255),
    id_lokalu VARCHAR(255),
    FOREIGN KEY (id_transakcji) REFERENCES transakcja(id),
    FOREIGN KEY (id_dzialki) REFERENCES dzialka(id),
    FOREIGN KEY (id_budynku) REFERENCES budynek(id),
    FOREIGN KEY (id_lokalu) REFERENCES lokal(id)
    );