from gingerit.gingerit import GingerIt
from bs4 import BeautifulSoup
import urllib3
import re


class SlangCleaner:
    abbr_dict = {}
    def __init__(self):
        self.gingerit = GingerIt()
        self.http = urllib3.PoolManager()

    def clean(self, text):
        # Remove punctuation
        text = re.sub("\p{P}", "", text)

        # Split it into words
        wordList = text.split(" ")

        # Replace slang with correct abbreviation
        for i in range(len(wordList)):
            wordList[i] = self.getAbbr(wordList[i])

        text = " ".join(wordList)
        # run it from grammar correction for one last time
        text = self.gingerit.parse(text)
        return text

    def cleanAll(self, textList):
        cleaned = []
        for text in textList:
            cleaned.append(self.clean(text))
        return cleaned

    # Function to get the Slangs from https://www.noslang.com/dictionary/
    def getAbbr(self, alpha):
        if alpha in SlangCleaner.abbr_dict.keys():
            return SlangCleaner.abbr_dict[alpha]

        r = self.http.request('GET', 'https://www.noslang.com/search/' + alpha)
        soup = BeautifulSoup(r.data, 'html.parser')
        result_abbr = None
        for i in soup.findAll('div', {'class': 'dictionary-word'}):
            abbr = i.find('abbr')['title']
            SlangCleaner.abbr_dict[i.find('span').text[:-2]] = abbr
            if result_abbr is None:
                result_abbr = abbr

        return result_abbr if result_abbr is not None else alpha