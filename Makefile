REPO = pandasheets
VENV_NAME = venv
VENV_PATH = $(VENV_NAME)/bin/activate
PYTHON := venv/bin/python

.PHONY: venv

venv:
ifeq ($(OS),Windows_NT)
	python -m venv $(VENV_NAME)
	. $(VENV_PATH) && pip install -r requirements.txt
else
	python3 -m venv $(VENV_NAME)
	. $(VENV_PATH); pip install -r requirements.txt
endif

activate:
	. source $(VENV_PATH)

.PHONY: test

test:
	python -m pytest tests/

.PHONY: install

install: venv
	. $(VENV_PATH); pip install --upgrade -r requirements.txt

.PHONY: install-dev

install-dev: venv
	. $(VENV_PATH); pip install --upgrade -r requirements-dev.txt

.PHONY: update

update: venv
	. $(VENV_PATH); pip install --upgrade -r requirements.txt

.PHONY: clean

clean:
	rm -rf $(VENV_NAME)

check-black:
	${PYTHON} -m black --check $(REPO) tests

check-isort:
	${PYTHON} -m isort --profile black --check-only $(REPO) tests

check-flake:
	${PYTHON} -m flake8 $(REPO) tests

check-mypy:
	${PYTHON} -m mypy --strict --implicit-reexport $(REPO)

lint: check-flake check-mypy check-black check-isort

format:
	${PYTHON} -m black $(REPO) tests
	${PYTHON} -m isort --profile black $(REPO) tests
