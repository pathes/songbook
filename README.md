songbook
========

Development prerequirements
---------------------------

* `virtualenv` (not necessary, but recommended)

Development setup
-----------------

* If you don't want to rely on global python packages, create an instance of `virtualenv` and launch it.

```
virtualenv .
. bin/activate
```

* Install required python packages

```
pip install -r requirements.txt
```
* Copy `app/settings_local.py.example` to `app/settings_local.py`. Customize if necessary.

```
cp app/settings_local.py.example app/settings_local.py
```
* Create a database. `sqlite` is default. This will also allow you to create admin account.

```
python manage.py makemigrations songbook
python manage.py migrate
```

If you want to have initial data in database, load fixtures.

```
python manage.py loaddata basic.json
```
* Launch development server.

```
python manage.py runserver
```
* Visit `http://localhost:8000`.
