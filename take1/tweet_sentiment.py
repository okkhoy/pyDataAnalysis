import sys
import json
import string
import re

scores = {}
punctMinusHash = "!$%&\'()*+,-./:;<=>?\#[\]^_`{|}~"


def hw():
    print 'Hello, world!'

def lines(fp):
    print str(len(fp.readlines()))

def cleanTweet(tweet):
    cleanedtweet = tweet.replace("\n", " ")
    cleanedtweet = re.sub(r"http\S+", " ", cleanedtweet)
    emoji_UCS4 = re.compile(u'['
        u'\U0001F300-\U0001F64F'
        u'\U0001F680-\U0001F6FF'
        u'\u2600-\u26FF\u2700-\u27BF]+',
        re.UNICODE)
    emoji_UCS2 = re.compile(u'('
        u'\ud83c[\udf00-\udfff]|'
        u'\ud83d[\udc00-\udeff]|'
        u'[\u2600-\u26FF\u2700-\u27BF])+',
        re.UNICODE)

    ecleanedtweet = emoji_UCS2.sub("", cleanedtweet)
    #cleanedtweet = emoji_UCS4.sub(" ", cleanedtweet)
    #cleanedtweet = re.sub(r"http\S+", " ", cleanedtweet)
    return ecleanedtweet.lower().translate(string.maketrans("",""), punctMinusHash)

def readTweets(fp):
    for tweet in fp.readlines()[1:]:
        jsonTweetObject = json.loads(tweet)
        try:
            tweetText = jsonTweetObject["text"].encode('utf-8')
            print cleanTweet(tweetText)
        except KeyError:
            pass

def loadafinn(fp):
    for line in fp:
        term, score = line.split("\t")
        scores[term] = int(score)

def main():
    sent_file = open(sys.argv[1])
    tweet_file = open(sys.argv[2])
    #hw()
    #lines(sent_file)
    #lines(tweet_file)
    loadafinn(sent_file)
    readTweets(tweet_file)
    #readSearchQuery(tweet_file)

if __name__ == '__main__':
    main()
