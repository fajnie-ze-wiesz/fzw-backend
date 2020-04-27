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
FLAKE8 := flake8
FLAKE8_OPTS :=
FLAKE8_ARGS := ${ARGS}
MYPY := mypy
MYPY_OPTS :=
MYPY_ARGS := ${ARGS}
PYLINT := pylint
PYLINT_OPTS := --rcfile=setup.cfg
PYLINT_ARGS := ${ARGS}
PYTEST := py.test
PYTEST_OPTS :=
PYTEST_ARGS := ${ARGS}

.PHONY: all
all: check test  ## check code, test

.PHONY: install_dev
install_dev:  ## install all pip requirements
	${PYTHON} -m pip install ${PIP_INSTALL_OPTS} -r requirements.txt -r dev-requirements.txt ${ARGS}

.PHONY: test
test:  ## run tests
	${PYTEST} ${PYTEST_OPTS} ${PYTEST_ARGS}

.PHONY: check
check: flake8 mypy pylint  ## run checks: flake8, mypy, pylint

.PHONY: flake8
flake8:  ## run flake8
	${FLAKE8} ${FLAKE8_OPTS} ${FLAKE8_ARGS}

.PHONY: mypy
mypy:  ## run mypy
	${MYPY} ${MYPY_OPTS} ${PACKAGE_DIR} ${MYPY_ARGS}

.PHONY: pylint
pylint:  ## run pylint
# run pylint for production code and test code separately
	${PYLINT} ${PYLINT_OPTS} ${PACKAGE_DIR} ./*.py ${ARGS}
	${PYLINT} ${PYLINT_OPTS} --disable=duplicate-code --disable=redefined-outer-name ${TESTS_DIR} ${ARGS}

.PHONY: start_dev_db
start_dev_db:  ## start database (via docker)
	${DOCKER_COMPOSE} up --detach

.PHONY: stop_dev_db
stop_dev_db:  ## stop database (via docker)
	${DOCKER_COMPOSE} down

.PHONY: migrate_db
migrate_db:  ## migrate database
	${PYTHON} manage.py migrate

.PHONY: serve_dev
serve_dev:  ## run development server
	DEBUG=1 ${PYTHON} manage.py runserver 0:8000

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

.PHONY: help
help:  ## list all make targets
	@${AWK} -F ':.*##' '$$0 ~ FS {printf "%-32s%s\n", $$1 ":", $$2}' $(MAKEFILE_LIST) | ${GREP} -v {AWK} | ${SORT}
