import pandas as pd
import os
import re
from snownlp import SnowNLP
from tqdm import tqdm
from langid.langid import LanguageIdentifier, model
from textblob import TextBlob
import warnings

warnings.filterwarnings('ignore')

identifier = LanguageIdentifier.from_modelstring(model, norm_probs=True)
bad_list = []


def test(index, data):
    sample = data.loc[index, 'text']
    # print("finish {} text".format(index+1))

    pattern = re.compile(r'(http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+)|'
                         r'(?<=^|(?<=[^a-zA-Z0-9-_\.]))@([A-Za-z]+[A-Za-z0-9]+)')
    # remove url and @
    sample = re.sub(pattern, '', sample)
    if len(sample) == 0:
        return

    lan = identifier.classify(sample)[0]
    try:
        if data.loc[index, "compound"] == 0:
            if lan == 'zh':
                s = SnowNLP(sample)
                score = s.sentiments * 2 - 1
            elif lan == 'en':
                s = TextBlob(sample)
                score = s.sentiment.polarity
            else:
                return
        else:
            return
    except:
        bad_list.append(str(index))
    else:
        data.loc[index, "compound"] = score


def save(name, data):
    id = ["用户名", "发布时间", "点赞数", "转发数", "转发者", "文本", "情感评价"]
    data.reindex(columns=id)
    writer = pd.ExcelWriter(name)
    data.to_excel(writer)
    writer.save()


use_col = ['screen_name', 'created_at', 'fav', 'rt', 'RTed', 'text', 'compound']

if __name__ == '__main__':
    c = os.listdir('../HKDATA/tweets/')
    for item in c:
        filename = item.replace(".xlsx", "")
        data = pd.read_excel('tweets/'+filename+".xlsx")

        data = data.loc[:,use_col]
        for i in tqdm(range(len(data))):
            test(i, data)
        save("analysis/"+filename+"-analysis.xlsx", data)

        with open("bad.txt", 'a+') as f:
            f.write(filename+'\n')
            if len(bad_list) != 0:
                print(bad_list)
                t = " ".join(bad_list) + "\n"
            else:
                t = "None\n"
            f.write(t)

        print("finish "+filename)