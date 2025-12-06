@echo off
:: --- KONFIGURACJA ---
:: Wpisz tutaj nazwę swojego kontenera (sprawdź w docker ps)
set CONTAINER_NAME=projekt-db-1
:: Wpisz użytkownika bazy
set DB_USER=myuser
:: Wpisz nazwę bazy danych
set DB_NAME=mydatabase
:: --------------------

:: Pobieranie aktualnej daty do nazwy pliku (Format RRRR-MM-DD)
set CUR_YYYY=%date:~-4,4%
set CUR_MM=%date:~-7,2%
set CUR_DD=%date:~-10,2%
set FILENAME=backup_%CUR_YYYY%-%CUR_MM%-%CUR_DD%.sql

echo.
echo ========================================================
echo   Tworzenie kopii zapasowej bazy: %DB_NAME%
echo   Z kontenera: %CONTAINER_NAME%
echo   Plik wyjsciowy: %FILENAME%
echo ========================================================
echo.

:: Wykonanie zrzutu (z flagami -O -x dla latwego udostepniania)
docker exec -t %CONTAINER_NAME% pg_dump -U %DB_USER% -d %DB_NAME% -O -x --clean --if-exists > %FILENAME%

if %ERRORLEVEL% equ 0 (
    echo.
    echo [SUKCES] Backup zostal utworzony pomyslnie!
) else (
    echo.
    echo [BLAD] Cos poszlo nie tak. Sprawdz czy kontener dziala.
)

:: Czeka na klawisz, zeby okno nie zniknelo od razu
pause