# build server docker image
conductor_network='docker_default'

#sudo docker build -t tmp/server -f ./server/Dockerfile  ../
#sudo docker run -d --name tmp-server tmp/server
#sudo docker network connect docker_default tmp-server

# build ui docker image
sudo docker build -t tmp/ui -f ./ui/Dockerfile ../
sudo docker run -d --name tmp-ui tmp/ui
sudo docker network connect docker_default tmp-ui
