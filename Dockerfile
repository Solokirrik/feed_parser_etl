FROM python:3.7.0
RUN apt-get update
RUN mkdir -p /opt/webapp
WORKDIR /opt/webapp
COPY requirements.txt ./
RUN pip install -r ./requirements.txt
COPY webapp ./
