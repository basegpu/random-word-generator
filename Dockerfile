FROM python:3.10-slim-buster

RUN mkdir /app
WORKDIR /app

COPY requirements.txt /app
RUN pip3 install -r requirements.txt

COPY templates /app/templates
COPY data /app/data
COPY src /app/src

CMD gunicorn -w 2 -b 0.0.0.0:$PORT --chdir src "main:app"