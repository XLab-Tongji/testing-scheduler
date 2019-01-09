basepath=$(cd `dirname $0`; pwd)					# get the absolute path of this shell file.
tmppath=$basepath/tmp_files
docker_tmppath=/home/noroot/build_dir/conductor
group="x-lab"
plugin_image="$group/conductor:builder"
plugin_container="conductor-builder"
#build the gradle project in a temp container.

mkdir -p $tmppath
docker build -t $plugin_image -f $basepath/Dockerfile $basepath
docker run -d --name $plugin_container $plugin_image
docker cp  $plugin_container:$docker_tmppath $tmppath/
docker rm -f $plugin_container
#docker rmi $plugin_image

#repair COPY error
#cd $tmppath/conductor/docker/server
#sed -i "14s/app\/libs/app\/libs\//g" Dockerfile
#cd ..

#repair npm warn
#cd ui
#sed -i "37s/install/install --no-optional --no-shrinkwrap --no-package-lock/g" Dockerfile
#cd ..

#build the images of conductor.
cd $tmppath/conductor/docker
docker-compose build
