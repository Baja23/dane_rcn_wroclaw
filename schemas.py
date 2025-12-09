from ETL_script import transakcja_joined_layer, adres_layer, dzialka_layer, budynek_layer, lokal_layer, id_joined_layer
#db tables columns lists
db_adres_schema = ['miejscowosc', 'ulica', 'nr_porzadkowy']

db_transakcja_schema = ['id_rcn', 'rodzaj_transakcji', 'rodzaj_rynku', 'strona_sprzedajaca', 'strona_kupujaca', 
                        'cena_transakcji', 'data_sporzadzenia_dokumentu', 'rodzaj_prawa_wlasnosci', 
                        'udzial_wlasnosci_nieruchomosci', 'pole_powierzchni_gruntowej', 'cena_nieruchomosci', 'rodzaj_nieruchomosci']
db_dzialka_schema = ['id_rcn', 'adres_id', 'pole_powierzchni_ewidencyjnej', 'cena_dzialki_ewidencyjnej', 'dodatkowe_informacje']
db_budynek_schema = ['id_rcn', 'adres_id', 'rodzaj_budynku', 'powierzchnia_uzytkowa', 'cena_budynku', 'dodatkowe_informacje']
db_lokal_schema = ['id_rcn', 'adres_id', 'funkcja_lokalu', 'liczba_izb', 'nr_kondygnacji', 'powierzchnia_uzytkowa_lokalu',
                   'powierzchnia_uzytkowa_pomieszczen_przynal', 'cena_lokalu', 'dodatkowe_informacje']
db_identyfikator_schema = ['gml_id', 'id_transakcji', 'id_dzialki', 'id_budynku', 'id_lokalu']

layers_config = {
    'adres':{
        'source_df': adres_layer,
        'rename': {'numerPorzadkowy': 'nr_porzadkowy'},
        'subset': ['miejscowosc', 'ulica', 'nr_porzadkowy']
    },
    'transakcja': {
        'source_df': transakcja_joined_layer,
        'rename': {
            'lokalnyId': 'id_rcn',
            'rodzajTransakcji': 'rodzaj_transakcji',
            'rodzajRynku': 'rodzaj_rynku',
            'stronaSprzedajaca': 'strona_sprzedajaca',
            'stronaKupujaca': 'strona_kupujaca',
            'cenaTransakcjiBrutto': 'cena_transakcji',
            'dataSporzadzeniaDokumentu': 'data_sporzadzenia_dokumentu',
            'rodzajPrawaDoNieruchomosci': 'rodzaj_prawa_wlasnosci',
            'udzialWPrawieDoNieruchomosci': 'udzial_w_nieruchomosci',
            'polePowierzchniNieruchomosciGruntowej': 'pole_powierzchni_gruntowej',
            'cenaNieruchomosciBrutto': 'cena_nieruchomosci',
            'rodzajNieruchomosci': 'rodzaj_nieruchomosci'
        },
        'subset': [
            'id_rcn', 
            'rodzaj_transakcji', 
            'rodzaj_rynku', 
            'strona_sprzedajaca', 
            'strona_kupujaca', 
            'cena_transakcji', 
            'data_sporzadzenia_dokumentu', 
            'rodzaj_prawa_wlasnosci', 
            'udzial_w_nieruchomosci', 
            'cena_nieruchomosci', 
            'rodzaj_nieruchomosci'
        ]
    },
    'dzialka': {
        'source_df': dzialka_layer,
        'rename': {
            'idDzialki': 'id_rcn',
            'polePowierzchniEwidencyjnej': 'pole_powierzchni_ewidencyjnej',
            'sposobUzytkowania': 'sposob_uzytkowania',
            'cenaDzialkiEwidencyjnejBrutto': 'cena_dzialki_ewidencyjnej'
        },
        'subset': [
            'id_rcn', 
            'adres_id', 
            'pole_powierzchni_ewidencyjnej', 
            'sposob_uzytkowania'
        ]
    },
    'budynek': {
        'source_df': budynek_layer,
        'rename': {
            'idBudynku': 'id_rcn',
            'rodzajBudynku': 'rodzaj_budynku',
            'cenaBudynkuBrutto': 'cena_budynku',
            'powierzchniaUzytkowaBudynku': 'powierzchnia_uzytkowa'
        },
        'subset': [
            'id_rcn', 
            'adres_id', 
            'rodzaj_budynku', 
            'powierzchnia_uzytkowa'
        ]        
    },
    'lokal': {
        'source_df': lokal_layer,
        'rename': {
            'idLokalu': 'id_rcn', 
            'funkcjaLokalu': 'funkcja_lokalu', 
            'liczbaIzb': 'liczba_izb', 
            'nrKondygnacji': 'nr_kondygnacji', 
            'powUzytkowaLokalu': 'powierzchnia_uzytkowa_lokalu',  
            'powUzytkowaPomieszczenPrzynal': 'powierzchnia_uzytkowa_pomieszczen_przynal', 
            'cenaLokaluBrutto': 'cena_lokalu', 
            'dodatkoweInformacje': 'dodatkowe_informacje'
        },
        'subset': [
            'id_rcn', 
            'adres_id', 
            'funkcja_lokalu', 
            'liczba_izb', 
            'nr_kondygnacji', 
            'powierzchnia_uzytkowa_lokalu'
        ]
    },
    'identyfikator': {
        'source_df': id_joined_layer,
        'rename': {'lokalnyId': 'id_transakcji', 'idDzialki': 'id_dzialki', 'idBudynku': 'id_budynku', 'idLokalu': 'id_lokalu'},
        'subset': ['gml_id', 'id_transakcji']
    }
}

