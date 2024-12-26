PORT ?= 8000

install:
	pip install uv
	uv sync

dev:
	uv run flask --app page_analyzer:app run

start:
	gunicorn -w 5 -b 0.0.0.0:$(PORT) page_analyzer:app