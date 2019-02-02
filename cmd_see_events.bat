@echo off
REM python %~dp0\login_selenium.py -m "myemail@netcompany.com" -p "mypassword" %*
python %~dp0\login_selenium.py %*
pause
