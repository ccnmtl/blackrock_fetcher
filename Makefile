VE ?= ./ve
FLAKE8 ?= $(VE)/bin/python -m flake8
REQUIREMENTS ?= requirements.txt
SYS_PYTHON ?= python3
PIP ?= $(VE)/bin/python -m pip
PY_SENTINAL ?= $(VE)/sentinal
WHEEL_VERSION ?= 0.33.6
SUPPORT_DIR ?= requirements/
MAX_COMPLEXITY ?= 10
PY_DIRS ?= *.py tests

all: flake8 test

$(PY_SENTINAL):
	rm -rf $(VE)
	$(SYS_PYTHON) -m venv $(VE)
	$(PIP) install wheel==$(WHEEL_VERSION)
	$(PIP) install --no-deps --requirement $(REQUIREMENTS)
	touch $@

flake8: $(PY_SENTINAL)
	$(FLAKE8) $(PY_DIRS) --max-complexity=$(MAX_COMPLEXITY) --extend-ignore=W605

test: $(PY_SENTINAL)
	$(VE)/bin/python -m unittest

clean:
	rm -rf ve

cunix:
	pyenv local 3.6.9
	python -m venv ve
	./ve/bin/pip install -r requirements.txt 

.PHONY: clean flake8 test cunix
