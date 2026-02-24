@echo off
setlocal

REM Proje klasorunde calistir
cd /d "%~dp0"

echo [1/3] Sanal ortam kontrolu (opsiyonel)...
if exist ".venv\Scripts\activate.bat" (
    call ".venv\Scripts\activate.bat"
)

echo [2/3] Paketler kontrol ediliyor...
pip install -r requirements.txt

echo [3/3] Otomatik kupon akisi baslatiliyor...
python otomatik_kupon_windows.py --config kupon_sablon.json

echo.
echo Islem tamamlandi.
endlocal
