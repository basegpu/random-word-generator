FROM python:3.10-slim-buster

RUN mkdir /syllable-shaker
WORKDIR syllable-shaker

COPY requirements.txt .
RUN pip3 install -r requirements.txt

COPY src/app/ app/
COPY src/main.py .

CMD gunicorn -w 2 -b 0.0.0.0:$PORT "main:app"