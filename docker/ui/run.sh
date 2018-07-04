conductor_network='docker_default'
ui_image='leoc/testing-scheduler:ui'				# ui image name
ui_container='t-scheduler-ui'						# ui container name

sudo docker run -d -p 5311:5311 --name $ui_container $ui_image
sudo docker network connect $conductor_network $ui_container