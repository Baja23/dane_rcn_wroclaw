Baza danych RCN Wrocław

1. Stwórz własny plik .env o poniższym schemacie, gdzie w miejsce gwiazdek podasz dowolne: nazwę użytkownika, hasło (najlepiej bez znaków specjalnych), localhost lub 127.0.0.1, wolny port(np. 5432) oraz nazwę bazy danych
    DB_USER=*****
    DB_PASSWORD=****
    DB_HOST=localhost/127.0.0.1
    DB_PORT=****
    DB_NAME=******
2. Zainstaluj i włącz Docker Desktop
3. W terminalu (np. w VS Code) wpisz docker-compose up -d i wciśnij enter, Docker wykorzysta dane podane w pliku .env i stworzy na ich podstawie nową bazę danych
4. W terminalu uruchom pip install -r requirements.txt aby zainstalować wszystkie potrzebne biblioteki do uruchomienia skryptów
5. Aby stworzyć puste tabele oraz dodać dane do tabel enumerations uruchom notatnik db_creation.ipynb
6. Za pomocą notatnika cleaning_data.ipynb przejrzyj dane pod kątem pustych i zduplikowanych wartości. 
7. Aby załadować dane do pustych tabel uruchom ETL_script.py
8. Dodatkowo dodane zostały skrypty do dumpowania oraz importowania bazy danych za pomocą Dockera
9. Aby zdumpować bazę danych wpisz do skryptu db_dumping.bat swoją nazwę użytkownika, kontener oraz nazwę bazy danych i uruchom skrypt
10. Aby zaimportować bazę danych, musisz mieć w niej stworzone konto; 
    stwórz analogiczny kontener na innym komputerze i do skryptu import_db_new.bat wpisz swoją nazwę użytkownika, kontener oraz nazwę bazy danych i uruchom skrypt poprzez przeciągnięcie backupu bazy danych na skrypt