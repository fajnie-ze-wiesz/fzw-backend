# Fajnie że wiesz - backend

[![Build Status](https://travis-ci.org/fajnie-ze-wiesz/fzw-backend.svg?branch=master)](https://travis-ci.org/fajnie-ze-wiesz/fzw-backend)


## Installation

Install [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli):

    sudo apt-get install heroku

Create a virtualenv with Python 3.
The preferred way is to use [virtualenv-wrapper](https://virtualenvwrapper.readthedocs.io/):

    mkvirtualenv -p /usr/bin/python3 fzw

You can also use other tools like [pyenv](https://github.com/pyenv/pyenv).

Install base requirements:

    pip install -r requirements.txt

Install development requirements:

    pip install -r dev-requirements.txt


## Develpoment

You need PostgreSQL database to be set up. You can do that by starting
Docker container via [docker-compose](https://docs.docker.com/compose/):

    docker-compose up

It will automatically forward the port 5432 to your host machine
and create required user and a database.

Assuming your virtualenv is activated, you can set debug mode via environment variable:

    export DEBUG="1"

Then you should ensure that your database is migrated properly:

    ./manage.py migrate

Then you can start the Django development server via:

    ./manage.py runserver 0:8000

After that, you should be able to navigate to http://localhost:8000 and
see your backend running.

If you want to access admin panel, you may need to create Django super user
manually via django shell:

    ./manage.py shell


## Deployment

The changes should be deployed automatically to Heroku via Travis
when you Pull Request will be merged to `master` branch.
