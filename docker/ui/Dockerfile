FROM python:2.7
MAINTAINER Leo.C
ENV REPO_DIR /home/testing-scheduler
WORKDIR ${REPO_DIR}
COPY ./ui .

RUN /bin/sh -c 'cat /etc/apt/sources.list | sed "s/deb.debian.org/mirrors.163.com/" | \
sed "s/security.debian.org/mirrors.163.com/" > /etc/apt/sources.list; apt-get update'

RUN /bin/sh -c 'curl -sL https://deb.nodesource.com/setup_6.x | bash -; apt-get install -y nodejs;' 
RUN /bin/sh -c 'npm install -g nrm; nrm use taobao;'
RUN /bin/sh -c 'npm install vue; npm install -g vue-cli'
RUN /bin/sh -c 'npm install .'

EXPOSE 5311
CMD /bin/sh -c 'npm run dev'
