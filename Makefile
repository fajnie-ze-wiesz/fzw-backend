SHELL := /bin/bash

PACKAGE_DIR := fzw
TESTS_DIR := tests

GREP := grep
AWK := awk
SORT := sort
RM := rm
FIND := find
XARGS := xargs
CAT := cat
DOCKER_COMPOSE := docker-compose

PYTHON := python
PIP_INSTALL_OPTS :=
PIP_COMPILE := pip-compile
PIP_COMPILE_OPTS :=
FLAKE8 := flake8
FLAKE8_OPTS :=
FLAKE8_ARGS := ${ARGS}
MYPY := mypy
MYPY_OPTS :=
MYPY_ARGS := ${ARGS}
PYLINT := pylint
PYLINT_OPTS := --rcfile=setup.cfg --load-plugins pylint_django --load-plugins pylint_django.checkers.migrations
PYLINT_ARGS := ${ARGS}
PYTEST := py.test
PYTEST_OPTS := -v
PYTEST_ARGS := ${ARGS}

.PHONY: help
help:  ## display this help screen
	@grep -E '^[\.a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.PHONY: all
all: check test  ## check code, test

.PHONY: dev.setup
dev.setup: dev.install dev.setup-db  ## install and setup the database

.PHONY: dev.setup-db
dev.setup-db: docker.start-db db.migrate db.load-fixtures dev.setup-admin ## start, migrate, load fixtures, setup base admin user

.PHONY: dev.setup-admin
dev.setup-admin:  ## setup admin user if not created. use only for local development!
	${PYTHON} manage.py shell -c 'from django.contrib.auth.models import User; (User.objects.create_superuser("admin", password="admin"), print("User admin created")) if not User.objects.filter(username="admin").exists() else print("User admin was already created")'

.PHONY: dev.serve
dev.serve:  ## run development server
	DEBUG=1 ${PYTHON} manage.py runserver 0:8000

.PHONY: dev.install
dev.install:  ## install all pip requirements
	${PYTHON} -m pip install ${PIP_INSTALL_OPTS} -r requirements-all.txt ${ARGS}

.PHONY: dev.update-requirements
dev.update-requirements:  ## update pip requirements using the .in files
	${PIP_COMPILE} ${PIP_COMPILE_OPTS} requirements.in
	${PIP_COMPILE} ${PIP_COMPILE_OPTS} requirements.txt requirements-dev.in -o requirements-all.txt

.PHONY: test.unit
test.unit:  ## run unit tests
	${PYTEST} ${PYTEST_OPTS} ${PYTEST_ARGS}

.PHONY: test
test: test.unit  ## run tests

.PHONY: check
check: check.flake8 check.mypy check.pylint  ## run checks: flake8, mypy, pylint

.PHONY: check.flake8
check.flake8:  ## run flake8
	${FLAKE8} ${FLAKE8_OPTS} ${FLAKE8_ARGS}

.PHONY: check.mypy
check.mypy:  ## run mypy
	${MYPY} ${MYPY_OPTS} ${PACKAGE_DIR} ${MYPY_ARGS}

.PHONY: check.pylint
check.pylint:  ## run pylint
	${PYLINT} ${PYLINT_OPTS} ${PACKAGE_DIR} ${TESTS_DIR} ./*.py ${ARGS}

.PHONY: docker.start-db
docker.start-db:  ## start database (via docker)
	${DOCKER_COMPOSE} up --detach

.PHONY: docker.stop-db
docker.stop-db:  ## stop database (via docker)
	${DOCKER_COMPOSE} down

.PHONY: db.migrate
db.migrate:  ## migrate database
	${PYTHON} manage.py migrate

.PHONY: db.load-fixtures
db.load-fixtures:  ## load fixtures
	${PYTHON} manage.py loaddata --format yaml fixtures/topic_categories.yaml
	${PYTHON} manage.py loaddata --format yaml fixtures/manipulation_categories.yaml

.PHONY: clean
clean:  ## remove generated files
	-${RM} -r .tox
	-${RM} -r .pytest_cache
	-${RM} -r .mypy_cache

	${FIND} "." -iname '__pycache__' -type d -print0 | ${XARGS} -0 ${RM} -r

	-${RM} TEST-*.xml

	-${RM} .coverage
	-${RM} coverage.xml
	-${RM} -r coverage_html_report
