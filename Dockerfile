FROM python:2
MAINTAINER Rob Haswell <me@robhaswell.co.uk>

COPY requirements.txt /usr/src/app/requirements.txt
WORKDIR /usr/src/app

RUN pip install -r requirements.txt

RUN apt-get -y update
RUN apt-get -y upgrade
RUN apt-get -y install coffeescript git node.js npm
RUN ln -s /usr/bin/nodejs /usr/local/bin/node

RUN npm install -g bower less

CMD ["python", "run.py"]
