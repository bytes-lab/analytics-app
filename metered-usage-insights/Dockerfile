FROM python:3.7-slim

ENV PLATFORM_ROUTE=analytics-apps
ENV API_SERVER=https://asura.opsramp.net
ENV INCLUDE_WRAPPER=true
ENV ON_PROXY=true

USER root

WORKDIR /app

ADD . /app

RUN pip install -r requirements.txt

EXPOSE 8050

CMD ["gunicorn", "--workers=2", "app:server", "-b 0.0.0.0:8050"]
