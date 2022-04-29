# Pull base image
FROM python:3.10.4-slim-bullseye

# Set environment varibles
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /code/
COPY . /code/
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

EXPOSE 8000
COPY entrypoint.sh /entrypoint.sh
## set RUN permission to docker-entrypoint ##
RUN chmod +x /entrypoint.sh
# CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
