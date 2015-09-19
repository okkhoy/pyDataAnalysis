import sys
import json
import string
import re
import operator

states = {
        'AK': 'Alaska',
        'AL': 'Alabama',
        'AR': 'Arkansas',
        'AS': 'American Samoa',
        'AZ': 'Arizona',
        'CA': 'California',
        'CO': 'Colorado',
        'CT': 'Connecticut',
        'DC': 'District of Columbia',
        'DE': 'Delaware',
        'FL': 'Florida',
        'GA': 'Georgia',
        'GU': 'Guam',
        'HI': 'Hawaii',
        'IA': 'Iowa',
        'ID': 'Idaho',
        'IL': 'Illinois',
        'IN': 'Indiana',
        'KS': 'Kansas',
        'KY': 'Kentucky',
        'LA': 'Louisiana',
        'MA': 'Massachusetts',
        'MD': 'Maryland',
        'ME': 'Maine',
        'MI': 'Michigan',
        'MN': 'Minnesota',
        'MO': 'Missouri',
        'MP': 'Northern Mariana Islands',
        'MS': 'Mississippi',
        'MT': 'Montana',
        'NA': 'National',
        'NC': 'North Carolina',
        'ND': 'North Dakota',
        'NE': 'Nebraska',
        'NH': 'New Hampshire',
        'NJ': 'New Jersey',
        'NM': 'New Mexico',
        'NV': 'Nevada',
        'NY': 'New York',
        'OH': 'Ohio',
        'OK': 'Oklahoma',
        'OR': 'Oregon',
        'PA': 'Pennsylvania',
        'PR': 'Puerto Rico',
        'RI': 'Rhode Island',
        'SC': 'South Carolina',
        'SD': 'South Dakota',
        'TN': 'Tennessee',
        'TX': 'Texas',
        'UT': 'Utah',
        'VA': 'Virginia',
        'VI': 'Virgin Islands',
        'VT': 'Vermont',
        'WA': 'Washington',
        'WI': 'Wisconsin',
        'WV': 'West Virginia',
        'WY': 'Wyoming'
}

# state coordinates are indexed in order: westlimit; southlimit; eastlimit; northlimit
statecoordinates = {
'Alabama':[-88.47,30.19,-84.89,35.01],
'Alaska':[172.4,51.2,-130.0,71.4],
'Arizona':[-114.82,31.33,-109.05,37.0],
'Arkansas':[-94.62,33.0,-89.64,36.5],
'California':[-124.42,32.53,-114.13,42.01],
'Colorado':[-109.06,36.99,-102.04,41.0],
'Connecticut':[-73.7278,40.987,-71.7872,42.0506],
'Delaware':[-75.7891,38.451,-75.0487,39.8395],
'District of Columbia':[-77.11974,38.80315,-76.909393,38.995548],
'Florida':[-87.63,24.52,-80.03,31.0],
'Georgia':[-85.61,30.36,-80.84,35.0],
'Hawaii':[-178.31,18.91,-154.81,28.4],
'Idaho':[-117.24,41.99,-111.04,49.0],
'Illinois':[-91.51,36.97,-87.5,42.51],
'Indiana':[-88.1,37.77,-84.78,41.76],
'Iowa':[-96.64,40.38,-90.14,43.5],
'Kansas':[-102.0518,36.993,-94.5884,40.0045],
'Kentucky':[-89.5715,36.4971,-81.965,39.1475],
'Louisiana':[-94.04,28.93,-88.82,33.02],
'Maine':[-71.08,42.97,-66.95,47.46],
'Maryland':[-79.4877,37.8895,-75.0492,39.723],
'Massachusetts':[-73.5081,41.239,-69.9286,42.8868],
'Michigan':[-90.42,41.7,-82.4,48.2],
'Minnesota':[-97.24,43.5,-89.49,49.38],
'Mississippi':[-91.66,30.17,-88.1,35.0],
'Missouri':[-95.77,36.0,-89.1,40.61],
'Montana':[-116.05,44.36,-104.04,49.0],
'Nebraska':[-104.0535,39.9999,-95.3083,43.0017],
'Nevada':[-120.01,35.0,-114.04,42.0],
'New Hampshire':[-72.5572,42.697,-70.6027,45.3055],
'New Jersey':[-75.5598,38.9286,-73.9024,41.3574],
'New Mexico':[-109.05,31.33,-103.0,37.0],
'New York':[-74.2591,40.4914,-73.7003,40.9153],
'North Carolina':[-84.3219,33.841,-75.46,36.5882],
'North Dakota':[-104.05,45.94,-96.55,49.0],
'Ohio':[-84.82,38.4,-80.52,41.98],
'Oklahoma':[-97.833675,35.290544,-97.12472,35.674752],
'Oregon':[-124.61,41.99,-116.46,46.29],
'Pennsylvania':[-80.5199,39.7198,-74.6895,42.2694],
'Rhode Island':[-71.8923,41.1461,-71.1205,42.0188],
'South Carolina':[-83.3533,32.0346,-78.5408,35.2155],
'South Dakota':[-104.06,42.48,-96.44,45.95],
'Tennessee':[-90.3103,34.9829,-81.6469,36.6781],
'Texas':[-106.65,25.84,-93.51,36.5],
'Utah':[-114.05,37.0,-109.04,42.0],
'Vermont':[-73.4306,42.7268,-71.465,45.0167],
'Virginia':[-83.6754,36.5408,-75.2422,39.466],
'Washington':[-77.11974,38.80315,-76.909393,38.995548],
'West Virginia':[-82.64,37.2,-77.72,40.64],
'Wisconsin':[-92.89,42.49,-86.76,47.08],
'Wyoming':[-111.06,40.99,-104.05,45.01],
}

stateScore = {}

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

def hw():
    print 'Hello, world!'

def lines(fp):
    print str(len(fp.readlines()))

def cleanTweet(sentence):
    # remove new lines in the tweet
    #cleanedSentence = tweet.replace("\n", " ")
    # remove urls in the tweet
    cleanedSentence = re.sub(r"http\S+", " ", sentence.lower())
    # remove emojis # this may not be used 'cos i m converting to ascii string anyway
    cleanedSentence = emoji_UCS2.sub("", cleanedSentence)
    cleanedSentence = emoji_UCS4.sub("", cleanedSentence)
    # remove stopwords
    cleanedSentence = englishStopwords.sub("", cleanedSentence)
    # remove direct message to /reply to twitter handles handle
    cleanedSentence = re.sub("@\S+", "", cleanedSentence)
    # remove all punctuation marks
    cleanedSentence = cleanedSentence.translate(string.maketrans("",""), punctMinusAt)

    # finally return the list of words in the tweet
    return [i for i in cleanedSentence.split() if len(i) > 1]

def findState(coordinates):
    for state in statecoordinates:
        if coordinates[0] > statecoordinates[state][0] and coordinates[0] < statecoordinates[state][2] and\
            coordinates[1] > statecoordinates[state][1] and coordinates[1] < statecoordinates[state][3]:
            return state
    return None


def scoreTweets(fp):
    for tweet in fp.readlines():
        score = 0
        jsonTweetObject = json.loads(tweet)
        try:
            tweetLocation = jsonTweetObject["coordinates"]#.encode('ascii', 'ignore') # as against 'utf-8'
            if tweetLocation is not None:
                state = findState(tweetLocation["coordinates"])
                if state is None:
                    continue
                    #[[[172.4458955,18.9110642],[172.4458955,71.3867745],[-66.9502861,71.3867745],[-66.9502861,18.9110642],[172.4458955,18.9110642]]]
                tweetText = jsonTweetObject["text"].encode('ascii', 'ignore') # as against 'utf-8'
                tweetText = cleanTweet(tweetText)
                #print tweetText
                for word in tweetText:
                    if word in scores:
                        score = score + scores[word]
                    else:
                        unscoredWords[word] = 0

                if state not in stateScore:
                    stateScore[state] = [score, 1]
                else:
                    stateScore[state][0] = (stateScore[state][0] * stateScore[state][1] + score) / 2.0
                    stateScore[state][1] = stateScore[state][1] + 1
                #allTweets[jsonTweetObject["id_str"]] = [tweetText, score]
                #print tweetGeo, tweetLocation
            #allTweets[jsonTweetObject["id_str"]] = [tweetText, score]
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
    #sent_file.seek(0)
    #tweet_file.seek(0)
    loadafinn(sent_file)
    scoreTweets(tweet_file)
    topten = sorted(stateScore.items(), key=operator.itemgetter(1), reverse=True)

    for k in states:
        if states[k] == topten[0][0]:
            print k
    #print allTweets


if __name__ == '__main__':
    main()
