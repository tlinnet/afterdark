# afterdark

## Requirements

* **choco** : [The package manager for Windows](https://chocolatey.org/)
* **chromedriver** : [ChromeDriver - WebDriver for Chrome](http://chromedriver.chromium.org/)

```
choco install python3
choco install chromedriver
pip install selenium
```

## Run program

Run the script, which will ask for your credentials
```
python login_selenium.py
```

Script also accepts input arguments for direct execution
```
python login_selenium.py -m "yourmail@netcompany.com" -p "your password"
```

Or run the .bat file
```
cmd_see_events.bat
```

## Creation of .exe file

With [pyinstaller](https://www.pyinstaller.org/)
```
pyinstaller login_selenium.py --onefile
```
