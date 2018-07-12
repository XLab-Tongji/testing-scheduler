FROM python:2.7
MAINTAINER Leo.C
ENV REPO_DIR /home/testing-scheduler
COPY . .
WORKDIR ${REPO_DIR}/server

RUN pip install -r ./python_modules.txt
EXPOSE 5310
CMD sh -c 'python ./src/rest/router.py'
