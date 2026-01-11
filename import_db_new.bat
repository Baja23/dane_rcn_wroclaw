@echo off
setlocal

echo Parametr: "%~1"
pause

:: --- KONFIGURACJA ---
set CONTAINER_NAME=analiza_cen_rcn_wroclaw_db
set DB_USER=Tycjan
set DB_NAME=rcn_wroclaw
set CONTAINER_TMP=/tmp/import.sql
:: --------------------

if "%~1"=="" (
    echo.
    echo [BLAD] Nie wybrano pliku!
    echo Prosze przeciagnac plik .sql na ikone tego skryptu.
    pause
    exit /b 1
)

echo.
echo ========================================================
echo   Importowanie do bazy: %DB_NAME%
echo   Plik: %~nx1
echo ========================================================
echo.

:: --- KROK 1: KOPIA SQL DO KONTENERA ---
echo [1/3] Kopiuje plik SQL do kontenera...

docker cp "%~1" %CONTAINER_NAME%:%CONTAINER_TMP%
if errorlevel 1 (
    echo [BLAD] Nie udalo sie skopiowac pliku do kontenera.
    pause
    exit /b 1
)

:: --- KROK 2: SPRAWDZENIE / UTWORZENIE BAZY ---
echo.
echo [2/3] Sprawdzam czy baza istnieje...

docker exec %CONTAINER_NAME% psql -U %DB_USER% -d postgres -tc ^
 "SELECT 1 FROM pg_database WHERE datname='%DB_NAME%';" | findstr 1 >nul

if errorlevel 1 (
    echo       Tworze baze danych: %DB_NAME%
    docker exec %CONTAINER_NAME% psql -U %DB_USER% -d postgres -c ^
     "CREATE DATABASE %DB_NAME%;"
) else (
    echo       Baza %DB_NAME% juz istnieje.
)

:: --- KROK 3: IMPORT SQL (LINUX, UTF-8 SAFE) ---
echo.
echo [3/3] Importuje dane (bezpieczny UTF-8)...

docker exec -i %CONTAINER_NAME% psql -X -v ON_ERROR_STOP=1 ^
  -U %DB_USER% -d %DB_NAME% -f %CONTAINER_TMP%

if errorlevel 1 (
    echo.
    echo [BLAD] Import zakonczony bledem.
    pause
    exit /b 1
)

echo.
echo [OK] Import zakonczony poprawnie
pause
