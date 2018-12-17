sudo docker rm -f t-scheduler-server \
                  t-scheduler-ui \
                  conductor_conductor-server_1 \
                  conductor_conductor-ui_1 \
                  conductor_dynomite_1 \
                  conductor_elasticsearch_1

sudo docker network rm conductor_default
