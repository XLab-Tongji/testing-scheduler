##############################################################################
# Copyright (c) 2018 Huawei Technologies Co.,Ltd and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

conductor_network='conductor_default'
group="x-lab"
# ui image name
ui_image="$group/test-scheduler:ui"
# ui container name
ui_container="t-scheduler-ui"
# grafana container name
grafana="bottlenecks-grafana"

docker network connect $conductor_network $grafana
docker run -d --rm -p 5311:5311 --net=$conductor_network --name $ui_container $ui_image
