import wikipedia
import difflib
from nltk.tag.stanford import NERTagger
import nltk
import re
def loose_match(s1,s2):
    seq = difflib.SequenceMatcher()
    try:
        seq.set_seqs(s1, s2)
        d=seq.ratio()*100
        d=int(d)
        return d
    except:
        return 0

sample="Xiaomi incurs wrath in China over India map"
sentences = nltk.sent_tokenize(sample)
tokenized_sentences = [nltk.word_tokenize(sentence) for sentence in sentences]
tagged_sentences = [nltk.pos_tag(sentence) for sentence in tokenized_sentences]
#print nltk.ne_chunk(tagged_sentences[0])


for e in tagged_sentences:
    namedEnt=nltk.ne_chunk(e,binary=True)
    np = [' '.join([y[0] for y in x.leaves()]) for x in namedEnt.subtrees() if x.label() == "NE"]
    print np

#extract_entity_names(t)
