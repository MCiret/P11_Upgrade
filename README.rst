=====================
"Pur Beurre" project
=====================
**Searching for food substitution in Open Food Facts french database**

https://purbeurre-mcda.tk/

|Status badge| |UIlanguage badge| |vPython badge| |vBootstrap badge|

*****************
TABLE OF CONTENTS
*****************

1. `DESCRIPTION`_
    * `Summary`_
    * `Features`_

2. `INSTALLATION`_
    * `Using Docker`_
    * `Using Python Package Manager (pipenv)`_

3. `OPEN FOOD FACTS API USAGE`_

DESCRIPTION
===========

Summary
-------
This Web application asks user for researching a food product to obtain more healthy alternatives based on nutriscore value.
The user could log in to bookmark a food product.

Food products are weekly collected from Open Food Facts (OFF) french database (requested via the OFF search API).
The API request response is a json data then parsed, reorganized and inserted in a database.

*NB: this source code is for french User Interface.*

Features
--------

1) User (logged or not (see below)) researches a food product in order to obtain an healthy substitute food.

    1.1) User could use research field (present in all pages header and in home page) to enter keywords and display the result page.

        - If only 1 food product matches the research keywords then substitutes foods are displayed.
        - Else if many food products match the research keywords then they are listed to be chosen by user and then substitutes foods are displayed.

    1.2) Click on substitute food picture to display the details page and its Open Food Facts url.

2) User (unlogged) creates or logs in.

    2.1) Unlogged user could click on the person-plus or carot icon to access the account creation page.

        - If the account is created, user is redicted to home page.
        - Else if the account is not created (email already exists or wrong password) the page is redisplayed and a message informs user of the reason why.

    2.2) Unlogged user on account creation page (see 2.1) could use the link "Cliquez ici pour vous connecter..." to access the account login page.

        - If the user is logged, he is redicted to home page.
        - Else if the user is not logged (wrong email or password) the page is redisplayed and a message informs user of the problem.

3) User (logged) bookmarks a substitute food product.

    3.1) Logged user could see and use the "Sauvegarder" button below the substitute food product picture to save and get back faster later.

        - If the user had already bookmarked a substitute food product, the text "Sauvegardé 🗹" is displayed below the picture.

    3.2) Logged user could click on carot icon (header menu) to diplay all his bookmarked food products.

    3.3) Logged user could modify his password from "Mon compte" page using the dedicated form. He could not re-use an ex-password.

    3.4) Not still logged but having an account, user could use the link "J'ai oublié mon mot de passe" on the "Connexion à un compte Pur Beurre" page.


INSTALLATION
============

This app is running : https://purbeurre-mcda.tk/ Deployment was done using a CI/CD workflow (GitHub Actions) where the Django app Docker image is build and send to the hosted server (ssh) with the docker-compose.prod.yml file. To complete this deployment, there are several pre-requisite steps that are to be done manually like copying .env files, nginx folder etc.


However, if you want to run this app locally, there are 2 ways :
1) the simplest is to use local Docker version (see docker_install_ section)
2) the still classic way is to use the Python Package Manager (pip) to install needed libs in a created Virtual environment (see classic_install_ section)


Using Docker
------------

.. _docker_install:

This app could be installed and run locally using "Dockerization" with the docker-compose.local.prod.yml file.


 ℹ️ **This section has to be written.**

Using Python Package Manager (pipenv)
-------------------------------------

.. _classic_install:

Application
^^^^^^^^^^^

1) Download the project : use the "Code" (green button) and unzip the P11_Upgrade.zip file.
2) Python3 comes with Python Package Manager (pip) else you have to install it (https://pip.pypa.io/en/stable/installing/)

3) Set up a virtual environment :

    NB: the symbol $ flags the commands prompt

    * UNIX operating system :
        3.1) Install the Python module : ``$ pip install pipenv``

        3.2) Install project requirements (i.e Pipfile list) : ``$ pipenv install``

        3.3) Activate the virtual environment : ``$ pipenv shell``


    * DOS operating system : same as UNIX os above..


4) Environment variables to be set/adapted :

    * project_config/settings.py :

        - variable SECRET_KEY (key to securing signed data) set with DJANGO_KEY enviro. variable name
        - variable DATABASES['default']['PASSWORD'] set with POSTGRE_PWD enviro. variable name

6) Install and fill the database (see db_settingup_ below).

7) Collect static files : (UNIX) ``$ python manage.py collectstatic`` (DOS) ``$ py manage.py collectstatic``

8) Run the code source main.py file : (UNIX) ``$ python manage.py runserver`` (DOS) ``$ py manage.py runserver``

9) Follow the http:// link given by Django starting message on the terminal output (usually http://127.0.0.1:8000/) to display interface in your browser.

Database
^^^^^^^^

.. _db_settingup:

*NB: this step is required only if you are not using Docker to install and run the app*

1) Install your favorite SGDB.
2) Create a database and Set up variable DATABASES (project_config/settings.py) with your database connection parameters.
3) Database migration (i.e tables creation) : (UNIX) ``$ python manage.py migrate`` (DOS) ``$ py manage.py migrate``
4) Run personalised Django command to request Open Food Facts API and insert food products (and categories) in database : (UNIX) ``$ python manage.py filldb`` (DOS) ``$ py manage.py filldb``

**note:** you can modify which data are requested from Open Food Facts API.


OPEN FOOD FACTS API USAGE
=========================

See research/management/commands/filldb.py

The build_get_request() static method (called by handle() method) shows you the used request.
https://documenter.getpostman.com/view/8470508/SVtN3Wzy#58efae40-73c3-4907-9a88-785faff6ffb1

**Warning:** if you modify the fields parameter then you will have to adapt the front-end part of the application.


Nevertheless, there is no problem if you would like to modify categories, page_size (number of product per page) and/or page (number of page per request).
The categories tags and page_nb are gotten from research/management/off_research_params.json. This file is modified (rewritten) each time the filldb command is used, to "feed" the database, the page_nb parameter is incremented.

**note:** categories tags have to exists in OFF. They are not case sensitive but you have to use underscore te replace whitespace characters.


.. |vPython badge| image:: https://img.shields.io/badge/Python-3.10-blue.svg
.. |vBootstrap badge| image:: https://img.shields.io/badge/Bootstrap-5-purple.svg

.. |Status badge| image:: https://img.shields.io/badge/Status-Production-green.svg
.. |UIlanguage badge| image:: https://img.shields.io/badge/UILang-French-9cf.svg
