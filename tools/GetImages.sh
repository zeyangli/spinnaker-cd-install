#!/bin/bash

S_REGISTRY="gcr.io/spinnaker-marketplace"
#T_REGISTRY="registry.cn-beijing.aliyuncs.com/spinnaker-cd"
T_REGISTRY="docker.io/spinnakercd"
NODES="node01.zy.com node02.zy.com"

## 下载镜像
function GetImages(){
    echo -e "\033[43;34m =====GetImg===== \033[0m"

    IMAGES=$( cat tagfile.txt)

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
