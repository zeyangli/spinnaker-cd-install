# Spinnaker Installation Manual


目前spinnaker的安装大都采用halyard部署，也有两种版本。一种使用halyard，另外一种是使用helm job（其实也是用的halyard）。
使用halyard安装部署非常简单，如果您的网络允许部署起立更快！

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


以上内容简单记录，后续再进一步整理完善。目前此版本仅限于学习研究使用，避免生产环境使用。




