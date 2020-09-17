
## minio install

如果从头配置来部署可以参考步骤[1,2,3]
如果你想使用当前仓库中的minio ，直接下载代码，然后运行部署[2,3]


## 0.准备一个pv

我这里用的nfs，可按需修改哦。

```
kind: PersistentVolume
apiVersion: v1
metadata:
  name: ci-minio-pv
  namespace: devops
spec:
  accessModes:
    - ReadWriteOnce
  capacity:
    storage: 50Gi
  persistentVolumeReclaimPolicy: Retain
  storageClassName: manual
  nfs:
    path: /data/devops/minio-data
    server: 192.168.1.200



kubectl create -f pv.yaml

```

## 1.获取最新minio charts

```
helm search repo stable/minio
helm fetch stable/minio --version 5.0.33

tar xf xxxx.tar
vim minio/values.yaml

```

## 2.替换values.yaml内容

我已经替换好了哦，大家需要按需修改pvc配置和ingress访问配置，其他配置也可以自定义。



```yaml
configPathmc: "/root/.mc/"


#pvc
persistence:
  enabled: true
  storageClass: "manual"
  VolumeName: "ci-minio-pv"
  accessMode: ReadWriteOnce
  size: 50Gi

#ingress
ingress:
  enabled: true
  labels: {}
    # node-role.kubernetes.io/ingress: platform

  annotations:
    kubernetes.io/ingress.class: nginx
  path: /
  hosts:
    - minio.idevops.site
  tls: []
```

## 3.部署
```
helm install minio -n devops ./minio
```
