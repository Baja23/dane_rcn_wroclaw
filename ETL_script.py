import geopandas as gpd
from sqlalchemy import create_engine, URL
from dotenv import load_dotenv
import os

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

def get_layer(selected_layer):
    gdf_layer  = gpd.read_file('Dane/wroclaw_rcn.gml', layer=selected_layer)
    return gdf_layer

def join_3_gdf_layers(transakcja_layer, dokument_layer, nieruchomosc_layer):
    gdf_transakcja_table = transakcja_layer.merge(dokument_layer, on='gml_id').merge(nieruchomosc_layer, on='gml_id')
    return gdf_transakcja_table 

#def transform_Load(layers_config, db_table_schema, gml_path, engine):


def main():
    load_dotenv()
    db_host = os.getenv('DB_HOST')
    db_port = os.getenv('DB_PORT')
    db_user = os.getenv('DB_USER')
    db_password = os.getenv('DB_PASSWORD')
    db_name = os.getenv('DB_NAME')
    engine = db_connection_engine(db_host, db_port, db_user, db_password, db_name)

    transakcja_layer = get_layer('RCN_Transakcja')
    dokument_layer = get_layer('RCN_Dokument')
    nieruchomosc_layer = get_layer('RCN_Nieruchomosc')
    dzialka_layer = get_layer('RCN_Dzialka')
    budynek_layer = get_layer('RCN_Budynek')
    lokal_layer = get_layer('RCN_Lokal')
    adres_layer = get_layer('RCN_Adres')

    transakcja_joined_layer = join_3_gdf_layers(transakcja_layer, dokument_layer, nieruchomosc_layer)

if __name__ == "__main__":
    main()