##############################################################################
# Copyright (c) 2018 Huawei Technologies Co.,Ltd and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

# get the absolute path of this shell file.
basepath=$(cd `dirname $0`; pwd)
# get the root directory of this project
projectpath=$basepath/../../..
group="x-lab"
# ui image name
ui_image="$group/test-scheduler:ui-builder"
docker build -t $ui_image -f $basepath/Dockerfile $projectpath
