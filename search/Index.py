import os
from .PreprocessFile import *
from .tools import *
import json
def createIndex(directname):
    invertedIndex = {}
    # path = projectpath + directname
    path=r'E:\课件\大三下\信息与知识获取\作业2\\'+directname
    files = os.listdir(path)
    for file in files:
        print("analyzing file: ", file)
        #每个文档的词项 list
        content = preProcess(path + '/' + file)
        if content=='':
            continue
        docId = getDocID(file)

        num = 0 #word在文档中的位置
        for word in content:
            if word[0].isdigit() :
                num += 1
                continue

            if word not in invertedIndex:
                docList = {}
                docList[docId] = [num]
                invertedIndex[word] = docList
            else:
                if docId not in invertedIndex[word]:
                    invertedIndex[word][docId] = [num]
                else:
                    invertedIndex[word][docId].append(num)

            num += 1

    #给倒排索引中的词项排序
    invertedIndex = sortTheDict(invertedIndex)
    #获取词项列表
    wordList = WordList(invertedIndex)

    # printIndex(invertedIndex)

    #将数据写入文件中
    writeToFile(invertedIndex, projectpath + 'invertIndex.json')
    writeToFile(wordList, projectpath + 'wordList.json')


#获取文档名中的文档的id
def getDocID(filename):
    end = filename.find('.')
    docId = filename[0:end]
    return int(docId)

def sortTheDict(dict):
    sdict =  { k:dict[k] for k in sorted(dict.keys())}
    for stem in sdict:
        sdict[stem] = { k:sdict[stem][k] for k in sorted(sdict[stem].keys())}
    return sdict

def printIndex(index):
    for stem in index:
        print(stem)
        for doc in index[stem]:
            print("    " , doc , " : " , index[stem][doc])

def WordList(invertedIndex):
    wordList = []
    for word in invertedIndex.keys():
        wordList.append(word)
    return wordList

def getIndex():
    file = open(projectpath + 'invertIndex.json', 'r')
    indexStr = file.read()
    index = json.JSONDecoder().decode(indexStr)
    return index

def getWordList():
    file = open(projectpath + 'wordList.json', 'r')
    wordStr = file.read()
    wordList = json.JSONDecoder().decode(wordStr)
    return wordList

# createIndex('data')
