install:
	poetry install

build:
	./build.sh

publish:
	poetry publish --dry-run

package-install:
	python3 -m pip install --user dist/hexlet_code-0.1.0-py3-none-any.whl

package-reinstall:
	python3 -m pip install . --force-reinstall

lint:
	poetry run flake8

dev:
	poetry run flask --app page_analyzer:app run


PORT ?= 8000

install:
	poetry install --no-dev
dev:
	poetry run flask --app page_analyzer:app run --debug
start:
	poetry run gunicorn -w 5 -b 0.0.0.0:$(PORT) page_analyzer:app
lint:
	poetry run flake8 --ignore=F401 page_analyzer/app.py
build:
	./build.sh