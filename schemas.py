from ETL_script import transakcja_joined_layer, adres_layer, dzialka_layer, budynek_layer, lokal_layer
#db tables columns lists
db_adres_schema = ['miejscowosc', 'ulica', 'nr_porzadkowy']

db_transakcja_schema = ['id_rcn', 'rodzaj_transakcji', 'rodzaj_rynku', 'strona_sprzedajaca', 'strona_kupujaca', 
                        'cena_transakcji', 'data_sporzadzenia_dokumentu', 'rodzaj_prawa_wlasnosci', 
                        'udzial_wlasnosci_nieruchomosci', 'pole_powierzchni_gruntowej', 'cena_nieruchomosci', 'rodzaj_nieruchomosci'
                        ]
db_dzialka_schema = ['id_rcn', 'adres_id', 'pole_powierzchni_ewidencyjnej', 'cena_dzialki_ewidencyjnej', 'dodatkowe_informacje']
db_budynek_schema = ['id_rcn', 'adres_id', 'rodzaj_budynku', 'powierzchnia_uzytkowa', 'cena_budynku', 'dodatkowe_informacje']
db_lokal_schema = ['id_rcn', 'adres_id', 'funkcja_lokalu', 'liczba_izb', 'nr_kondygnacji', 'powierzchnia_uzytkowa_lokalu',
                   'powierzchnia_uzytkowa_pomieszczen_przynal', 'cena_lokalu', 'dodatkowe_informacje']

layers_config = {
    'adres':{
        'source_df': adres_layer,
        'rename': {'numerPorzadkowy': 'nr_porzadkowy'},
        'subset': ['miejscowosc', 'ulica', 'nr_porzadkowy']
    },
    'transakcja': {
        'source_df': transakcja_joined_layer,
        'rename': {},
        'subset': []
    },
    'dzialka': {
        'source_df': dzialka_layer,
        'rename': {},
        'subset': []
    },
    'budynek': {
        'source_df': budynek_layer,
        'rename': {},
        'subset': []        
    },
    'lokal': {
        'source_df': lokal_layer,
        'rename': {},
        'subset': []
    }
}

#finish layers config and decide on the final design of the database

