FROM python:3.7-slim

ENV PLATFORM_ROUTE=hello-world-app
ENV API_SERVER=https://asura.opsramp.net
USER root

WORKDIR /app

ADD . /app

RUN pip install -r requirements.txt

EXPOSE 8000

CMD ["gunicorn", "--workers=2", "app:server", "-b 0.0.0.0:8000"]
