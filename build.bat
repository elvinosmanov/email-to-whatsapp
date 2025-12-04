@echo off
echo ============================================================
echo  Email to WhatsApp - Windows Build Script
echo ============================================================
echo.

echo [1/4] Installing dependencies...
python -m pip install --upgrade pip
pip install -r requirements.txt
pip install pyinstaller

echo.
echo [2/4] Building executable with PyInstaller...
pyinstaller --onefile --name EmailToWhatsApp --optimize 2 --exclude-module matplotlib --exclude-module numpy --exclude-module pandas --exclude-module scipy --exclude-module pytest --exclude-module tkinter --exclude-module unittest email_to_whatsapp_selenium.py

echo.
echo [3/4] Creating deployment package...
cd dist
if not exist EmailToWhatsApp_Package mkdir EmailToWhatsApp_Package
copy EmailToWhatsApp.exe EmailToWhatsApp_Package\
copy ..\chromedriver.exe EmailToWhatsApp_Package\ 2>nul

echo.
echo [4/4] Creating README file...
echo Email to WhatsApp Monitor > EmailToWhatsApp_Package\README.txt
echo. >> EmailToWhatsApp_Package\README.txt
echo Installation: >> EmailToWhatsApp_Package\README.txt
echo 1. Make sure Google Chrome is installed >> EmailToWhatsApp_Package\README.txt
echo 2. Both files must be in the same folder >> EmailToWhatsApp_Package\README.txt
echo 3. Download chromedriver.exe if not included >> EmailToWhatsApp_Package\README.txt
echo    https://chromedriver.chromium.org/downloads >> EmailToWhatsApp_Package\README.txt
echo. >> EmailToWhatsApp_Package\README.txt
echo Usage: >> EmailToWhatsApp_Package\README.txt
echo 1. Double-click EmailToWhatsApp.exe >> EmailToWhatsApp_Package\README.txt
echo 2. Scan QR code with WhatsApp on first run >> EmailToWhatsApp_Package\README.txt
echo 3. Program will run continuously >> EmailToWhatsApp_Package\README.txt
echo. >> EmailToWhatsApp_Package\README.txt
echo Configuration: >> EmailToWhatsApp_Package\README.txt
echo - Email: bakugan192@gmail.com >> EmailToWhatsApp_Package\README.txt
echo - WhatsApp Group: Shift schedule >> EmailToWhatsApp_Package\README.txt
echo - Check interval: 20 seconds >> EmailToWhatsApp_Package\README.txt

echo.
echo ============================================================
echo  BUILD COMPLETE!
echo ============================================================
echo.
echo Your files are in: dist\EmailToWhatsApp_Package\
echo.
echo Files included:
dir EmailToWhatsApp_Package
echo.
echo Press any key to exit...
pause >nul
