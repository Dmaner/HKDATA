from nltk.corpus import stopwords
from nltk import stem
import nltk
import pandas as pd
import re
import string
from tqdm import tqdm
import numpy as np
import os

time_begin = "2019-6-1 0:00:00"

remove = str.maketrans('', '', string.punctuation)
lan = stem.SnowballStemmer('english')
stopword = stopwords.words('english')
newlist = ['us', '‘', '’', '“', '”']
stopword.extend(newlist)


def loadtext(filename):
    sample = pd.read_excel(filename)
    name = sample["screen_name"][0]
    # remove retweets
    sample = sample[pd.isna(sample['RTed'])]
    # remove earlier than 2019/6/1
    sample = sample[sample['created_at'] >= pd.datetime(2019, 6, 1)]
    text = sample['text']
    # TODO:词性还原

    return text


def preprocess(word):
    word = word.lower()
    # remove @ and http
    pattern = re.compile(r'(http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+)|'
                             r'(?<=^|(?<=[^a-zA-Z0-9-_\.]))@([A-Za-z]+[A-Za-z0-9]+)')
    word = re.sub(pattern, '', word)
    # remove , . ?
    word = word.translate(remove)
    word = nltk.word_tokenize(word)
    # remove a, the...
    word = [w for w in word if not w in stopword and not w.isdigit()]
    # change word
    # word = [lan.stem(w) for w in word]
    return word


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
    with open(filename+".txt", 'w+') as f:
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


if __name__ == '__main__':
    process_dir = "wordget/enprocess"
    data_dir = "wordget/en"
    if not os.path.exists(process_dir):
        os.mkdir(process_dir)
    for dir in os.listdir(data_dir):
        tweet_dir = os.path.join(data_dir, dir)
        tweet = loadtext(tweet_dir)
        nickname = dir.split('-')[1]
        print("load user {}".format(nickname))

        save_path = os.path.join(process_dir, nickname)
        main(tweet, nickname, save_path)