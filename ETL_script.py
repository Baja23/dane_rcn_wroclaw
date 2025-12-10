import geopandas as gpd
import pandas as pd
from sqlalchemy import create_engine, URL, text
from dotenv import load_dotenv
import os
from schemas import layers_config
import xml.etree.ElementTree as ET

#function that returns engine connection
def db_connection_engine(db_host, db_port, db_user, db_password, db_name):
    connection_url = URL.create(
    "postgresql+psycopg2",
    username=db_user,
    password=db_password,
    host=db_host,
    port=db_port,
    database=db_name,
    )
    engine = create_engine(connection_url)
    return engine

def extract_transaction_links(gml_path):
    """
    Ręcznie wyciąga relacje xlink:href z warstwy RCN_Transakcja,
    które GeoPandas pomija.
    """
    tree = ET.parse(gml_path)
    root = tree.getroot()
    
    # Mapowanie przestrzeni nazw (Namespace) - to konieczne w XML
    # Jeśli to nie zadziała, spróbujemy bardziej elastycznej metody, ale zazwyczaj RCN ma te:
    ns = {
        'rcn': 'http://www.geoportal.gov.pl/rcn',  # Przykładowy namespace, skrypt spróbuje go znaleźć
        'gml': 'http://www.opengis.net/gml/3.2',
        'xlink': 'http://www.w3.org/1999/xlink'
    }
    
    # Lista na wyniki
    data = []

    # Iterujemy po wszystkich elementach, niezależnie od namespace (bezpieczniej)
    # Szukamy tagów kończących się na 'RCN_Transakcja'
    for element in root.iter():
        if element.tag.endswith('RCN_Transakcja'):
            
            # 1. Pobierz ID Transakcji (gml:id)
            # Atrybuty w xml.etree mają pełne nazwy z klamrami {url}
            gml_id = None
            for k, v in element.attrib.items():
                if k.endswith('id'): # Szukamy gml:id
                    gml_id = v
                    break
            
            if not gml_id: continue

            # 2. Szukamy linku do Dokumentu (podstawaPrawna)
            doc_id = None
            for child in element:
                if child.tag.endswith('podstawaPrawna'):
                    # Szukamy atrybutu href
                    for k, v in child.attrib.items():
                        if k.endswith('href'):
                            doc_id = v
                            break
            
            # 3. Szukamy linku do Nieruchomości (nieruchomosc)
            nier_id = None
            for child in element:
                if child.tag.endswith('nieruchomosc'):
                    for k, v in child.attrib.items():
                        if k.endswith('href'):
                            nier_id = v
                            break
            
            data.append({
                'gml_id': gml_id,
                'ref_dokument_id': doc_id,
                'ref_nieruchomosc_id': nier_id
            })
            
    return pd.DataFrame(data)

def extract_complex_relations(gml_path):
    """
    Kompleksowy parser relacji RCN.
    1. Buduje mapę ID: Techniczne -> Biznesowe.
    2. Buduje mapę Adresów: Obiekt -> GML_ID Adresu.
    3. Zwraca połączone relacje: Transakcja -> Obiekt -> Adres.
    """
    tree = ET.parse(gml_path)
    root = tree.getroot()
    
    # Słowniki pomocnicze
    id_map = {}        # { 'GUID_Obiektu': '146501_1.0001...' }
    obj_to_addr = {}   # { 'GUID_Obiektu': 'GUID_Adresu' }
    
    print("     * Indeksowanie obiektów i adresów w XML...")

    # --- PRZEBIEG 1: Budowanie map (Działki, Budynki, Lokale) ---
    for element in root.iter():
        # Sprawdzamy czy to obiekt, który nas interesuje
        is_object = False
        tag_type = None
        
        if element.tag.endswith('RCN_Dzialka'):
            is_object = True; tag_type = 'dzialka'
        elif element.tag.endswith('RCN_Budynek'):
            is_object = True; tag_type = 'budynek'
        elif element.tag.endswith('RCN_Lokal'):
            is_object = True; tag_type = 'lokal'
            
        if not is_object: continue

        # 1. Pobieramy GML ID (Klucz techniczny)
        gml_id = None
        for k, v in element.attrib.items():
            if k.endswith('id'):
                gml_id = v
                break
        
        if not gml_id: continue
        clean_gml = gml_id.strip()

        # 2. Pobieramy ID Biznesowe (z tagów wewnętrznych)
        # Np. <idDzialki>, <idBudynku>
        biz_id = None
        target_tag = 'idDzialki' if tag_type == 'dzialka' else ('idBudynku' if tag_type == 'budynek' else 'idLokalu')
        
        for child in element.iter():
            if child.tag.endswith(target_tag) and child.text:
                biz_id = child.text.strip()
                break
        
        if biz_id:
            id_map[clean_gml] = biz_id

        # 3. Szukamy powiązania z ADRESEM
        # Szukamy tagu, który ma 'adres' w nazwie i atrybut href
        addr_ref = None
        for child in element:
            if 'adres' in child.tag.lower(): # Np. <rcn:adres> lub <adresNieruchomosci>
                for k, v in child.attrib.items():
                    if k.endswith('href'):
                        addr_ref = v
                        break
            if addr_ref: break
        
        if addr_ref:
            # Zapisujemy link do adresu (usuwamy hash #)
            obj_to_addr[clean_gml] = addr_ref.lstrip('#').strip()


    # --- PRZEBIEG 2: Budowanie głównej ścieżki (Transakcja -> Nieruchomość -> Obiekty) ---
    
    trans_to_nier = []
    nier_to_objects = []

    for element in root.iter():
        # A. Transakcja
        if element.tag.endswith('RCN_Transakcja'):
            full_id = None
            for k, v in element.attrib.items():
                if k.endswith('id'): full_id = v; break
            
            match_id = None
            for child in element.iter():
                if child.tag.endswith('lokalnyId'): match_id = child.text; break
            
            if not match_id and full_id: match_id = full_id

            nier_ref = None
            for child in element:
                if child.tag.endswith('nieruchomosc'):
                    for k, v in child.attrib.items():
                        if k.endswith('href'): nier_ref = v; break
            
            if full_id and nier_ref:
                trans_to_nier.append({
                    'trans_full_id': full_id.strip(),
                    'trans_match_id': match_id.strip(),
                    'ref_nier_id': nier_ref.strip()
                })

        # B. Nieruchomość -> Obiekty
        elif element.tag.endswith('RCN_Nieruchomosc'):
            nier_id = None
            for k, v in element.attrib.items():
                if k.endswith('id'): nier_id = v; break
            
            if not nier_id: continue

            for child in element:
                raw_ref = None
                for k, v in child.attrib.items():
                    if k.endswith('href'): raw_ref = v; break
                
                if raw_ref:
                    clean_ref = raw_ref.lstrip('#').strip()
                    
                    # Tłumaczymy na ID Biznesowe (z mapy z kroku 1)
                    final_obj_id = id_map.get(clean_ref, clean_ref)
                    # Wyciągamy ID Adresu (z mapy adresów z kroku 1)
                    final_addr_id = obj_to_addr.get(clean_ref, None)

                    obj_type = None
                    if child.tag.endswith('dzialka'): obj_type = 'dzialka'
                    elif child.tag.endswith('budynek'): obj_type = 'budynek'
                    elif child.tag.endswith('lokal'): obj_type = 'lokal'

                    if obj_type:
                        nier_to_objects.append({
                            'ref_nier_id': nier_id.strip(),
                            'type': obj_type,
                            'obj_ref': final_obj_id,   # ID do złączenia z tabelą obiektów (dzialka)
                            'addr_ref': final_addr_id  # ID do złączenia z tabelą adres
                        })

    # Tworzenie DataFrame i łączenie
    df_trans = pd.DataFrame(trans_to_nier)
    df_objs = pd.DataFrame(nier_to_objects)

    if df_trans.empty or df_objs.empty:
        return pd.DataFrame()

    # Łączymy: Transakcja + (Nieruchomość) + Obiekt (z Adresem)
    full_map = df_trans.merge(df_objs, on='ref_nier_id', how='inner')
    
    return full_map

def main():
    gml_path = 'Dane/wroclaw_rcn.gml'
    load_dotenv()
    db_host = os.getenv('DB_HOST')
    db_port = os.getenv('DB_PORT')
    db_user = os.getenv('DB_USER')
    db_password = os.getenv('DB_PASSWORD')
    db_name = os.getenv('DB_NAME')
    engine = db_connection_engine(db_host, db_port, db_user, db_password, db_name)

    for layer_name, config in layers_config.items():
        print(f"Przetwarzam warstwę: {layer_name}.")
        if config['type'] == 'simple':
            gdf = gpd.read_file(gml_path, layer=config['source_df'])
            # --- POPRAWKA: Wyciągamy gml_id z indeksu ---
            if 'gml_id' not in gdf.columns:
                    gdf.reset_index(inplace=True)
                    if 'index' in gdf.columns:
                        gdf.rename(columns={'index': 'gml_id'}, inplace=True)
                
            # Upewniamy się, że kolumna nazywa się gml_id (czasem jest 'id')
            if 'gml_id' not in gdf.columns and 'id' in gdf.columns:
                     gdf.rename(columns={'id': 'gml_id'}, inplace=True)
                
            # Czyścimy spacje (ważne!)
            if 'gml_id' in gdf.columns:
                    gdf['gml_id'] = gdf['gml_id'].astype(str).str.strip()
        elif config['type'] == 'joined_3':
                print(f"   - Łączenie warstw: {config['layer_names']}")
                
                # 1. Wczytujemy standardowe warstwy GeoPandas
                layers = {}
                for name in config['layer_names']:
                    print(f"     * Czytam: {name}")
                    layers[name] = gpd.read_file(gml_path, layer=name)

                # 2. MAGICZNY KROK: Wyciągamy brakujące linki z XML
                print("     * Wydobywanie ukrytych relacji z XML...")
                links_df = extract_transaction_links(gml_path)
                
                # 3. Przygotowanie danych do łączenia
                
                # A. Transakcje (Główna)
                # Doklejamy do niej nasze wydobyte linki (po gml_id)
                transakcja_full = layers['RCN_Transakcja'].merge(links_df, on='gml_id', how='left')
                
                # B. Dokumenty
                # Musimy mieć pewność, że gml_id to kolumna
                if 'gml_id' not in layers['RCN_Dokument'].columns:
                     layers['RCN_Dokument'].reset_index(inplace=True) # Czasem jest w indeksie
                     layers['RCN_Dokument'].rename(columns={'index': 'gml_id'}, inplace=True)
                
                # C. Nieruchomości
                if 'gml_id' not in layers['RCN_Nieruchomosc'].columns:
                     layers['RCN_Nieruchomosc'].reset_index(inplace=True)
                     layers['RCN_Nieruchomosc'].rename(columns={'index': 'gml_id'}, inplace=True)

                # 4. FINALNE ŁĄCZENIE (MERGE)
                # Teraz łączymy: Transakcja -> Dokument (po ref_dokument_id) -> Nieruchomosc (po ref_nieruchomosc_id)
                
                print("     * Scalanie tabel...")
                gdf = transakcja_full.merge(
                    layers['RCN_Dokument'], 
                    left_on='ref_dokument_id', # Kolumna z naszych linków
                    right_on='gml_id',         # Kolumna ID w dokumencie
                    suffixes=('', '_dok')      # Żeby nie dublować nazw kolumn
                ).merge(
                    layers['RCN_Nieruchomosc'],
                    left_on='ref_nieruchomosc_id', # Kolumna z naszych linków
                    right_on='gml_id',             # Kolumna ID w nieruchomości
                    suffixes=('', '_nier')
                )
        elif config['type'] == 'joined_4':
                print(f"   - Tworzenie tabeli łączącej (Identyfikator)...")
                
                relations_df = extract_complex_relations(gml_path)
                
                if relations_df.empty:
                    print("   ⚠️ Nie znaleziono relacji. Pomijam.")
                    continue

                print(f"     * Znaleziono {len(relations_df)} powiązań. Tłumaczenie i insert SQL...")

                temp_table_name = 'temp_links_gml'
                
                # Przygotowujemy dane do wysyłki (dodajemy kolumnę ADRESU)
                df_to_upload = pd.DataFrame({
                    'trans_full': relations_df['trans_full_id'],
                    'trans_match': relations_df['trans_match_id'],
                    'obj_gml': relations_df['obj_ref'],   # To jest ID biznesowe obiektu
                    'obj_type': relations_df['type'],
                    'addr_gml': relations_df['addr_ref']  # To jest GML_ID adresu
                })
                
                df_to_upload.to_sql(temp_table_name, con=engine, if_exists='replace', index=False)
                
                # ZAPYTANIE SQL - Teraz uwzględnia też JOIN do tabeli adres
                sql_translate_and_insert = text(f"""
                    INSERT INTO identyfikator (gml_id, id_transakcji, id_dzialki, id_budynku, id_lokalu, id_adresu)
                    SELECT 
                        temp.trans_full,
                        t.id,
                        d.id,
                        b.id,
                        l.id,
                        a.id  -- Pobieramy ID adresu
                    FROM {temp_table_name} temp
                    -- Join Transakcji
                    JOIN transakcja t ON temp.trans_match = t.id_rcn
                    -- Join Obiektów (po ID biznesowym)
                    LEFT JOIN dzialka d ON temp.obj_gml = d.id_rcn AND temp.obj_type = 'dzialka'
                    LEFT JOIN budynek b ON temp.obj_gml = b.id_rcn AND temp.obj_type = 'budynek'
                    LEFT JOIN lokal l ON temp.obj_gml = l.id_rcn AND temp.obj_type = 'lokal'
                    -- Join Adresu (po GML_ID, bo tak wczytaliśmy tabelę 'adres' w trybie simple)
                    LEFT JOIN adres a ON temp.addr_gml = a.gml_id;
                """)
                
                with engine.begin() as conn:
                    conn.execute(sql_translate_and_insert)
                    conn.execute(text(f"DROP TABLE {temp_table_name}"))
                
                print(f"   ✅ Sukces! Tabela 'identyfikator' wypełniona kompletem danych (Transakcja + Obiekt + Adres).")
                continue
        #dropping rows with null values in key columns (definied in schemas.py)
        initial_count = len(gdf)
        gdf_clean = gdf.dropna(subset=config['subset'])
        dropped_count = initial_count - len(gdf_clean)
        print(f"   - Usunięto {dropped_count} wierszy z brakami w: {config['subset']}")

        gdf_renamed = gdf_clean.rename(columns=config['rename'])
        gdf_renamed = gdf_renamed.reindex(columns=config['target_schema'])

        gdf_renamed.to_sql(layer_name, con=engine, if_exists='append', index=False)
        print(f"Sukces! {len(gdf_renamed)} wierszy trafiło do tabeli '{layer_name}'.")

    print("\nKoniec procesu ETL.")


if __name__ == "__main__":
    main()