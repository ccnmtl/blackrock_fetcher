VE ?= ./ve
FLAKE8 ?= $(VE)/bin/python -m flake8
REQUIREMENTS ?= requirements.txt
SYS_PYTHON ?= python3
PIP ?= $(VE)/bin/python -m pip
PY_SENTINAL ?= $(VE)/sentinal
WHEEL_VERSION ?= 0.30.0
SUPPORT_DIR ?= requirements/
MAX_COMPLEXITY ?= 10
PY_DIRS ?= *.py tests

$(PY_SENTINAL):
	rm -rf $(VE)
	$(SYS_PYTHON) -m venv $(VE)
	$(PIP) install wheel==$(WHEEL_VERSION)
	$(PIP) install --use-wheel --no-deps --requirement $(REQUIREMENTS)
	touch $@

flake8: $(PY_SENTINAL)
	$(FLAKE8) $(PY_DIRS) --max-complexity=$(MAX_COMPLEXITY) --extend-ignore=W605

test: $(PY_SENTINAL)
	$(VE)/bin/python -m tests.test_data_processor

clean:
	rm -rf ve

.PHONY: clean
