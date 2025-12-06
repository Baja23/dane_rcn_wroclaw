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

:: Sprawdzenie czy uzytkownik upuscil plik na skrypt
if "%~1"=="" (
    echo.
    echo [BLAD] Nie wybrano pliku!
    echo Prosze przeciagnac plik .sql na ikone tego skryptu.
    echo.
    pause
    exit /b
)

echo.
echo ========================================================
echo   UWAGA! Nadpisuje baze danych: %DB_NAME%
echo   Wgrywany plik: %~n1%~x1
echo ========================================================
echo.
echo Nacisnij dowolny klawisz, aby rozpoczac IMPORT...
echo Zamknij to okno, aby anulowac.
pause >nul

echo.
echo Trwa wgrywanie danych... Prosze czekac.

:: Komenda importu (metoda z 'type' i 'docker exec -i')
type "%~1" | docker exec -i %CONTAINER_NAME% psql -U %DB_USER% -d %DB_NAME%

if %ERRORLEVEL% equ 0 (
    echo.
    echo [SUKCES] Baza danych zostala przywrocona!
) else (
    echo.
    echo [BLAD] Wystapil problem podczas importu.
)

pause