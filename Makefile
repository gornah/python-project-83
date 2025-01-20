PORT ?= 8000

install:
	uv sync

dev:
	uv run flask --app page_analyzer:app run

start:
	gunicorn -w 5 -b 0.0.0.0:$(PORT) page_analyzer:app

build:
	./build.sh

render-start:
	gunicorn -w 5 -b 0.0.0.0:$(PORT) page_analyzer:app