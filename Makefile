all: install approve docs

install:
	pip3 install -r requirements.txt

lint:
	pylint --rcfile=.pylintrc src/*.py
	pylint --rcfile=.pylintrc tests/*/*.py

docs:
	pdoc3 --html --force --output-dir docs src/*.py

test:
	python3 -m pytest

check-type:
	mypy --ignore-missing-imports src/*.py
	mypy --ignore-missing-imports tests/*/*.py

approve: check-type lint test