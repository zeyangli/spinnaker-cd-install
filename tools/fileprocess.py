import yaml
import sys
import os 


class SpinnakerToDo(object):
    
    def __init__(self):
        self.filePath = sys.argv[1]
        self.tagFile = sys.argv[2]
        self.bomDir = sys.argv[3]
        self.gitRepo = "https://raw.githubusercontent.com/spinnaker"
        #self.exceptServices = ["defaultArtifact","monitoring-third-party","monitoring-daemon"]
        self.exceptServices = ["defaultArtifact","monitoring-third-party"]


    ## 读取yaml文件
    def GetYamlData(self):
        print("======> get yaml data <======")
        file = open(self.filePath, 'r', encoding="utf-8")
        fileData = file.read()
        file.close()
        ## 转换dict
        data = yaml.load(fileData)
        print(data['services'])
        serviceData = data['services']
        print(serviceData.keys())

        return serviceData
    
    ## 生成镜像tag文件
    def CreateTagFile(self):
        print("======> Get Tag <======")
        os.system("rm -fr " + self.tagFile)

        serviceData = self.GetYamlData()
        for s in serviceData.keys():
            if  s not in  self.exceptServices : 
                print(s + ":" + serviceData[s]['version'])
                tag = s + ":" + serviceData[s]['version']
                f = open(self.tagFile, 'a')
                f.write(tag + "\n")
                f.close()

    ## 生成服务配置文件（首先用户会将当前版本的bom文件打包上传到updates目录中）
    def CreateServiceConf(self):
        serviceData = self.GetYamlData()
        for s in serviceData.keys():
            if  s not in  self.exceptServices :
                serviceVersion = serviceData[s]['version']
                tag = "version-" + serviceVersion.split("-")[0]
                print(s  + ">>>>===GitHub Tag Version===>>>>" + tag)
                ## 创建一个服务目录
                createDirCmd = "mkdir -p %s/%s/%s" %(self.bomDir, s, serviceVersion )
                os.system(createDirCmd)
                ## deck配置文件为settings.js,其他服务为yml。
                if s == "deck":
                    serviceFile="settings.js"
                else:
                    serviceFile="%s.yml" %(s)
                    
                ## 监控程序
                if s == "monitoring-daemon":
                    serviceFile = 'spinnaker-monitoring.yml'
                    ## 下载服务配置文件，放到服务目录下
                    ## https://raw.githubusercontent.com/spinnaker/spinnaker-monitoring/version-0.18.1/spinnaker-monitoring-daemon/halconfig/spinnaker-monitoring.yml
                    cmd1 = "curl %s/%s/%s/spinnaker-monitoring-daemon/halconfig/%s -o %s/%s/%s" %(self.gitRepo, 'spinnaker-monitoring', tag, serviceFile, self.bomDir, s, serviceFile )
                    os.system(cmd1)
                    cmd2 = "cp %s/%s/%s %s/%s/%s/%s" %(self.bomDir, s, serviceFile, self.bomDir,  s, serviceVersion, serviceFile )
                    os.system(cmd2)
                else :
                    ## 下载服务配置文件，放到服务目录下
                    cmd1 = "curl %s/%s/%s/halconfig/%s -o %s/%s/%s" %(self.gitRepo, s, tag, serviceFile, self.bomDir, s, serviceFile )
                    os.system(cmd1)
                    ## 复制服务配置文件，放到服务版本目录下
                    cmd2 = "cp %s/%s/%s %s/%s/%s/%s" %(self.bomDir, s, serviceFile, self.bomDir,  s, serviceVersion, serviceFile )
                    os.system(cmd2)
                    ## rosco服务需要额外下载几个目录(images.yml packer)
                    if s == "rosco":
                        os.system("git clone --branch %s https://github.com/spinnaker/rosco.git " %(tag))
                        os.system("cp -r rosco/halconfig/* %s/%s/" %(self.bomDir, s))
                        os.system("cp -r rosco/halconfig/* %s/%s/%s/" %(self.bomDir, s, serviceVersion))

                    ## 检查文件
                    os.system("ls %s/%s" %(self.bomDir, s ))
                    os.system("ls %s/%s/%s" %(self.bomDir, s, serviceVersion ))
    
    ## 更新bom版本文件中的版本号为local:
    def UpdateBomVersionFile(self):
        print("======> write yaml data <======")
        file = open(self.filePath, 'r', encoding="utf-8")
        fileData = file.read()
        file.close()
        data = yaml.load(fileData)
        #serviceData = self.GetYamlData()
        for s in data['services'].keys():
            if s != "defaultArtifact" :
                serviceVersion = data['services'][s]['version']
                data['services'][s]['version'] = "local:" + serviceVersion
        
        
        data = yaml.dump(data)
        print(data)
        os.system("rm -fr " + self.filePath)
        f = open(self.filePath, 'a')
        f.write(data)
        f.close()

    def main(self):
        self.CreateTagFile()
        self.CreateServiceConf()
        self.UpdateBomVersionFile()



if __name__ == '__main__':
    sp = SpinnakerToDo()
    sp.main()
