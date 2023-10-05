FROM python:3

WORKDIR /app

COPY requirements.txt /app/

COPY main.py /app/

RUN pip install -r /app/requirements.txt