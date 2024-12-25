#!/usr/bin/env bash

pip install uv
PORT=${PORT:-8000}
uv run gunicorn -w 5 -b 0.0.0.0:$PORT page_analyzer:app