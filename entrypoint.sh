#!/bin/bash --login
# The --login ensures the bash configuration is loaded,
echo "starting the database seed"
# python seed.py
echo "starting the Backend Web Server"
exec uvicorn main:app --reload --host 0.0.0.0 --port 8000
# exec gunicorn main:app --workers 4 --bind 0.0.0.0:8000
