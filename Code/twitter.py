import nltk
import re


def stopwords():
    stop_words = nltk.corpus.stopwords.words('english')
    stop_words.extend(['this', 'that', 'the', 'might', 'have', 'been', 'from',
                       'but', 'they', 'will', 'has', 'having', 'had', 'how',
                       'went', 'were', 'why', 'and', 'still', 'his', 'her',
                       'was', 'its', 'per', 'cent', 'a', 'able', 'about', 'am',
                       'across', 'after', 'all', 'almost', 'also', 'among',
                       'an', 'and', 'any', 'are', 'as', 'at', 'be', 'because',
                       'been', 'but', 'by', 'can', 'cannot', 'could', 'dear',
                       'did', 'do', 'does', 'either', 'else', 'ever', 'every',
                       'for', 'from', 'get', 'got', 'had', 'has', 'have', 'he',
                       'her', 'hers', 'him', 'his', 'how', 'however', 'i',
                       'if', 'in', 'into', 'is', 'it', 'its', 'just', 'least',
                       'let', 'like', 'likely', 'may', 'me', 'might', 'most',
                       'must', 'my', 'neither', 'nor', 'not', 'of', 'off',
                       'often', 'on', 'only', 'or', 'other', 'our', 'own',
                       'rather', 'said', 'say', 'says', 'she', 'should',
                       'since', 'so', 'some', 'than', 'that', 'the', 'their',
                       'them', 'then', 'there', 'these', 'they', 'this', 'tis',
                       'to', 'too', 'twas', 'us', 'wants', 'was', 'we', 'were',
                       'what', 'when', 'where', 'which', 'while', 'who',
                       'whom', 'why', 'will', 'with', 'would', 'yet', 'you',
                       'your', 've', 're', 'rt',  'retweet', 'fuck', 'ya',
                       'yall', 'yay', 'youre', 'youve', 'ass', 'factbox',
                       'com', 'lt', 'th', 'retweeting', 'dick', 'fuckin',
                       'shit', 'via', 'fucking', 'shocker', 'wtf', 'hey',
                       'ooh', 'rtamp', 'amp', 'retweet', 'goooooooooo',
                       'hellooo', 'gooo', 'fucks', 'fucka', 'bitch', 'wey',
                       'sooo', 'helloooooo', 'lol', 'smfh'])
    stop_words = set(stop_words)
    return stop_words


def normalize_text(text):
    # try:
    #    text = text.encode('utf-8')
    # except:
    #    pass
    text = re.sub('((www\.[^\s]+)|(https?://[^\s]+)|(pic\.twitter\.com/[^\s]+))', '', text)
    # text = re.sub('@[^\s]+', '', text)
    # text = re.sub('#([^\s]+)', '', text)
    text = re.sub('[:;>?<=*+()/,\-#!$%\{˜|\}\[^_\\@\]1234567890’‘]', ' ', text)
    text = re.sub('[\d]', '', text)
    text = text.replace(".", '')
    text = text.replace("'", ' ')
    text = text.replace("\"", ' ')
    text = text.replace("-", " ")
    text = text.replace("@", "")
    text = text.replace("#", "")
    text = text.replace("…", "")

    # Normalize some utf8 encoding
    text = text.replace("\x9d", ' ').replace("\x8c", ' ').replace("\xa0", ' ')
    text = text.replace("\x9d\x92", ' ')
    text = text.replace("\x9a\xaa\xf0\x9f\x94\xb5", ' ')
    text = text.replace("\xf0\x9f\x91\x8d\x87\xba\xf0\x9f\x87\xb8", ' ')
    text = text.replace("\x9f", ' ').replace("\x91\x8d", ' ')
    text = text.replace("\xf0\x9f\x87\xba\xf0\x9f\x87\xb8", ' ')
    text = text.replace("\xf0", ' ').replace('\xf0x9f', '')
    text = text.replace("\x9f\x91\x8d", ' ').replace("\x87\xba\x87\xb8", ' ')
    text = text.replace("\xe2\x80\x94", ' ').replace("\x9d\xa4", ' ')
    text = text.replace("\x96\x91", ' ')
    text = text.replace("\xe1\x91\xac\xc9\x8c\xce\x90\xc8\xbb\xef\xbb\x89" +
                        "\xd4\xbc\xef\xbb\x89\xc5\xa0\xc5\xa0\xc2\xb8", ' ')
    text = text.replace("\xe2\x80\x99s", " ").replace("\xe2\x80\x98", ' ')
    text = text.replace("\xe2\x80\x99", ' ').replace("\xe2\x80\x9c", " ")
    text = text.replace("\xe2\x80\x9d", " ")
    text = text.replace("\xe2\x82\xac", " ").replace("\xc2\xa3", " ")
    text = text.replace("\xc2\xa0", " ").replace("\xc2\xab", " ")
    text = text.replace("\xf0\x9f\x94\xb4", " ")
    text = text.replace("\xf0\x9f\x87\xba\xf0\x9f\x87\xb8\xf0\x9f", "")
    return text


def nltk_tokenize(text):
    tokens = []
    features = []
    tokens = text.split()
    for word in tokens:
        if word.lower() not in stopwords() and len(word) > 2:
            features.append(word.lower())
    return features


def parse(filename):
    file_object = open(filename, 'r')
    data = {}
    for line in file_object:
        username, text = line.split('\t\t')
#        print(text)
        text = normalize_text(str(text))
        features = nltk_tokenize(text)
        if username not in data:
            data[username] = []
        data[username].append(features)
    return data


def main():
    data = parse('tweets.txt')
    print(data)


if __name__ == "__main__":
    # execute only if run as a script
    main()
