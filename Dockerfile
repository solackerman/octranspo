FROM python:3.6-slim

WORKDIR /app
ADD . /app

RUN apt-get update && \
    apt-get install -y gcc && \
    pip install -r requirements/production.txt && \
    mv .env_docker .env

CMD ["python", "run.py"]