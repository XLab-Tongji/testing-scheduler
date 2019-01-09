sudo docker rm -f t-scheduler-server \
                  t-scheduler-ui \
                  conductor_conductor-server_1 \
                  conductor_conductor-ui_1 \
                  conductor_dynomite_1 \
                  conductor_elasticsearch_1

sudo docker network rm conductor_default

basepath=$(cd `dirname $0`; pwd)					# get the absolute path of this shell file.

cd plugin
sudo rm -r tmp_files

echo "--- Clean Finished ---"
