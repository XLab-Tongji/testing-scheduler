# build server docker image
conductor_network='docker_default'
server_image='leoc/testing-scheduler:server'  		# server image name
server_container='t-scheduler-server'           	# server container name
ui_image='leoc/testing-scheduler:ui'		   		# ui image name
ui_container='t-scheduler-ui'					   	# ui container name

sudo docker build -t $server_image -f ./server/Dockerfile  ../
sudo docker run -d -p 5310:5310 --name $server_container $server_image
sudo docker network connect $conductor_network $server_container

# build ui docker image
sudo docker build -t $ui_image -f ./ui/Dockerfile ../
sudo docker run -d -p 5311:5311 -p 5312:5312 --name $ui_container $ui_image
sudo docker network connect $conductor_network $ui_container
