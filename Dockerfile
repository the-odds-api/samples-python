FROM python:3.7

ENV APP_HOME /usr/src/app/

WORKDIR $APP_HOME

COPY requirements.txt $APP_HOME/requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY ./ $APP_HOME
