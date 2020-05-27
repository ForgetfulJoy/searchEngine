# -*- coding: utf-8 -*-
# @Author: 刘威
# @Date:   2020-05-13 17:57:28
# @Last Modified by:   刘威
# @Last Modified time: 2020-05-14 12:19:40
import json
import os
projectpath = os.getcwd()
#projectpath = projectpath.replace('/',"\\")
# projectpath += "\\"
projectpath +='/'
datapath=projectpath+'data'
print("projectpath:",projectpath)
print("Reuters path",datapath)

def writeToFile(item,filename):
    # 将数据写入到文件中
    file = open(filename,'w')
    str = json.JSONEncoder().encode(item)
    file.write(str)
    file.close()

#获取文档名中的文档的id
def getDocID(filename):
    end = filename.find('.')
    docId = filename[0:end]
    return int(docId)

def getWholeDocList():
    print("data is"+datapath)
    files = os.listdir(datapath)
    fileList = []
    for file in files:
        fileList.append(getDocID(file))
    return sorted(fileList)

print("getting file list...")
wholeDocList = getWholeDocList()