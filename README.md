# Login API

**Install virtual environment**
```bash
sudo apt-get install python3-dev
pip install virtualenv
virtualenv -p /usr/bin/python3.5 venv
source venv/bin/activate
pip install -r requirements.txt
```

**Create Database**
```sudo -u postgres psql
CREATE DATABASE login_register;
\q
```
```bash
flask db migrate -m "users table"
flask db upgrade
```

**Run application**
```bash
flask run
```