import yaml
import sys
import os 

filePath = sys.argv[1]
tagFile = sys.argv[2]
bomDir = sys.argv[3]
gitRepo = "https://raw.githubusercontent.com/spinnaker"


print("======>Get Yaml Data<=======")
file = open(filePath, 'r', encoding="utf-8")
fileData = file.read()
file.close()

print("======>Yaml To Dict<=======")
data = yaml.load(fileData)
print(data['services'])

print("======> Service Name <======")
serviceData = data['services']
print(serviceData.keys())

print("======> Get Tag <======")
os.system("rm -fr " + tagFile)
for s in serviceData.keys():
    if  s not in  ["defaultArtifact","monitoring-third-party","monitoring-daemon"]:
      print(s + ":" + serviceData[s]['version'])
      tag = s + ":" + serviceData[s]['version']
      f = open(tagFile, 'a')
      f.write(tag + "\n")
      f.close()


### 生成 服务配置文件
os.system("mkdir -p %s" %(bomDir))
for s in serviceData.keys():
    if  s not in  ["defaultArtifact","monitoring-third-party","monitoring-daemon"]:
        serviceVersion = serviceData[s]['version']
        tag = "version-" + serviceVersion.split("-")[0]
        print(s  + ">>>>===GitHub Tag Version===>>>>" + tag)

        ## 创建一个服务目录
        createDirCmd = "mkdir -p %s/%s/%s" %(bomDir, s, serviceVersion )
        os.system(createDirCmd)
 
        ## deck配置文件为settings.js,其他服务为yaml。
        if s == "deck":
            serviceFile="settings.js"
        else:
            serviceFile="%s.yaml" %(s)

        ## 下载服务配置文件，放到服务目录下
        cmd1 = "curl %s/%s/%s/halconfig/%s -o %s/%s/%s" %(gitRepo, s, tag, serviceFile, bomDir, s, serviceFile )
        os.system(cmd1)

        ## 复制服务配置文件，放到服务版本目录下
        cmd2 = "cp %s/%s/%s %s/%s/%s/%s" %(bomDir, s, serviceFile, bomDir,  s, serviceVersion, serviceFile )
        os.system(cmd2)

        if s == "rosco":
            os.system("git clone --branch %s https://github.com/spinnaker/rosco.git " %(tag))
            os.system("cp -r rosco/halconfig/* %s/%s/" %(bomDir, s))
            os.system("cp -r rosco/halconfig/* %s/%s/%s/" %(bomDir, s, serviceVersion))

        ## 检查文件
        os.system("ls %s/%s" %(bomDir, s ))
        os.system("ls %s/%s/%s" %(bomDir, s, serviceVersion ))
