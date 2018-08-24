import wikipedia
from nltk.tag.stanford import NERTagger
import nltk
import re
"""def ner(sample):
    #sample=' '.join(sen.split('-'))
    sentences = nltk.sent_tokenize(sample)
    tokenized_sentences = [nltk.word_tokenize(sentence) for sentence in sentences]
    tagged_sentences = [nltk.pos_tag(sentence) for sentence in tokenized_sentences]
    print tagged_sentences
    #entity_n=[]
    for e in tagged_sentences:
        namedEnt=nltk.ne_chunk(e,binary=True)
        #print namedEnt
        entity_n = [' '.join([y[0] for y in x.leaves()]) for x in namedEnt.subtrees() if x.label() == "NE"]
        print entity_n"""
def ner(sample):
    sentences = nltk.sent_tokenize(sample)
    tokenized_sentences = [nltk.word_tokenize(sentence) for sentence in sentences]
    tagged_sentences = [nltk.pos_tag(sentence) for sentence in tokenized_sentences]
    print tagged_sentences
"""def check_for_special_char(s):
    for i in s:
        if i.isdigit() or i in " ?.!/;:":
            return True
            break
    return False
def check_for_category(cat):
    if len(cat)>4 and len(cat)<20 and check_for_special_char(cat)is not True:
        return True
    else:
        return False
def url_category_list(s):
    print s
    cat_list=[]
    if s[0]=='/':
        sp=s.split('/')[1:]
    else:
        sp=s.split('/')[1:]
        #print sp
    print sp
    for i in range(0,len(sp)):
        y=sp[i].strip('-_,. :').lower()
        if check_for_category(y):
             cat_list.append(y)
        else:
            if len(y)>10:
                ner(y)
    return cat_list"""




ner('Kapil Sharma lives in mumbai')
#element='http://movies.ndtv.com/bollywood/kapil-sharma-will-make-big-screen-debut-with-yash-raj-films-bank-chor-484564?pfrom=home-latest'
#e='/slideshows/5-things-the-pm-said...and-what-he-probably-meant.html'
"""splitted_url=element.split("//")
if len(splitted_url)==2:
     url_category_list(splitted_url[1])
else:
     url_category_list(splitted_url[0])

s='   ---hello_'
print s.strip('-_,. :').lower()"""
