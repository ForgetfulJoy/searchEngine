import queue
import os
from .tools import *
import re
from nltk.corpus import wordnet


def searchOneWord(index, word):
    if word not in index:
        return []
    else:
        # 将所有文档id变为数字
        docList = [int(key) for key in index[word].keys()]
        # 将文档的id排序
        docList.sort()
        return docList


# 将所有word的结果取并，即所有包含这些word的文档
def searchWords(index, words):
    if len(words) == 0:
        return []
    docQueue = queue.Queue()
    # print(wordset)
    for word in words:
        docQueue.put(searchOneWord(index, word))
    while docQueue.qsize() > 1:
        list1 = docQueue.get()
        list2 = docQueue.get()
        list3 = list(set(list1 + list2))
        list3.sort()
        docQueue.put(list3)

    list3 = docQueue.get()
    return list3


def searchPhrase(index, words, inputList):
    if len(words) == 0:
        return []
    docQueue = queue.Queue()
    for word in words:
        docQueue.put(searchOneWord(index, word))

    while docQueue.qsize() > 1:
        list1 = docQueue.get()
        list2 = docQueue.get()
        docQueue.put(andTwoList(list1, list2))
    doclist = docQueue.get()

    resultList = {}

    if len(inputList) == 1:
        for doc in doclist:
            resultList[doc] = index[inputList[0]][str(doc)]
        return resultList

    # print(doclist)
    for docid in doclist:
        docid = str(docid)
        locList = []
        x = index[inputList[0]][docid]
        for loc in index[inputList[0]][docid]:
            # print(index[inputList[0]][docid])
            floc = loc
            n = len(inputList)
            hasFind = True
            for word in inputList[1:n]:
                floc += 1
                try:
                    # print(index[word][docid])
                    index[word][docid].index(floc)
                except:
                    hasFind = False
                    break
            if hasFind:
                locList.append(loc)
        if len(locList) > 0:
            resultList[docid] = locList
    return resultList



def wildcardSearch(statement,index,wordList):
    words = statement.split(' ')
    #print(words)
    forSearchList = []

    for word in words:
        rset = searchBasedOnWildcard(word,wordList)
        if len(rset) > 0:
            forSearchList.append(rset)
        else:
            print(word,"doesn't find matching words in these articles.")
            return []

    i = 0
    numList = []
    N = len(forSearchList)
    while i < N:
        numList.append(0)
        i += 1

    resultList = {}

    while 1:
        searchList = []
        statement = ""
        j = 0
        while j < N:
            searchList.append(forSearchList[j][numList[j]])
            statement += searchList[j] + " "
            j += 1

        docList = searchPhrase(index,set(searchList),searchList)

        resultList[statement] = docList
        if len(docList) > 0:
            print(statement, ":")
            print("    DocList: ", docList)

        j = 0
        while j < N:
            if numList[j] < len(forSearchList[j]) - 1:
                numList[j] += 1
                m = 0
                while m < j:
                    numList[m] = 0
                    m += 1

                break
            j += 1

        if j >= N:
            break

    return resultList


def wildcard2regex(wildcard):
    regex = '^'
    for i in range(wildcard.__len__()):
        if(i == 0):
            if (wildcard[i] == '*'):
                regex = regex + '[a-z]*'
            elif (wildcard[i] == '?'):
                regex = regex + '[a-z]'
            elif (not wildcard[i].isalpha()):
                return None
            else:
                regex = regex + wildcard[i]
        else:
            if(wildcard[i] == '*'):
                regex = regex + '[a-z]*'
            elif (wildcard[i] == '?'):
                regex = regex + '[a-z]'
            elif (not wildcard[i].isalpha()):
                return None
            else:
                regex = regex + wildcard[i]
    regex = regex + '$'
    return regex

'''
e.g.
ret = searchBasedOnWildcard('f*bility', ['feasability', 'family', 'hello', 'flexibility'])
print(ret)

show: {'feasability', 'flexiblility'}
'''
def searchBasedOnWildcard(wildcard, wordList):
    result = []
    regex = wildcard2regex(wildcard)
    if(regex == None):
        return result
    pattern = re.compile(regex, flags=re.IGNORECASE)
    for word in wordList:
        if(pattern.match(word)):
            result.append(word)
            # print(word)
    return result
        
def getSynonyms(index,word):
    stem = word.lower()
    result = [[word]]
    for synset in wordnet.synsets(stem):
        for lemma in synset.lemmas():
            if lemma.name() != stem:
                wordlist = lemma.name().split('_')
                result.append(wordlist)
    return result

def searchSynonymsWord(index,word):
    wordlist = getSynonyms(index,word)
    resultList = {}

    for phraseList in wordlist:
        #print(phraseList)
        wordset =set(phraseList)
        list = searchPhrase(index,wordset,phraseList)
        phrase = ''
        for w in phraseList:
            phrase += w + " "
        if len(list) > 0:
            print(phrase, ":")
            print("    ",list)
            resultList[phrase] = list

    return resultList





def andTwoList(list1,list2):
    rlist = []
    len1 = len(list1)
    len2 = len(list2)
    n1 = 0
    n2 = 0
    while n1 < len1 and n2 < len2:
        if list1[n1] < list2[n2]:
            n1 += 1
        elif list1[n1] > list2[n2]:
            n2 += 1
        else:
            rlist.append(list1[n1])
            n1 += 1
            n2 += 1
    return rlist

#list1中不包含list2的
def listNotcontain(list1,list2):
    rlist = []
    len1 = len(list1)
    len2 = len(list2)
    n1 = 0
    n2 = 0
    while n1 < len1 and n2 < len2:
        if list1[n1] < list2[n2]:
            rlist.append(list1[n1])
            n1 += 1
        elif list1[n1] > list2[n2]:
            n2 += 1
        else:
            n1 += 1
            n2 += 1
    return rlist
