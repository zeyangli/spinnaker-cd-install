
## minio install

```
helm install minio --namespace=devops --set persistence.size=50Gi,persistence.VolumeName=ci-minio-pv,persistence.storageClass=manual ./minio  

```
