# -*- coding: utf-8 -*-
# @Author: 刘威
# @Date:   2020-05-13 17:53:18
# @Last Modified by:   刘威
# @Last Modified time: 2020-05-14 12:57:49
import os
import json
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
from nltk import word_tokenize, pos_tag

def preProcess(filename):
    file = open(filename,'r')
    a = json.loads(file.readline())
    if not a['Headline'][0] or not a['Article_Body'][0]:
        return ''
    content=a['Headline'][0]+' '+a['Article_Body'][0]
    words = lemmatize_sentence(content,False)
    return words



def get_wordnet_pos(treebank_tag):
    if treebank_tag.startswith('J'):
        return wordnet.ADJ
    elif treebank_tag.startswith('V'):
        return wordnet.VERB
    elif treebank_tag.startswith('N'):
        return wordnet.NOUN
    elif treebank_tag.startswith('R'):
        return wordnet.ADV
    else:
        return None

deleteSignal = [',','.',';','&',':','>',"'",'`','(',')','+','!','*','"','?','~','@','#','$','%','-','\'','\"']
deleteSignalForInput = [',','.',';','&',':','>',"'",'`','+','!','*','"','?']

def lemmatize_sentence(sentence,forinput):
    res = []
    result = []
    lemmatizer = WordNetLemmatizer()
    for word, pos in pos_tag(word_tokenize(sentence)):
        # print(word,pos)
        wordnet_pos = get_wordnet_pos(pos) or wordnet.NOUN
        res.append(lemmatizer.lemmatize(word, pos=wordnet_pos))

    for word in res:
        #如果是 's什么的，直接排除
        if word[0] is '\'':
            continue
        flag=0
        #去除标点符号
        if not forinput:
            for c in word:
                if not c.isalpha():
                    flag=1
                    break
        else:
            for c in deleteSignalForInput:
                word = word.replace(c,'')
        if flag:
            continue
        #排除空的字符串
        if len(word) is 0 or word[0] is '-':
            continue

        #如果分解的单词中有/,则将其中的每个单词添加到结果中
        if word.find('/') > 0:
            rs = word.split('/')
            for w in rs:
                w = getWord(w)
                result.append(w)
        else:
            word = getWord(word)
            result.append(word)

    return result

def getWord(word):
    if word.istitle():
        word = word.lower()
        word = WordNetLemmatizer().lemmatize(word, pos='n')
    else:
        word = WordNetLemmatizer().lemmatize(word, pos='n')
    return word
