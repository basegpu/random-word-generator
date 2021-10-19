FROM python:3.10-slim-buster

RUN mkdir /app
WORKDIR /app

COPY requirements.txt /app
RUN pip3 install -r requirements.txt

COPY syllables.csv /app
COPY *.py /app

CMD ["gunicorn", "-w 4", "-b", "0.0.0.0:8000", "main:app"]