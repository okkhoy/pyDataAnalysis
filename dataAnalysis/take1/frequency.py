import sys
import json
import string
import re

scores = {}
punctMinusAt = "!$%&\'()*+,-./:;<=>?\#[\]^_`{|}~\""
englishStopwords = re.compile(r'\b(' + r'|'.join(['rt', 'i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', 'her', 'hers', 'herself', 'it', 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', 'should', 'now'])+ r')\b\s*')
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

unscoredWords = {}
allTweets = {}
allWords = {}

def cleanTweet(sentence):
    # remove new lines in the tweet
    #cleanedSentence = tweet.replace("\n", " ")
    # remove urls in the tweet
    cleanedSentence = re.sub(r"http\S+", " ", sentence.lower())
    # remove emojis # this may not be used 'cos i m converting to ascii string anyway
    cleanedSentence = emoji_UCS2.sub("", cleanedSentence)
    cleanedSentence = emoji_UCS4.sub("", cleanedSentence)
    # remove stopwords
    #cleanedSentence = englishStopwords.sub("", cleanedSentence)
    # remove direct message to /reply to twitter handles handle
    cleanedSentence = re.sub("@\S+", "", cleanedSentence)
    # remove all punctuation marks
    cleanedSentence = cleanedSentence.translate(string.maketrans("",""), punctMinusAt)

    # finally return the list of words in the tweet
    return [i for i in cleanedSentence.split() if len(i) > 1]

def scoreTerms(fp):
    for tweet in fp.readlines():
        score = 0
        jsonTweetObject = json.loads(tweet)
        try:
            tweetText = jsonTweetObject["text"].encode('ascii', 'ignore') # as against 'utf-8'
            tweetText = cleanTweet(tweetText)
            #print tweetText
            for word in tweetText:
                if word not in allWords:
                    allWords[word] = 1
                else:
                    allWords[word] = allWords[word] + 1
            allTweets[jsonTweetObject["id_str"]] = [tweetText, score]
        except KeyError:
            pass


def main():
    tweet_file = open(sys.argv[1])
    scoreTerms(tweet_file)
    totalWords = sum(allWords.itervalues())
    for word in allWords:
        print word, float(allWords[word])/totalWords
    #print "total word count:", totalWords



if __name__ == '__main__':
    main()
