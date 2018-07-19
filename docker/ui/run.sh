conductor_network='docker_default'
group="x-lab"
ui_image="$group/testing-scheduler:ui"				# ui image name
ui_container="t-scheduler-ui"						# ui container name
docker run -d -p 5311:5311 --net=$conductor_network --name $ui_container $ui_image 