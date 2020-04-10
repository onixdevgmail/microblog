# Microblog

**Install virtual environment**
```bash
sudo apt-get install python3-dev
pip install virtualenv
virtualenv -p /usr/bin/python3.5 venv
source venv/bin/activate
pip install -r requirements.txt
```

**.flaskenv**
```
Create file microblog/.flaskenv
Put there your settings like in microblog/.flaskenv.example

MS_TRANSLATOR_KEY must be generated on https://portal.azure.com/
```

**Migration**
``
flask db migrate -m 'your message'
flask db upgrade
``

**Run application**
```bash
flask run
```
