@echo off
setlocal EnableDelayedExpansion

:: --- KONFIGURACJA ---
set CONTAINER_NAME=projekt-db-1
set DB_USER=myuser
set DB_NAME=mydatabase
:: --------------------

echo.
echo ========================================================
echo   UNIWERSALNY IMPORT DO BAZY: %DB_NAME%
echo ========================================================
echo.

:: 1. SPRAWDZENIE CZY PLIK ZOSTAL PRZECIAGNIETY
if "%~1"=="" (
    color 0C
    echo [BLAD] Nie wybrano pliku!
    echo Prosze przeciagnac plik .sql na ikone tego skryptu.
    echo.
    pause
    exit /b
)

:: 2. SPRAWDZENIE CZY KONTENER DZIALA
docker ps | findstr "%CONTAINER_NAME%" >nul
if %errorlevel% neq 0 (
    color 0C
    echo [BLAD] Kontener '%CONTAINER_NAME%' nie dziala!
    echo Uruchom go komenda: docker-compose up -d
    echo.
    pause
    exit /b
)

:: 3. INTELIGENTNE SPRAWDZANIE CZY BAZA ISTNIEJE
echo [1/2] Weryfikacja bazy danych...

:: Pytamy Postgresa czy widzi baze o takiej nazwie. 
:: Flaga -tAc zwraca '1' jesli baza jest, lub pusty ciag jesli jej nie ma.
for /f "tokens=*" %%i in ('docker exec %CONTAINER_NAME% psql -U %DB_USER% -tAc "SELECT 1 FROM pg_database WHERE datname='%DB_NAME%'"') do set DB_EXISTS=%%i

if "!DB_EXISTS!"=="1" (
    echo       [INFO] Baza danych '%DB_NAME%' juz istnieje.
    echo       Pomijam tworzenie i przechodze do importu.
) else (
    echo       [INFO] Baza nie istnieje. Tworze nowa...
    docker exec %CONTAINER_NAME% createdb -U %DB_USER% %DB_NAME%
    
    if !errorlevel! equ 0 (
        echo       [SUKCES] Baza zostala utworzona.
    ) else (
        color 0C
        echo       [BLAD] Nie udalo sie utworzyc bazy. Sprawdz logi.
        pause
        exit /b
    )
)

echo.
echo [2/2] Rozpoczynam import pliku: %~n1%~x1
echo       Prosze czekac...

:: 4. IMPORT DANYCH
:: Uzywamy polecenia 'type' zeby wyslac plik do kontenera
type "%~1" | docker exec -i %CONTAINER_NAME% psql -U %DB_USER% -d %DB_NAME%

if %errorlevel% equ 0 (
    color 0A
    echo.
    echo ========================================================
    echo   [SUKCES] IMPORT ZAKONCZONY POMYSLNIE!
    echo ========================================================
) else (
    color 0C
    echo.
    echo   [BLAD] Wystapil problem podczas importu SQL.
    echo   Sprawdz czy plik nie zawiera bledow.
)

echo.
pause