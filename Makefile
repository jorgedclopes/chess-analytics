all: install approve docs

install:
	pip3 install -r requirements.txt

lint:
	pylint --rcfile=.pylintrc src || true
	pylint --rcfile=.pylintrc tests/unit || true

docs:
	pdoc3 --html --force --output-dir docs src

test:
	python3 -m pytest -v

check-type:
	mypy --ignore-missing-imports src
	mypy --ignore-missing-imports tests/unit

approve: check-type lint test