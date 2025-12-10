#db tables columns lists
db_adres_schema = ['gml_id', 'miejscowosc', 'ulica', 'nr_porzadkowy']

db_transakcja_schema = ['id_rcn', 'rodzaj_transakcji', 'rodzaj_rynku', 'strona_sprzedajaca', 'strona_kupujaca', 
                        'cena_transakcji', 'data_sporzadzenia_dokumentu', 'rodzaj_prawa_wlasnosci', 
                        'udzial_w_nieruchomosci', 'pole_powierzchni_gruntowej', 'cena_nieruchomosci', 'rodzaj_nieruchomosci']
db_dzialka_schema = ['id_rcn', 'pole_powierzchni_ewidencyjnej', 'cena_dzialki_ewidencyjnej', 'dodatkowe_informacje']
db_budynek_schema = ['id_rcn', 'rodzaj_budynku', 'powierzchnia_uzytkowa', 'cena_budynku', 'dodatkowe_informacje']
db_lokal_schema = ['id_rcn', 'funkcja_lokalu', 'liczba_izb', 'nr_kondygnacji', 'powierzchnia_uzytkowa_lokalu',
                   'powierzchnia_uzytkowa_pomieszczen_przynal', 'cena_lokalu', 'dodatkowe_informacje']
db_identyfikator_schema = ['gml_id', 'id_transakcji', 'id_dzialki', 'id_budynku', 'id_lokalu', 'id_adresu']

layers_config = {
    'adres':{
        'type': 'simple',
        'source_df': 'RCN_Adres',
        'rename': {'numerPorzadkowy': 'nr_porzadkowy'},
        'subset': ['gml_id', 'miejscowosc', 'ulica', 'numerPorzadkowy'],
        'target_schema': db_adres_schema
    },
    'transakcja': {
        'type': 'joined_3',
        'layer_names': ['RCN_Transakcja', 'RCN_Dokument', 'RCN_Nieruchomosc'], 
        'rename': {
            'lokalnyId': 'id_rcn',
            'rodzajTransakcji': 'rodzaj_transakcji',
            'rodzajRynku': 'rodzaj_rynku',
            'stronaSprzedajaca': 'strona_sprzedajaca',
            'stronaKupujaca': 'strona_kupujaca',
            'cenaTransakcjiBrutto': 'cena_transakcji',
            
            # Kolumny z połączonych warstw (Dokument, Nieruchomość)
            'dataSporzadzeniaDokumentu': 'data_sporzadzenia_dokumentu',
            'rodzajPrawaDoNieruchomosci': 'rodzaj_prawa_wlasnosci',
            'udzialWPrawieDoNieruchomosci': 'udzial_w_nieruchomosci',
            'polePowierzchniNieruchomosciGruntowej': 'pole_powierzchni_gruntowej',
            'cenaNieruchomosciBrutto': 'cena_nieruchomosci',
            'rodzajNieruchomosci': 'rodzaj_nieruchomosci'
        },
        'subset': [
            'lokalnyId',
            'rodzajTransakcji',
            'rodzajRynku',
            'stronaSprzedajaca',
            'stronaKupujaca',
            'cenaTransakcjiBrutto', 
            'dataSporzadzeniaDokumentu',
            'rodzajPrawaDoNieruchomosci',
            'udzialWPrawieDoNieruchomosci'
        ],
        'target_schema': db_transakcja_schema
    },
    'dzialka': {
        'type': 'simple',
        'source_df': 'RCN_Dzialka',
        'rename': {
            'idDzialki': 'id_rcn',
            'polePowierzchniEwidencyjnej': 'pole_powierzchni_ewidencyjnej',
            'sposobUzytkowania': 'sposob_uzytkowania',
            'cenaDzialkiEwidencyjnejBrutto': 'cena_dzialki_ewidencyjnej'
        },
        'subset': [
            'idDzialki', 
            'polePowierzchniEwidencyjnej'
        ],
        'target_schema': db_dzialka_schema
    },
    'budynek': {
        'type': 'simple',
        'source_df': 'RCN_Budynek',
        'rename': {
            'idBudynku': 'id_rcn',
            'rodzajBudynku': 'rodzaj_budynku',
            'cenaBudynkuBrutto': 'cena_budynku',
            'powierzchniaUzytkowaBudynku': 'powierzchnia_uzytkowa'
        },
        'subset': [
            'idBudynku', 
            'rodzajBudynku', 
        ],
        'target_schema': db_budynek_schema        
    },
    'lokal': {
        'type': 'simple',
        'source_df': 'RCN_Lokal',
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
            'idLokalu', 
            'funkcjaLokalu', 
            'liczbaIzb', 
            'nrKondygnacji', 
            'powUzytkowaLokalu'
        ],
        'target_schema': db_lokal_schema
    },
    'identyfikator': {
        'type': 'joined_4',
        'layer_names': [], # Nie używamy layer_names w joined_4, bo czytamy XML, ale pole musi być
        'rename': {
            # Tutaj mapowanie nie jest potrzebne, bo w kodzie Pythona (krok 2)
            # stworzyliśmy od razu poprawne nazwy kolumn:
            # 'id_transakcji', 'id_dzialki', 'id_budynku', 'id_lokalu'
        },
        'subset': ['gml_id'],
        'target_schema': db_identyfikator_schema
    }
}

