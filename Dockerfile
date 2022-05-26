# syntax=docker/dockerfile:1

FROM python:latest

WORKDIR /app

RUN apt-get update

RUN apt-get -y install libglib2.0-0
RUN apt-get -y install libgl1-mesa-glx
RUN apt-get -y install build-essential libgl1-mesa-dev
RUN apt-get -y install libxkbcommon-x11-0

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

# CMD ["python", "src/morphinspector.py"]
CMD /bin/bash