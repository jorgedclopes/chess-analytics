all: install approve docs

install:
	pip3 install --upgrade -r requirements.txt

lint:
	pylint --rcfile=.pylintrc src
	pylint --rcfile=.pylintrc tests/unit

docs: cleandocs
	pdoc3 --html --force -c syntax_highlighting=False --output-dir docs src

test:
	pytest --cov-report html --cov=src -vv --cov-fail-under=70

check-type:
	mypy --ignore-missing-imports src
	mypy --ignore-missing-imports tests/unit

clean-output:
	nbstripout src/*.ipynb

approve: check-type lint test

cleandocs:
	rm -rf docs
