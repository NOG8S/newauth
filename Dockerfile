FROM python:2-onbuild
MAINTAINER Rob Haswell <me@robhaswell.co.uk>

RUN apt-get -y update
RUN apt-get -y upgrade
RUN apt-get -y install git node.js npm
RUN ln -s /usr/bin/nodejs /usr/local/bin/node

RUN npm install -g bower

CMD ["python", "run.py"]
