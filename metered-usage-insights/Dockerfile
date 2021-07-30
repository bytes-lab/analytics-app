FROM python:3.7-slim

ENV PLATFORM_ROUTE=analytics-apps
ENV DATA_API_BASE_URL=https://asura.opsramp.net
ENV APP_SERVICE_BASE_URL=http://13.57.187.238:8001/oap-api/v1
ENV OAP_APP_ID=32a1bc14-c471-46a4-9b0a-835b4b80e58f
ENV INCLUDE_WRAPPER=true
ENV ON_PROXY=false

USER root

WORKDIR /app

ADD . /app

RUN pip install -r requirements.txt

EXPOSE 8050

CMD ["gunicorn", "--workers=2", "app:server", "-b 0.0.0.0:8050"]
