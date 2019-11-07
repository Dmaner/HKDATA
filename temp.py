import os

following = 'following'
followers = 'followers'
wordpiar = "wordget/en"
wordpiarzh = "wordget/zh"

names = {}

for dir in os.listdir(wordpiar):
    user = dir.split('-')[1]
    names[user.lower()] = names.get(user.lower(), '') + "tweets"

for dir in os.listdir(wordpiarzh):
    user = dir.split('-')[1]
    names[user.lower()] = names.get(user.lower(), '') + "tweets"

for dir in os.listdir(followers):
    user = dir.split('-')[1]
    names[user.lower()] = " ".join([names.get(user.lower(), ''), "following"])

for dir in os.listdir(followers):
    user = dir.split('-')[1]
    names[user.lower()] = " ".join([names.get(user.lower(), ''), "followers"])

for user, s in names.items():
    print("user: {:<20}  {:20}".format(user, s))