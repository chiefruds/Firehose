import time
from bisect import bisect_left
from slangCleaner import SlangCleaner


class Encoder:
    PADDING = 0
    couldnt_find = []

    def __init__(self, file: str = "resources/dataset/dictionary"):
        self.cleaner = SlangCleaner()
        start = time.time()
        self.index = [""]
        self.count = 1
        with open(file) as dictFile:
            while True:
                word = dictFile.readline().strip('\n')
                if word is None or word == "":
                    break
                if self.count % 5000 == 0:
                    print("Count at", self.count, "with word", word)
                self.index.append(word)
                self.count += 1
        finish = time.time()
        print("Loaded a dictionary with size:", self.count, "in", finish - start, "seconds")

    def binarysearch(self, word: str):
        l = 0
        r = len(self.index) - 1
        while l <= r:

            mid = int(l + (r - l) / 2)

            # Check if x is present at mid
            if self.index[mid] == word:
                return mid

                # If x is greater, ignore left half
            elif self.index[mid] < word:
                l = mid + 1

            # If x is smaller, ignore right half
            else:
                r = mid - 1

        # If we reach here, then the element was not present
        print("Could not find", word)
        Encoder.couldnt_find.append(word)
        return self.count

    def encodelist(self, word_list: list):
        encoded = [0] * 250
        for i in range(len(word_list)):
            word = word_list[i].lower()
            encoded[i] = bisect_left(self.index, word)
        return encoded

    def encode(self, text: str):
        word_list = self.cleaner.clean(text)
        return self.encodelist(word_list)

    def decode(self, encoded: list):
        words = []
        for num in encoded:
            if num != self.count:
                words.append(self.index[num])
            else:
                words.append("<UNKNOWN>")

        return " ".join(words)
