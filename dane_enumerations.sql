-- 1. Tabela: rodzaj_transakcji
-- Źródło: RCN_RodzajTransakcji
INSERT INTO rodzaj_transakcji (id, nazwa) VALUES
(1, 'wolnyRynek'),
(2, 'sprzedazBezprzetargowa'),
(3, 'sprzedazPrzetargowa'),
(4, 'sprzedazWPostepowaniuEgzekucyjnym'),
(5, 'sprzedazNaCelPubliczny'),
(6, 'sprzedazZBonifikata');

-- 2. Tabela: rodzaj_rynku
-- Źródło: RCN_RodzajRynku
INSERT INTO rodzaj_rynku (id, nazwa) VALUES
(1, 'rynekPierwotny'),
(2, 'rynekWtorny');

-- 3. Tabela: strona_transakcji
-- Źródło: RCN_StronaSprzedajacaKupujaca
INSERT INTO strona_transakcji (id, nazwa) VALUES
(1, 'skarbPanstwa'),
(2, 'jednostkaSamorzaduTerytorialnego'),
(3, 'osobaFizyczna'),
(4, 'osobaPrawna');

-- 4. Tabela: rodzaj_prawa_wlasnosci
-- Źródło: RCN_RodzajPrawa
INSERT INTO rodzaj_prawa_wlasnosci (id, nazwa) VALUES
(1, 'wlasnoscNieruchomosciGruntowej'),
(2, 'uzytkowanieWieczyste'),
(3, 'wlasnoscLokaluWrazZPrawemZwiazanym'),
(4, 'wlasnoscBudynkuWrazZPrawemZwiazanym');

-- 5. Tabela: rodzaj_nieruchomosci
-- Źródło: RCN_RodzajNieruchomosci
INSERT INTO rodzaj_nieruchomosci (id, nazwa) VALUES
(1, 'nieruchomoscGruntowaNiezabudowana'),
(2, 'nieruchomoscGruntowaZabudowana'),
(3, 'nieruchomoscBudynkowa'),
(4, 'nieruchomoscLokalowa');

-- 6. Tabela: rodzaj_budynku
-- Źródło: RCN_RodzajBudynku (UWAGA: ID zaczynają się od 101)
INSERT INTO rodzaj_budynku (id, nazwa) VALUES
(101, 'przemyslowy'),
(102, 'transportuILacznosci'),
(103, 'handlowoUslugowy'),
(104, 'zbiornikiSilosyMagazyny'),
(105, 'biurowy'),
(106, 'szpitale'),
(107, 'oswiatyISportu'),
(108, 'gospodarczy'),
(109, 'pozostaleNiemieszkalne'),
(110, 'mieszkalny');

-- 7. Tabela: funkcja_lokalu
-- Źródło: RCN_FunkcjaLokalu
INSERT INTO funkcja_lokalu (id, nazwa) VALUES
(1, 'mieszkalna'),
(2, 'handlowoUslugowa'),
(3, 'biurowa'),
(4, 'produkcyjna'),
(5, 'garaz'),
(6, 'inna');

-- 8. Tabela: sposob_uzytkowania
-- Źródło: RCN_SposobUzytkowania
INSERT INTO sposob_uzytkowania (id, nazwa) VALUES
(1, 'gruntyRolne'),
(2, 'gruntyLesne'),
(3, 'gruntyZabudowaneIZurbanizowane'),
(4, 'terenyKomunikacyjne'),
(5, 'inne');