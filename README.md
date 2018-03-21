# Aviator Log

> An aviator logbook web application, written in Django/Python.

### Requirements

Python 2.17.13 and Django 1.10.5. If you use Conda to manage your
Python installation, load and activate the included environment file
[condaenv.txt](condaenv.txt). Otherwise, detailed requirements may be
gleaned from this file, which is human readable.

### Installation

To get a development version of the app running, clone the repository,
change directory into the repo, and create an administative user at
the command line with

````
python manage.py createsuperuser
````

Then start the development server with 


````
python manage.py runserver
````

and navigate to the app at "http://127.0.0.1:8000/logbook/" on your
local browser. Add new users at the administration page
"http://127.0.0.1:8000/admin/".


