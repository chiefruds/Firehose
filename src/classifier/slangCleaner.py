from gingerit.gingerit import GingerIt
from bs4 import BeautifulSoup
import urllib3
import re
import string
import json


class SlangCleaner:
    abbr_dict = {}
    def __init__(self):
        self.gingerit = GingerIt()
        self.http = urllib3.PoolManager()
        self.abbr_dict = {}
        with open('/home/mkmeral/Documents/NNHackathon/Firehose/src/classifier/slangList.json') as json_file:
            self.abbr_dict = json.load(json_file)


    def clean(self, text):
        # Remove any mentions, URLs and punctuations
        text = re.sub("(\s)@\w+", " ", text)
        text = re.sub(r"http\S+", "", text)
        text.translate(str.maketrans('', '', string.punctuation))

        # Split it into words
        wordList = text.split(" ")

        # Replace slang with correct abbreviation
        for i in range(len(wordList)):
            wordList[i] = self.getAbbr(wordList[i])

        text = " ".join(wordList)
        # run it from grammar correction for one last time
        # text = self.gingerit.parse(text)
        return text

    def cleanAll(self, textList):
        cleaned = []
        for text in textList:
            cleaned.append(self.clean(text))
        return cleaned

    def getAbbr(self, word):
        if word in self.abbr_dict.keys():
            return self.abbr_dict[word]

        return word

    # Function to get the Slangs from https://www.noslang.com/dictionary/
    # def getAbbr(self, alpha):
    #     if alpha in SlangCleaner.abbr_dict.keys():
    #         return SlangCleaner.abbr_dict[alpha]
    #
    #     r = self.http.request('GET', 'https://www.noslang.com/search/' + alpha)
    #     soup = BeautifulSoup(r.data, 'html.parser')
    #     abbr_list = soup.findAll('div', {'class': 'dictionary-word'})
    #     if abbr_list is None or len(abbr_list) == 0:
    #         return alpha
    #
    #     for i in abbr_list:
    #         if i.find("h3") is not None:
    #             continue
    #         abbr = i.find('abbr')['title']
    #         SlangCleaner.abbr_dict[i.find('span').text[:-2]] = abbr
    #
    #     if alpha in SlangCleaner.abbr_dict.keys():
    #         return SlangCleaner.abbr_dict[alpha]
    #
    #     return alpha

if __name__ == "__main__":
    text = "Some random text with @user and #thisisnow also with http://www.google.com ehe xd"
    parser = SlangCleaner()
    text = parser.clean(text)
    print("Result: ")
    print(text)