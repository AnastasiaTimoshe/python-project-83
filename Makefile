install:
	poetry install


lint:
	poetry run flake8


selfcheck:
	poetry check


build:
	./build.sh


publish:
	poetry publish --dry-run


dev:
	poetry run flask --app page_analyzer:app run


PORT ?= 8000
start:
	poetry run gunicorn -w 5 -b 0.0.0.0:$(PORT) page_analyzer:app
