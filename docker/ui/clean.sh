group="x-lab"
ui_image="$group/testing-scheduler:ui"				# ui image name
ui_container="t-scheduler-ui"						# ui container name
sudo docker rm -f $ui_container
sudo docker rmi $ui_image
basepath=$(cd `dirname $0`; pwd)					# get the absolute path of this shell file.
rm -rf $basepath/dist