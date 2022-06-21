FROM python:3.7
RUN apt-get update && apt-get -y install vim
WORKDIR /opt/followup
COPY requirements.txt ./requirements.txt
RUN pip install -r requirements.txt
