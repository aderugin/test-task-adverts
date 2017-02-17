FROM python:3.5
ENV PYTHONUNBUFFERED 1

RUN apt-get update \
    && apt-get -y install uuid-dev \
    && apt-get -y install cron

RUN mkdir -p /webapp
COPY ./requirements /webapp/requirements
WORKDIR /webapp

COPY ./crontab /etc/cron.d/webapp-cron
RUN chmod 0644 /etc/cron.d/webapp-cron
RUN touch /var/log/cron.log

RUN pip install --upgrade pip
RUN pip install -r requirements/develop.txt
