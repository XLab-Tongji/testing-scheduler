FROM python:2.7
MAINTAINER Leo.C
ENV REPO_DIR /home/testing-scheduler
WORKDIR ${REPO_DIR}
COPY ./ui .

RUN /bin/sh -c 'curl -sL https://deb.nodesource.com/setup_6.x | bash -; apt-get install -y nodejs;' 
RUN /bin/sh -c 'npm install -g cnpm --registry=https://registry.npm.taobao.org; cnpm install vue;'
RUN /bin/sh -c 'cnpm install -g vue-cli'
RUN /bin/sh -c 'cnpm install .'

EXPOSE 5311
CMD /bin/sh -c 'npm run dev'
