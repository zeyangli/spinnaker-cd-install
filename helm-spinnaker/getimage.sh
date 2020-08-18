#!/bin/bash

VERSION="1.19.4"
S_REGISTRY="gcr.io/spinnaker-marketplace"
T_REGISTRY="registry.cn-beijing.aliyuncs.com/spinnaker-cd"
NODES="node01.zy.com node02.zy.com"

## 下载镜像
function GetImages(){
    echo -e "\033[43;34m =====GetImg===== \033[0m"
    #gcr.io/spinnaker-marketplace/gate:1.15.1-20200403040016
    #gcr.io/spinnaker-marketplace/front50:0.22.1-20200401121252
    #gcr.io/spinnaker-marketplace/igor:1.9.2-20200401121252
    #gcr.io/spinnaker-marketplace/echo:2.11.2-20200401121252
    #gcr.io/spinnaker-marketplace/deck:3.0.2-20200324040016
    #gcr.io/spinnaker-marketplace/halyard:1.32.0
    #gcr.io/spinnaker-marketplace/clouddriver:6.7.3-20200401190525
    #gcr.io/spinnaker-marketplace/orca:2.13.2-20200401144746
    #gcr.io/spinnaker-marketplace/rosco:0.18.1-20200401121252

    IMAGES="gate:1.15.1-20200403040016\
    front50:0.22.1-20200401121252\
    igor:1.9.2-20200401121252\
    echo:2.11.2-20200401121252\
    deck:3.0.2-20200324040016\
    halyard:1.32.0\
    clouddriver:6.7.3-20200401190525\
    orca:2.13.2-20200401144746\
    rosco:0.18.1-20200401121252"

    for image in ${IMAGES}
    do
        for node in ${NODES}
        do 
           echo  -e "\033[32m ${node} ---> pull ---> ${image} \033[0m"
           ssh ${node} "docker pull ${T_REGISTRY}/${image}"
           echo  -e "\033[32m ${node} ---> tag ---> ${image} \033[0m"
           ssh ${node} "docker tag ${T_REGISTRY}/${image} ${S_REGISTRY}/${image}"
        done
    done
    for node in ${NODES}
    do
       echo -e "\033[43;34m =====${node}===镜像信息===== \033[0m"
       ssh ${node} "docker images | grep 'spinnaker-marketplace' "
    done
    
}

GetImages
