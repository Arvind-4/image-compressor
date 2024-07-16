#!/bin/bash

HOST=${HOST:-"0.0.0.0"}
PORT=${PORT:-"8000"}

gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.main:app --bind $HOST:$PORT