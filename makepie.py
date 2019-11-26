import plotly as py
import plotly.graph_objs as go
import os

DIR1 = 'wordget/enprocess'
DIR2 = 'wordget/zhprocess'
DIR3 = 'wordget/groupprocess'
DIR4 = 'wordget/all'

topnumber = 20

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

def getthedict(filename):
    dict = {}
    total = 0
    cout = 0
    with open(filename, 'r', encoding='utf-8') as f:
        data = f.read().split('\n')
        for line in data:
            if line.startswith("关键字"):
                cout += 1
                if cout > topnumber:
                    break
                word = line.split()[1]
                times = line.split()[-1]
                total += int(times)
            elif line.startswith("高联系词对"):
                relates = dict.get(word, [times])
                relates.append(line.split()[1])
                dict[word] = relates
    return dict, total

def process(path):
    fans = get_usr_fans()
    d, t = getthedict(path)
    name = path.split('\\')[-1].replace('.txt', '')

    pyplt = py.offline.plot

    labels = []
    values = []
    for w, info in d.items():
        head = "词："+w + "<br>联系词: "+', '.join(info[1:])
        times = int(info[0])
        labels.append(head)
        values.append(times)
    if len(labels) < 2:
        print("not enough")
        print(name)
        return

    fan = fans.get(name, 0)
    trace = [go.Pie(labels=labels, values=values)]
    layout = go.Layout(
        title=name if fan == 0 else name+"粉丝数({})".format(fan),
    )
    fig = go.Figure(data=trace, layout=layout)
    pyplt(fig, filename='finalchart/{}.html'.format(name), auto_open=False)

if __name__ == '__main__':
    for dir in [DIR1, DIR2, DIR3, DIR4]:
        for d in os.listdir(dir):
            path = os.path.join(dir, d)
            print(path)
            process(path)