:: Jak go używać?
: :Stwórz plik wgraj_backup.bat.
: :Złap myszką plik .sql, który chcesz wgrać.
: :Upuść go na ikonkę skryptu wgraj_backup.bat.

@echo off
:: --- KONFIGURACJA ---
set CONTAINER_NAME=projekt-db-1
set DB_USER=myuser
set DB_NAME=mydatabase
:: --------------------

if "%~1"=="" (
    echo.
    echo [BLAD] Nie wybrano pliku!
    echo Prosze przeciagnac plik .sql na ikone tego skryptu.
    pause
    exit /b
)

echo.
echo ========================================================
echo   Importowanie do bazy: %DB_NAME%
echo   Plik: %~n1%~x1
echo ========================================================
echo.

:: --- KROK 1: PROBA UTWORZENIA BAZY (Jesli nie istnieje) ---
echo [1/2] Sprawdzam czy baza istnieje...
docker exec %CONTAINER_NAME% createdb -U %DB_USER% %DB_NAME% 2>nul

if %ERRORLEVEL% equ 0 (
    echo       Utworzono nowa baze danych: %DB_NAME%
) else (
    echo       Baza %DB_NAME% juz istnieje (lub inny blad), kontynuuje import...
)
echo.

:: --- KROK 2: IMPORT DANYCH ---
echo [2/2] Wgrywanie danych...
type "%~1" | docker exec -i %CONTAINER_NAME% psql -U %DB_USER% -d %DB_NAME%

if %ERRORLEVEL% equ 0 (
    echo.
    echo [SUKCES] Operacja zakonczona!
) else (
    echo.
    echo [BLAD] Wystapil problem podczas importu.
)

pause