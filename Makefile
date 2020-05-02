all: install set_path approve docs

set_path:
	export PYTHONPATH=$(pwd)

install:
	pip3 install -r requirements.txt

lint:
	pylint --rcfile=.pylintrc src || true
	pylint --rcfile=.pylintrc tests/unit || true

docs:
	pdoc3 --html --force --output-dir docs src

test:
	python3 -m pytest --cov-report html --cov=src -vv

check-type:
	mypy --ignore-missing-imports src
	mypy --ignore-missing-imports tests/unit

approve: check-type lint test