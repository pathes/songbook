songbook
========

Development prerequirements
---------------------------

* `virtualenv` (not necessary, but recommended)

Development setup
-----------------

* If you don't want to rely on global python packages, create an instance of `virtualenv` and launch it.
      virtualenv .
      . bin/activate
If your default system python is `python3`, you may want to create `virtualenv` instance with python2.
      virtualenv -p /path/to/python2 .
* Install required python packages
      pip install -r requirements.txt
* Copy `app/settings_local.py.example` to `app/settings_local.py`. Customize if necessary.
      cp app/settings_local.py.example app/settings_local.py
* Create a database. `sqlite` is default. This will also allow you to create admin account.
      python manage.py syncdb
* Launch development server.
      python manage.py runserver
* Visit `http://localhost:8000`.
