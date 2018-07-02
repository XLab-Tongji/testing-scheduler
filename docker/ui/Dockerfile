FROM python:2.7
MAINTAINER Leo.C
ENV REPO_DIR /home/testing-scheduler
WORKDIR ${REPO_DIR}
COPY ./ui .

RUN /bin/sh -c 'curl -sL https://deb.nodesource.com/setup_6.x | bash -; apt-get install -y nodejs; npm install vue; npm install -g vue-cli'
RUN /bin/sh -c 'npm install;'

EXPOSE 5311
EXPOSE 5312
CMD /bin/sh -c 'node proxy-server.js & npm run dev'
