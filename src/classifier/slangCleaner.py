from gingerit.gingerit import GingerIt
import urllib3
import re
import string
import json


class SlangCleaner:
    abbr_dict = {}

    def __init__(self, slang_file: str = "resources/slangList.json"):
        self.gingerit = GingerIt()
        self.http = urllib3.PoolManager()
        self.abbr_dict = {}
        with open(slang_file) as json_file:
            self.abbr_dict = json.load(json_file)

    def clean(self, text):
        # Remove any mentions, URLs and punctuations
        text = re.sub("@\w+", " ", text)
        text = re.sub(r"http\S+", "", text)
        text = text.translate(str.maketrans('', '', string.punctuation))
        text = re.sub("\s+", " ", text)
        # Split it into words
        wordList = text.split(" ")

        # Replace slang with correct abbreviation
        for i in range(len(wordList)):
            abbr = self.getAbbr(wordList[i]).split(" ")
            for word in abbr:
                wordList.append(word)

        # text = " ".join(wordList)
        # run it from grammar correction for one last time
        # text = self.gingerit.parse(text)
        return wordList

    def cleanAll(self, textList):
        cleaned = []
        for text in textList:
            cleaned.append(self.clean(text))
        return cleaned

    def getAbbr(self, word):
        if word in self.abbr_dict.keys():
            return self.abbr_dict[word]

        return word


if __name__ == "__main__":
    text = "Some random text with @user and #thisisnow also with http://www.google.com ehe xd"
    parser = SlangCleaner()
    text = parser.clean(text)
    print("Result: ")
    print(text)
