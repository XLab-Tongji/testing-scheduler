basepath=$(cd `dirname $0`; pwd)					# get the absolute path of this shell file.
tmppath=$basepath/tmp_files
docker_tmppath=/root/build_dir

#build the gradle project in a temp container.
mkdir -p $tmppath
docker build -t leoc/conductor -f $basepath/Dockerfile $basepath
docker run -d --name conductor-builder leoc/condcutor tail -f /dev/null
docker cp  conductor-builder:$docker_tmppath $tmppath/
docker rm -f conductor-builder
#docker rmi leoc/conductor

#build the images of conductor.
cd $tmppath/docker
docker-compose build
