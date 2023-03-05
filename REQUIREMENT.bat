@echo off

echo Installation des packages externes pour Python...

pip install win32api 
pip install win32con 
pip install win32gui 
pip install keyboard 
pip install PyQt5 
	
echo Packages installés avec succès !
pause