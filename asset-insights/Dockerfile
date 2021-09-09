FROM python:3.7-slim

ENV PLATFORM_ROUTE=analytics-apps
ENV DATA_API_BASE_URL=https://staging.opsramp.com
#ENV APP_SERVICE_BASE_URL=http://13.57.187.238:8001
ENV APP_SERVICE_BASE_URL=http://172.26.103.192:8001/oap-api/v1
ENV OAP_APP_ID=442e2df8-3175-4508-b6d9-8a8271443854
ENV INCLUDE_WRAPPER=true
ENV ON_PROXY=true

USER root

WORKDIR /app

ADD . /app

RUN pip install -r requirements.txt

EXPOSE 8050

CMD ["gunicorn", "--timeout=10000", "--workers=2", "app:server", "-b 0.0.0.0:8050"]
