cd /d "%~dp0Webpage"
call backend\env\Scripts\activate.bat
call set_keys.bat
python seed.py
pause