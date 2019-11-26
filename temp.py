import pandas as pd
import numpy as np

def get_usr_fans():
    fans = {}
    with open("explore/fans.txt", 'r') as f:
        data = f.read().split('\n')
        for item in data:
            usr = item.split(' ')[0]
            if len(usr) == 0:
                continue
            fan = item.split(' ')[-1]
            fans[usr] = int(fan)

    return fans

def get_class_word_dict():
    """
    得到学校组织
    """
    dict = {}
    with open("findwordpair/twitter_class.txt", encoding='utf-8') as f:
        data = f.read().split('\n')
        for line in data:
            if line.startswith('-'):
                kind = line.replace('-', '')
            else:
                dict[line.lower()] = kind
    return dict

if __name__ == '__main__':
    fans = get_usr_fans()
    groups = get_class_word_dict()
    ranks = dict((k.lower(), v) for k , v in zip(groups.values(), [1]*len(groups)))
    dataset = []
    rank = 1
    for name, fan in sorted(fans.items(), key=lambda x: x[1], reverse=True):
        temp = {"用户名": name,
                "粉丝数总排名": rank,
                "粉丝数": fan,
                "所属团体": groups[name.lower()],
                "所属团体内粉丝数排名": ranks[groups[name.lower()]]}
        ranks[groups[name.lower()]] += 1
        rank += 1
        dataset.append(temp)
    dataset = pd.DataFrame(dataset, columns=['用户名', '粉丝数总排名','粉丝数', '所属团体', '所属团体内粉丝数排名'])
    dataset.to_excel("附件1.xlsx", index=False)