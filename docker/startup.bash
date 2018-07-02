# build server docker image
conductor_network='docker_default'

sudo docker build -t leoc/testing-scheduler:server -f ./server/Dockerfile  ../
sudo docker run -d -p 5310:5310 --name testing-scheduler-server tmp/server
sudo docker network connect docker_default testing-scheduler-server

# build ui docker image
sudo docker build -t leoc/testing-scheduler:ui -f ./ui/Dockerfile ../
sudo docker run -d -p 5311:5311 -p 5312:5312 --name testing-scheduler-ui tmp/ui
sudo docker network connect docker_default testing-scheduler-server
