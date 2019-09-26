from gingerit.gingerit import GingerIt
from bs4 import BeautifulSoup
import urllib3
import re
import string
import json
if __name__ == "__main__":
    alphabet = ["a", "b", "c", "d", "e", "f", "g", "h", "j", "k", "l", "m", "n", "o", "p", "r", "q", "s", "t", "u", "v", "w", "x", "y", "z", "i"]
    slang_dict = {}

    http = urllib3.PoolManager()
    for i in alphabet:
        print("Working on", i)
        r = http.request('GET', 'https://www.noslang.com/dictionary/' + i)
        soup = BeautifulSoup(r.data, 'html.parser')
        abbr_list = soup.findAll('div', {'class': 'dictionary-word'})

        for a in abbr_list:
            abbr = a.find('abbr')['title']
            slang_dict[a.find('span').text[:-2]] = abbr


    print("size:",len(slang_dict.keys()))
    print(json.dumps(slang_dict))