import yaml
import sys
import os 

filePath = sys.argv[1]
tagFile = sys.argv[2]


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
    if s not in  ["defaultArtifact","monitoring-third-party","monitoring-daemon"]:
      print(s + ":" + serviceData[s]['version'])
      tag = s + ":" + serviceData[s]['version']
      f = open(tagFile, 'a')
      f.write(tag + "\n")
      f.close()
