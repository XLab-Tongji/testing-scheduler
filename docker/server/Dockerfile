FROM python:2.7
MAINTAINER x-lab/Leo
WORKDIR /home/testing-scheduler/server
COPY ./server .

RUN pip install -r ./python_modules.txt
EXPOSE 5310
EXPOSE 5312
EXPOSE 5313
CMD sh -c 'python ./src/rest/router.py & python ./src/rest/test_service_demo.py & python ./service_plugins/loop_service/loop_service/flask/router_2.py'
