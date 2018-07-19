group="x-lab"
server_image="$group/testing-scheduler:server"		# server image name
server_container="t-scheduler-server"				# server container name

sudo docker rm -f $server_container
sudo docker rmi $server_image