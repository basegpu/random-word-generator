FROM python:3.10-slim-buster

RUN mkdir /app
WORKDIR /app

COPY requirements.txt /app
RUN pip3 install -r requirements.txt

COPY syllables.csv /app
COPY *.py /app
COPY templates /app/templates

CMD gunicorn -w 2 -b 0.0.0.0:$PORT "main:app"