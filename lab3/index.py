import nltk
from collections import defaultdict


class Index:
    def __init__(self, tokenizer, stemmer=None, stopwords=None):
        self.tokenizer = tokenizer
        self.stemmer = stemmer
        self.index = defaultdict(list)
        self.documents = {}
        self.__unique_id = 0
        if not stopwords:
            self.stopwords = set()
        else:
            self.stopwords = set(stopwords)

    def lookup(self, word):
        word = word.lower()
        results = None
        for token in [t.lower() for t in nltk.word_tokenize(word)]:
            if token in self.stopwords:
                continue

            if self.stemmer:
                token = self.stemmer.stem(token)
            token_search_res = set([self.documents.get(id, None) for id in self.index.get(token)])
            if results is None:
                results = token_search_res
            else:
                results = results.intersection(token_search_res)
        return results

    def add(self, url, document):
        for token in [t.lower() for t in nltk.word_tokenize(document)]:
            if token in self.stopwords:
                continue

            if self.stemmer:
                token = self.stemmer.stem(token)

            if self.__unique_id not in self.index[token]:
                self.index[token].append(self.__unique_id)

        self.documents[self.__unique_id] = url
        self.__unique_id += 1
