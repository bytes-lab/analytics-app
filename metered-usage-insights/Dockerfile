FROM python:3.7-slim

USER root

WORKDIR /app

ADD . /app

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 8050

CMD ["gunicorn", "--workers=2", "app:server", "-b 0.0.0.0:8050"]
