FROM python:3.7-slim

ENV PLATFORM_ROUTE=analytics-apps
ENV PDF_SERVER=http://don-mk8s-lb-3c9b790ca6219e7e.elb.us-west-1.amazonaws.com/pdf-server/generate-report
ENV VIEW_SERVICE=http://don-mk8s-lb-3c9b790ca6219e7e.elb.us-west-1.amazonaws.com/view-service
ENV API_SERVER=https://asura.opsramp.net
ENV INCLUDE_WRAPPER=true

USER root

WORKDIR /app

ADD . /app

RUN pip install -r requirements.txt

EXPOSE 8050

CMD ["gunicorn", "--workers=2", "app:server", "-b 0.0.0.0:8050"]
