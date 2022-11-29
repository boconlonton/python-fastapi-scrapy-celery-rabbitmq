FROM python:3.8-slim

RUN mkdir /api

WORKDIR /api

RUN pip install --upgrade pip

RUN apt-get update \
    && apt-get install gcc -y \
    && apt-get clean

COPY ./requirements.txt requirements.txt

RUN pip install -r /api/requirements.txt && rm -rf /root/.cache/pip

COPY . /api

WORKDIR /api
