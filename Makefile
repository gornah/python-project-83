install:
	pip install -r requirements.txt
	uv sync

dev:
	uv run flask --app page_analyzer:app run

PORT ?= 8000
start:
	uv run gunicorn -w 5 -b 0.0.0.0:$(PORT) page_analyzer:app