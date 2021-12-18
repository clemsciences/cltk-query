# cltk-query

This package is used to query `Word` in a [CLTK](https://github.com/cltk/cltk) `Doc`.


````python
from cltk import NLP
from cltk.core.data_types import Word
from cltk_query import Query
non_nlp = NLP("non", suppress_banner=True)
doc = non_nlp.analyze("ek er armr")
q = Query(doc)
word_query = Word(string="er")
r = q.filter(word_query)
print(r.total)
print(r.matches[0].string)
print(r.matches[0].index_token)
print(r.doc.tokens)
````
