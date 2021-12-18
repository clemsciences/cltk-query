from typing import Union, List, Dict

from cltk.core import Doc, Word
from boltons.cacheutils import cachedproperty


__author__ = "Clément Besnier <clem@clementbesnier.fr>"


class QueryResults:
    """

    """

    def __init__(self):
        self.matches: Dict[Doc, List[Union[Word, List[Word]]]] = {}

    def __add__(self, other):
        if isinstance(other, QueryResult):
            qrs = QueryResults()
            qrs.matches = self.matches
            qrs.matches[other.doc] = other.matches
            return qrs

        elif isinstance(other, QueryResults):
            qrs = QueryResults()
            qrs.matches.update(self.matches)
            qrs.matches.update(other.matches)
            return qrs
        else:
            raise ValueError()

    @cachedproperty
    def matches(self):
        matches = []
        for key in self.matches:
            matches.extend(self.matches[key])
        return matches

    def __setitem__(self, key: Doc, value: List[Union[Word, List[Word]]]):
        self.matches[key] = value

    def __getitem__(self, item: Doc):
        return self.matches[item]


class QueryResult:
    """
    """
    def __init__(self, doc: Doc):
        self.matches = []
        self.doc = doc

    def add_match(self, match: Union[Word, List[Word]]):
        self.matches.append(match)

    @cachedproperty
    def total(self):
        return len(self.matches)

    def __add__(self, other):
        if isinstance(other, QueryResult):
            qrs = QueryResults()
            qrs[self.doc] = self.matches
            qrs[other.doc] = other.matches
            return qrs
        else:
            raise ValueError()


class Query:
    """
    >>> from cltk import NLP
    >>> non_nlp = NLP("non", suppress_banner=True)
    >>> doc = non_nlp.analyze("ek er armr")
    >>> q = Query(doc)
    >>> from cltk.core.data_types import Word
    >>> word_query = Word(string="er")
    >>> r = q.filter(word_query)
    >>> r.total
    1
    >>> r.matches[0].string
    'er'
    >>> r.matches[0].index_token
    1
    >>> r.doc.tokens
    ['ek', 'er', 'armr']

    """

    def __init__(self,
                 doc: Doc):
        self.doc = doc
        self.word_query = None
        self.result = QueryResult(doc)

    def filter(self, word_query: Union[Word, List[Word]]) -> QueryResult:
        self.word_query = word_query
        if type(word_query) == Word:
            for i, word in enumerate(self.doc.words):
                if self.__class__.compare_words(word, self.word_query):
                    self.result.add_match(word)

        elif type(word_query) == list:
            doc_size = len(self.doc.words)
            query_size = len(word_query)
            for i, word in enumerate(self.doc.words):
                if i + query_size < doc_size:
                    matches = False
                    for j in range(query_size):
                        matches = matches and self.__class__.compare_words(self.doc.words[i+j], self.word_query[j])
                    if matches:
                        self.result.add_match(self.doc.words[i: i+query_size])
        return self.result

    @staticmethod
    def compare_words(doc_word: Word, query_word: Word) -> bool:
        matches = False
        if query_word.pos is not None:
            if doc_word.pos == query_word.pos:
                matches = True
            else:
                return False
        if query_word.lemma is not None:
            if doc_word.lemma == query_word.lemma:
                matches = True
            else:
                return False
        if query_word.string is not None:
            if doc_word.string == query_word.string:
                matches = True
            else:
                return False
        if query_word.phonetic_transcription is not None:
            if doc_word.phonetic_transcription == query_word.phonetic_transcription:
                matches = True
            else:
                return False
        return matches

    @cachedproperty
    def result(self):
        return self.result
