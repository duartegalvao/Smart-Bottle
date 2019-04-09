# UC\_Project
## Overview

Project for the ID2012 course on KTH.

## Objective

TODO

## Issues

Issues are listed in "Issues".

## Development
### Installation
Verify if you have python installed first (if not, install it):
```
$ python -V
```

Then, create a virtual environment and activate it:
```
$ virtualenv bottle-env
$ source bottle-env/bin/activate
```
Then, install the requirements:
```
$ pip install -r requirements.txt
```

### Installation (python not linked to python3)
If by default python is linked to Python 2, follow these steps instead.

Create a virtual environment and activate it:
```
$ virtualenv bottle-env -p python3
$ source bottle-env/bin/activate
```
Then, install the requirements:
```
$ pip3 install -r requirements.txt
```
Also replace "python" with "python3" in the following section.

### Running
First, add a migration for your database system (default: sqlite) and migrate it:

Assuming you are at the project root:
```
$ python bottle/manage.py makemigrations
$ python bottle/manage.py migrate
```

To run server, at default port:
```
$ python bottle/manage.py runserver
```

## Important Notes

Note that this isn't enough in order to dominate Django development.
It is really important to read Django documentation. 

For more information visit [Django Website](https://www.djangoproject.com/)

