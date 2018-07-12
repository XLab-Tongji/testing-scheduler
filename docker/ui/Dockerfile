FROM node:alpine
MAINTAINER Leo.C
ENV REPO_DIR /home/testing-scheduler
COPY . .
WORKDIR ${REPO_DIR}/ui

RUN /bin/sh -c 'npm config set registry https://registry.npm.taobao.org'
RUN /bin/sh -c 'npm install vue; npm install -g vue-cli'
RUN /bin/sh -c 'npm install .'

EXPOSE 5311
CMD /bin/sh -c 'npm run dev'