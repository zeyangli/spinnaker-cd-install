# Spinnaker Installation Manual

![Spinnaker Pre Install](https://github.com/zeyangli/spinnaker-cd-install/workflows/Spinnaker%20Pre%20Install/badge.svg?branch=master)

目前spinnaker的安装大都采用halyard部署，也有两种版本。一种使用halyard，另外一种是使用helm job（其实也是用的halyard）。
使用halyard安装部署非常简单，如果您的网络允许部署起立更快！

![acr-images](acr.png)


## 采用halyard部署（代理方式）

```

```



## halyard-bom-install

使用halyard安装配置spinnaker，无需设置代理。（bom方式）这种方式会启动一个docker容器（halyard）执行任务。

```
├── bom-yaml-1.19.4.tar.gz   ## bom所需的yaml文件
├── halyard.sh               ## halyard初始化配置发布脚本
├── halyard.yaml             ## halyard 配置文件
├── ingress.yaml             ## spinnaker部署访问入口
└── install.sh               ## 安装脚本

```

注意编辑install.sh 调整部署变量值。 然后 sh -x install.sh allinstall .


## helm-bom-install

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
使用github actions 自动化获取版本文件，获取gcr.io镜像然后更名上传到阿里云仓库中。最后会生成一个制品`version-image-script`，里面包含镜像tag文件和下载镜像的脚本。
(图片如果加载不出来，可以直接在Actions中查看最新的流水线中获取哦)
 ![artifacts-images](docs/artifacts.png)

然后手动获取服务版本分支中的配置文件，最后手动发布。







------
以上内容简单记录，后续再进一步整理完善。目前此版本仅限于学习研究使用，避免生产环境使用。

The Bill of Materials (BOM) ：https://spinnaker.io/guides/operator/custom-boms/
https://spinnaker.io/community/releases/versions/  获取最新稳定版本



