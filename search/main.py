import os
# from .tools import *
# from .Index import *

import nltk
from .PreprocessFile import *
from .spell import *
# from .getScore import *
# from .searchWord import *
from .sortDoc import *
import json

from .helper import *
from .CreatIndex import *
from .corrector import *
from .search import *
from .Rank import *
from collections import Counter

words = getFile('Words')
INDEX = getFile('Index')
vector = getFile('vector')
LD = getFile('LD')

nfiles = nfiles


# #下载需要的依赖文件,第一次运行时下载  后续运行时注释掉
# nltk.download("wordnet")
# nltk.download("averaged_perceptron_tagger")
# nltk.download("punkt")
# nltk.download("maxnet_treebank_pos_tagger")


def VSM(Query):
    QueryWords = getStem(Query)
    QueryWords = correct(QueryWords)
    wordset = Counter(QueryWords)
    docs = getDocList(INDEX, wordset)
    phDocs = getPhraseDocList(INDEX, wordset, QueryWords)
    rankDocs = getSortedDoc(INDEX, nfiles, wordset, docs, phDocs, vector)
    newdocs = []
    docIds = []
    scores = []
    for doc in rankDocs:
        with open("data/" + doc[1].__str__() + ".json", 'r') as d:
            newdocs.append(json.loads(d.read()))
        docIds.append(doc[1])
        scores.append(doc[0])
    # for doc in rankDocs:
    #     print("doc ID: ", doc[1], " score: ", "%.4f" % doc[0])
    newdocs = DOCproc(list(zip(newdocs, docIds)))
    return list(zip(newdocs,docIds,scores))

def BM25(Query):
    QueryWords = getStem(Query)
    QueryWords = correct(QueryWords)

    wordset = Counter(QueryWords)

    docs = getDocList(INDEX, wordset)
    rankDocs = sortScoreDocList_BM25(INDEX, nfiles, wordset, docs, AVG_L, LD)
    newdocs = []
    docIds = []
    scores = []
    for doc in rankDocs:
        with open("data/" + doc[1].__str__() + ".json", 'r') as d:
            newdocs.append(json.loads(d.read()))
        docIds.append(doc[1])
        scores.append(doc[0])
    # for doc in rankDocs:
    #     print("doc ID: ", doc[1], " score: ", "%.4f" % doc[0])

    newdocs = DOCproc(list(zip(newdocs, docIds)))
    return list(zip(newdocs, docIds, scores))

#返回所有匹配的结果，SORTEDDOCLIST[i][0]表示分数，SORTEDDOCLIST[i][1]表示文档id
# def overall(statement):
#     INPUTWORDS = lemmatize_sentence(statement, True)
#     print(INPUTWORDS)
#     INPUTWORDS = correctSentence(INPUTWORDS)
#     print(INPUTWORDS)
#
#     WORDSET = set(INPUTWORDS)
#
#     DOCLIST = searchWords(INDEX, WORDSET)
#     # 卡在sort处
#     SORTEDDOCLIST = sortScoreDocList(INDEX, FILENUM, WORDSET, DOCLIST)
#     docs=[]
#     docIds=[]
#     scores=[]
#     for doc in SORTEDDOCLIST:
#         with open("data/"+doc[1].__str__()+".json",'r') as d:
#             docs.append(json.loads(d.read()))
#         docIds.append(doc[1])
#         scores.append(doc[0])
#         # print("doc ID: ", doc[1], " score: ", "%.4f" % doc[0])
#     #adjust(WORDSET)
#     docs=DOCproc(list(zip(docs,docIds)))
#     return list(zip(docs,docIds,scores))
# def adjust(wordset):
#     with open('adjust.txt', 'a', encoding='utf-8') as f:
#         for word in wordset:
#             f.write(word + ' ' + str(docName) + ' ' + operate + '\n')

def DOCproc(keyDoc):
    newDoc=[]
    for doc,id in keyDoc:
        # print(id)
        ndoc={}
        ndoc['Url']=doc['Url'][0]
        ndoc['FirstPublishDate']=doc['FirstPublishDate'][0]
        ndoc['Headline']=doc['Headline'][0]
        ndoc['Article_Body']=doc['Article_Body'][0]
        if doc['MappedSection'] != False:
            ndoc['MappedSection']=doc['MappedSection'][0]
        else:
            ndoc['MappedSection']="None"
        newDoc.append(ndoc)
    return newDoc

# def phrase(statement):
#     INPUTWORDS = lemmatize_sentence(statement, True)
#     INPUTWORDS = correctSentence(INPUTWORDS)
#
#     WORDSET = set(INPUTWORDS)
#
#     PHRASEDOCLIST = searchPhrase(INDEX, WORDSET, INPUTWORDS)
#     docs=[]
#     docIds=[]
#     if 0 == len(PHRASEDOCLIST):
#         print("Doesn't find \"", INPUTWORDS, '"')
#         return []
#     else:
#         # TODO PHRASEDOCLIST 的location代表啥？
#         for key in PHRASEDOCLIST:
#             with open("data/" + key.__str__() + ".json", 'r') as d:
#                 docs.append(json.loads(d.read()))
#             docIds.append(key)
#             # print('    location: ', PHRASEDOCLIST[key])
#             # print('docID: ', key, "   num: ", len(PHRASEDOCLIST[key]))
#     return list(zip(docs,docIds))
def phrase(Query):
    QueryWords = getStem(Query)
    QueryWords = correct(QueryWords)

    wordset = Counter(QueryWords)

    phDocs = searchsortPhrase(INDEX, wordset, QueryWords)
    if 0 == len(phDocs):
        print("Doesn't find \"", QueryWords, '"')
    else:
        newdocs = []
        docIds = []
        for doc in phDocs:
            with open("data/" + doc[0].__str__() + ".json", 'r') as d:
                newdocs.append(json.loads(d.read()))
            docIds.append(doc[0])
        newdocs = DOCproc(list(zip(newdocs, docIds)))
        return list(zip(newdocs, docIds))
        # for item in phDocs:
        #     print('docName: ', item[0], "   num: ", len(item[1]))
        #     print('    location: ', item[1])




def getDoc(keyWord,sortKind):
    statement = keyWord
    #查询排序
    if sortKind == '0':
        return VSM(statement)
    elif sortKind == '1':
        return BM25(statement)
    # 近义词查询
    elif sortKind == '4':
        return phrase(statement)
    else:
        print("choice error")
        return []

