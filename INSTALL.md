### Pre-requisite(installed in system):
1. python 3.8 + 
2. Mysql 5.7 or 8
3. Weasyprint and cairo
4. MQTT broker

**NOTE:** *for deployment, clone the project inside the folder `/srv/apps/` and make sure to change owner of the folder to "isa"*

## Installation guide

### Option 1: Ubuntu Linux 20.04 (preferred)

* update Ubuntu
```
sudo apt -y update && sudo apt -y dist-upgrade
```
* install project dependencies
```
sudo apt -y install python3-pip python3-venv mysql-client
sudo apt -y install libmysqlclient-dev libsdl-pango-dev libcairo2-dev
```
* cd into your home/working folder
```
cd ~
```

### Option 2: Windows 10
* download and install [Python 3.8+](https://www.python.org/ftp/python/3.8.6/python-3.8.6-amd64.exe)
* download and install [MySQL 8.0+](https://dev.mysql.com/get/Downloads/MySQLInstaller/mysql-installer-community-8.0.22.0.msi)
* download and install [Git 2.2+](https://git-scm.com/download/win)
* for WeasyPrint, download and install [GTK+ 64](https://github.com/tschoonj/GTK-for-Windows-Runtime-Environment-Installer/releases/download/2020-07-15/gtk3-runtime-3.24.20-2020-07-15-ts-win64.exe)
* open PowerShell as standard user and create your working folder
```
cd ~
mkdir apps
cd apps
```
* allow running of ps scripts for current user
```
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```


### Standard commands for both Ubuntu and Windows 10

**Clone project from GitLab:**
* clone project repository into a folder named "`src`"
```
git clone https://gitlab.isa.net.ph/johnpeteraa/pms_win_3.0.git src
```

---
**For PIPENV user:**
* install PIPENV
```
pip3 install pipenv
```
* cd into the cloned project folder
```
cd src
```
* create virtual environment and install all required packages from Pipfile
```
pipenv install
```
* activate virtual environment
```
pipenv shell
```

---
**For VENV user:**
* create virtual environment
```
python3 -m venv venvpms
```
* **Ubuntu**: activate virtual environment
```
source venvpms/bin/activate

```
* **Windows**: activate virtual environment
```
.\venvpms\Scripts\Activate.ps1

```
* upgrade PIP, setuptools and install weasyprint
```
python -m pip install --upgrade pip setuptools
python -m pip install weasyprint
```
* cd into the cloned project folder
```
cd src
```
* install all required packages from requirements.txt *(run again if errors are encountered)*
```
pip install -r requirements.txt
```

---
**Initial project run:** *(assumes empty DB already created and DB user)*

* edit `pms_win/settings.py` and adjust DATABASES section as needed *(sample below)*
```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'pmsdb',
        'USER': 'dbuser',
        'PASSWORD': 'dbpassword',
        'HOST': 'localhost',
        'PORT': ''
    },
}
```
* run migrate to initialize the database
```
python manage.py migrate
```
* create admin user
```
python manage.py createsuperuser
```
* start django's webserver (port 8000)
```
python manage.py runserver
```
