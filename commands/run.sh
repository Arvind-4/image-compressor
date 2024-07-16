#!/bin/bash

HOST=${HOST:-"0.0.0.0"}
PORT=${PORT:-"8000"}

uvicorn app.main:app --reload --host $HOST --port $PORT