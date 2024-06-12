FROM python:3.12-slim

ENV PYTHONUNBUFFERED 1

WORKDIR /dj-movie-rate/

COPY . .

COPY ./requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

RUN apt-get update && apt-get install -y procps

RUN apt-get update && apt-get install -y git
