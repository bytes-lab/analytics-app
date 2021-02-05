FROM python:3.7-slim

ENV PLATFORM_ROUTE=metered-usage-insight
ENV PDF_SERVER=http://don-mk8s-lb-3c9b790ca6219e7e.elb.us-west-1.amazonaws.com/pdf-server/generate-report
ENV VIEW_SERVICE=http://don-mk8s-lb-3c9b790ca6219e7e.elb.us-west-1.amazonaws.com/view-service
ENV API_SERVER=http://don-mk8s-lb-3c9b790ca6219e7e.elb.us-west-1.amazonaws.com
USER root

WORKDIR /app

ADD . /app

RUN pip install -r requirements.txt

EXPOSE 8000

CMD ["gunicorn", "--workers=2", "app:server", "-b 0.0.0.0:8000"]
