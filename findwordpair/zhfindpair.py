import jieba
import re
import pandas as pd
from langconv import *
import logging
from tqdm import tqdm
import numpy as np
import os
import time

# 防止jieba打印日志
jieba.setLogLevel(logging.INFO)

def getstopwords():
    with open("../stopwords-zh/中文停用词表.txt", 'r', encoding='utf-8') as f:
        stops = f.read()
        return stops.split('\n')

def loadtxt(filename):
    # 筛选特定文本
    sample = pd.read_excel(filename)
    sample = sample[sample["RTed"].isna()]
    sample.reset_index()
    sample = sample[sample['created_at'] >= pd.datetime(2019, 6, 1)]
    text = sample["text"]

    return text


def preprocess(text):
    text = format_str(text)

    # 繁体到简体
    text = converter.convert(text)

    # 分词
    cut_words = list(jieba.cut(text))

    # 除去停用词
    clean_text = [w for w in cut_words if not w in stopwords]
    return clean_text



def pmi(dicts, doc):
    relate = []
    r_dicts = {}
    total = len(doc)
    words = dicts.keys()
    for w1 in tqdm(words):
        p1 = dicts[w1] / total
        for w2 in words:
            if w1 is w2:
                continue
            else:
                p2 = dicts[w2] / total
                p3 = cal_pxy(w1, w2, doc) / total
                if p3 == 0:
                    continue
                r = f(p1, p2, p3)
                relate.append((w2, r))
        r_dicts[w1] = sorted(relate, key=lambda item:item[1], reverse=True)[:10]
        relate = []
    return r_dicts


def cal_pxy(w1, w2, docs):
    pair = {w1, w2}
    appear = 0
    for item in docs:
        word = item
        if pair.issubset(set(word)):
            appear += 1
    return appear


def f(px, py, pxy):
    return np.log(pxy/(px*py))


def writemss(filename, sorteddict, r_dicts, name, text):
    with open(filename+".txt", 'w+', encoding='utf-8') as f:
        f.write("发文者: {:^18} 从2019/6/1所发推文数: {}\n".format(name, len(text)))
        for w, times in sorteddict.items():
            f.write("关键字: {:<12} 出现次数: {}\n".format(w, times))
            for rw, v in r_dicts[w][:5]:
                f.write("高联系词对: {:<12} 联系值:{:.2f}\n".format(rw, v))


def main(text, user, dir):
    dicts = {}
    prewords = []
    for word in tqdm(text):
        word = preprocess(word)
        prewords.append(word)
        for w in word:
            dicts[w] = dicts.get(w, 0) + 1
    sorteddict = dict(sorted(dicts.items(), key=lambda item:item[1], reverse=True)[:50])
    r_dicts = pmi(sorteddict, prewords)
    writemss(dir, sorteddict, r_dicts, user, text)


def format_str(sentence):
    pattern1 = r'\[.*?\]'
    pattern2 = re.compile(r'[^\u4e00-\u9fa5]')
    line1 = re.sub(pattern1, '', sentence)
    line2 = re.sub(pattern2, '', line1)
    new_sentence = ''.join(line2.split())  # 去除空白
    return new_sentence


if __name__ == '__main__':
    converter = Converter("zh-hans")
    stopwords = getstopwords()
    newlist = ['月', '日', '想', '😂😂😂']
    stopwords.extend(newlist)
    process_dir = "../wordget/zhprocess"
    data_dir = "../wordget/zh"
    if not os.path.exists(process_dir):
        os.mkdir(process_dir)
    for dir in os.listdir(data_dir):
        tweet_dir = os.path.join(data_dir, dir)
        tweet = loadtxt(tweet_dir)
        nickname = dir.split('-')[1]
        print("load user {}".format(nickname))
        time.sleep(0.1)
        save_path = os.path.join(process_dir, nickname)
        main(tweet, nickname, save_path)