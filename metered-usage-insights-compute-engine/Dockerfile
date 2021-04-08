FROM python:3.8.8-alpine3.12

ENV API_SERVER=http://don-mk8s-lb-3c9b790ca6219e7e.elb.us-west-1.amazonaws.com

USER root

WORKDIR /app

ADD . /app

RUN apk add sqlite
RUN pip install -r requirements.txt

EXPOSE 8000

CMD uvicorn main:app --reload --host 0.0.0.0 --port 8000
