conductor_network='docker_default'
server_image='leoc/testing-scheduler:server'		# server image name
server_container='t-scheduler-server'				# server container name

sudo docker run -d -p 5310:5310 --name $server_container $server_image
sudo docker network connect $conductor_network $server_container