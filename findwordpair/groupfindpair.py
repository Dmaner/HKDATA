import os

DIR1 = '../wordget/enprocess'
DIR2 = '../wordget/zhprocess'

class WORD:
    def __init__(self, name):
        self.name = name
        self.times = 0
        self.relations = {}
        self.temp = 0

    def appeartimes(self, times):
        self.times += times
        self.temp = times

    def add_relate_words(self, word, value):
        v = value * self.temp
        v += self.relations.get(word, 0)
        self.relations[word] = v

    def top5(self):
        temp = []
        for word, _ in sorted(self.relations.items(), key=lambda x:x[1], reverse=True)[:5]:
            temp.append(word)
        return temp

    def __repr__(self):
        return self.name


def get_class_word_dict():
    """
    得到学校组织
    """
    dict = {}
    with open("twitter_class.txt", encoding='utf-8') as f:
        data = f.read().split('\n')
        for line in data:
            if line.startswith('-'):
                kind = line.replace('-', '')
            else:
                dict[line.lower()] = kind
    return dict

def wirtedict(dictionary):
    for group, words in dictionary.items():
        with open("../wordget/groupprocess/{}.txt".format(group),'w+', encoding='utf-8') as f:
            head = "发文者：{}\n"
            f.write(head.format(group))
            for word, word_class in sorted(words.items(), key=lambda x:x[1].times, reverse=True)[:20]:
                msg = "关键字: {:<12} 出现次数: {}\n"
                f.write(msg.format(word, word_class.times))
                for w in word_class.top5():
                    msg = "高联系词对: {:<12}\n"
                    f.write(msg.format(w))


def main():
    group_dict = get_class_word_dict()
    print(group_dict)
    dict = {}
    for DIR in [DIR1, DIR2]:
        for dir in os.listdir(DIR):
            path = os.path.join(DIR, dir)
            with open(path,'r',encoding='utf-8') as f:
                # 读取文件头
                name = f.readline().split()[1].lower()
                if not name in group_dict:
                    print(name)
                    continue
                group = group_dict[name]
                words = dict.get(group, {})
                data = f.read().split('\n')
                for i, line in enumerate(data):
                    if line.startswith("关键字"):
                        if i != 0:
                            words[keyword] = word
                        keyword = line.split()[1]
                        appeartimes = int(line.split()[-1])
                        word = words.get(keyword, WORD(keyword))
                        word.appeartimes(appeartimes)
                    elif line.startswith("高联系词对"):
                        text = line.split()[1]
                        value = float(line.split()[-1].replace("联系值:", ""))
                        word.add_relate_words(text, value)
                    else:
                        print("!!!")
                        words[keyword] = word
                dict[group] = words
            print("Finish "+path)
    wirtedict(dict)

if __name__ == '__main__':
    main()