all: install approve docs

install:
	pip3 install -r requirements.txt

lint:
	pylint --rcfile=.pylintrc src
	pylint --rcfile=.pylintrc tests/unit

docs: cleandocs
	pdoc3 --html --force --output-dir docs src

test:
	python3 -m pytest --cov-report html --cov=src -vv

check-type:
	mypy --ignore-missing-imports src
	mypy --ignore-missing-imports tests/unit

clean-output:
	nbstripout src/*.ipynb

approve: check-type lint test

cleandocs:
	rm -rf docs
