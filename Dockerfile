FROM python:3.7
RUN apt-get update && apt-get -y install vim
RUN mkdir /opt/followup
WORKDIR /opt/followup
COPY requirements.txt ./requirements.txt
COPY . .
RUN pip install -r requirements.txt
