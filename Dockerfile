FROM python:3.8.5
ENV PYTHONBUFFERED=1

RUN mkdir -p /home/geronimo

ENV HOME=/home/geronimo
ENV APP_HOME=/home/geronimo/backend
RUN mkdir $APP_HOME
WORKDIR $APP_HOME

COPY requirements.txt $APP_HOME
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . $APP_HOME

RUN useradd geronimo && chown -R geronimo $APP_HOME

USER geronimo
