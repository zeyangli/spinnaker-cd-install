# Spinnaker Installation Manual

![Spinnaker Pre Install](https://github.com/zeyangli/spinnaker-cd-install/workflows/Spinnaker%20Pre%20Install/badge.svg?branch=master)

目前spinnaker的安装大都采用halyard部署，也有两种版本。一种使用halyard，另外一种是使用helm job（其实也是用的halyard）。
使用halyard安装部署非常简单，如果您的网络允许部署起立更快！

![acr-images](acr.png)

已同步更新docker.io。  


## 安装说明(最新)

- 提前部署好S3存储（可以使用minio，提前部署好，注意更新tools/halyard.sh文件）

```
## Storage 配置基于minio搭建的S3存储
hal config storage s3 edit \
        --endpoint http://minio.idevops.site \
        --access-key-id AKIAIOSFODNN7EXAMPLE \
        --secret-access-key wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY \
        --bucket spinnaker \
        --path-style-access true --no-validate
hal config storage edit --type s3 --no-validate
```

- 如需自定义spinnaker域名，可以修改tools/halyard.sh

```
DECK_HOST="http://spinnaker.idevops.site"
GATE_HOST="http://spin-gate.idevops.site"
```


在[actions](https://github.com/zeyangli/spinnaker-cd-install/actions) 中获取最新的版本部署脚本文件(代码库中已保存1.26.7版本的安装脚本文件)。
将该文件上传到配置好了kubectl客户端的节点中。

```
unzip 1.23.6-Install-Script.zip  && cd 1.23.6
[root@master 1.23.6]# ls
GetImages.sh  halyard.sh  halyard.yaml  ingress.yaml  install.sh  tagfile.txt
[root@master 1.23.6]# tree
.
├── GetImages.sh     ## 可单独执行，遍历tagfile.txt进行镜像下载。
├── halyard.sh       ## Halyard初始化配置脚本。
├── halyard.yaml     ## Halyard容器方式部署时的配置文件。
├── ingress.yaml     ## Spinnaker 部署后的Ingress模板文件。
├── install.sh       ## Spinnaker 部署脚本。
└── tagfile.txt      ## 镜像标签文件（该文件的形成取决于bom版本文件中的定义，具体可以看actions过程）

0 directories, 6 files
```

在每个k8s node节点下载spinnaker部署时需要的docker镜像， 然后安装spinnaker。

```
[root@master 1.23.6]# sh install.sh
 [getimg -> install -> ingress = allinstall]

sh install.sh getimg    ## 下载镜像（提前配置好各node节点的免密）
sh install.sh install   ## 安装spinnaker
sh install.sh ingress   ## 创建ingress

```
验证pod运行状态

```
[root@master 1.23.6]# kubectl get pod -n spinnaker
NAME                                READY   STATUS    RESTARTS   AGE
spin-clouddriver-65c656b665-v9qgg   0/1     Running   0          36s
spin-deck-c74b79594-vbp2l           1/1     Running   0          34s
spin-echo-56bbbbd648-bj2ss          0/1     Running   0          36s
spin-front50-54894dd569-6p89d       0/1     Running   0          31s
spin-gate-5798654745-4fzkw          0/1     Running   0          35s
spin-igor-68f6bfdcbc-zbhcq          0/1     Running   0          33s
spin-orca-5547d664b8-pj8tw          0/1     Running   0          32s
spin-redis-6d85585fd7-d6jzx         1/1     Running   0          34s
spin-rosco-56c56bb968-vmfr8         0/1     Running   0          31s
```



## halyard-bom-install（demo）

使用halyard安装配置spinnaker，无需设置代理。（bom方式）这种方式会启动一个docker容器（halyard）执行任务。

```
├── bom-yaml-1.19.4.tar.gz   ## bom所需的yaml文件
├── halyard.sh               ## halyard初始化配置发布脚本
├── halyard.yaml             ## halyard 配置文件
├── ingress.yaml             ## spinnaker部署访问入口
└── install.sh               ## 安装脚本

```

注意编辑install.sh 调整部署变量值。 然后 sh -x install.sh allinstall .


## helm-bom-install[废弃]

其实是一个helm chart，已经对values做了修改。这种方式会启动一个pod（halyard）执行任务。

```
sh getimages.sh  ## 获取阿里云镜像
kubectl create ns spinnaker 
cd helm-bom-install
kubectl create -f pvc.yaml -n spinnaker       ## 注意修改pv类型，这里使用的nfs
kubectl create -f ingress.yaml -n spinnaker   ## 注意修改Ingress Host

helm install spinnaker -n spinnaker ./spinnaker  ## 部署
kubectl get pod -n spinnaker 

```

## Spinnaker版本更新
注意：现在已经在actions中配置ci，大部分步骤都是自动完成的。需要提前将您当前spinnaker版本的boms文件（~/.hal/.boms）打包上传到代理库updates目录中哦！

使用github actions 自动化获取版本文件，获取gcr.io镜像然后更名上传到阿里云仓库中。最后会生成一个制品`version-install-script`，里面包含镜像tag文件和下载镜像的脚本。
(图片如果加载不出来，可以直接在Actions中查看最新的流水线中获取哦)
 ![artifacts-images](docs/artifacts.png)

然后手动获取服务版本分支中的配置文件，（此步骤已经在ci中实现，无需手动，直接下载actions制品即可）


最后手动发布。

```
unzip 1.19.14-Image-Script.zip
cd 1.19.14

rm -fr ~/.hal/.boms/
mv .boms/ ~/.hal/
chmod 777 -R ~/.hal/*
 
docker exec -it halyard bash
hal config version edit --version local:1.19.14 --no-validate
hal deploy apply --no-validate
```

回滚
```
hal config version edit --version local:1.19.4 --no-validate
hal deploy apply --no-validate
```






------
以上内容简单记录，后续再进一步整理完善。目前此版本仅限于学习研究使用，避免生产环境使用。

The Bill of Materials (BOM) ：https://spinnaker.io/guides/operator/custom-boms/
https://spinnaker.io/community/releases/versions/  获取最新稳定版本



