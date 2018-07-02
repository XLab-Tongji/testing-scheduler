FROM python:2.7
MAINTAINER Leo.C
ENV REPO_DIR /home/testing-scheduler
WORKDIR ${REPO_DIR}
COPY ./server .
RUN pip install -r ./python_modules.txt
EXPOSE 5310
CMD sh -c 'python ./src/rest/router.py'
