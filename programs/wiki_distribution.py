import wikipedia
import nltk
from nltk import word_tokenize
from nltk.util import ngrams
from nltk.corpus import stopwords

def wiki_relations(entity_name):
    required_sentences=[]
    tagged_sentences=[]
    text=wikipedia.summary(entity_name)
    sentence=nltk.sent_tokenize(text)
    token=text.split()
    sixgrams=ngrams(token,6)
    for element in list(sixgrams):
        #count=count+1
        if element[2].encode('utf-8')=='of': #or  element[2].encode('utf-8')=='of':
            #y=list(element)
            x=[]
            for e in element:
                x.append(e.encode('utf-8'))
            s=' '.join(x)
            required_sentences.append(s)
            for sent in sentence:
                if s in sent:
                    tagged_sent=nltk.pos_tag(nltk.word_tokenize(sent))
                    #print tagged_sent
                    required_sentences.append(tagged_sent)
                    #tagged_sentences.append(tagged_sent)
                    break
            #print x
        if element[0].encode('utf-8')=='is' and (element[1].encode('utf-8')=='a'or element[1].encode('utf-8')=='an'):
            x=[]
            for e in element:
                x.append(e.encode('utf-8'))
            s=' '.join(x)
            required_sentences.append(s)
            for sent in sentence:
                if s in sent:
                    tagged_sent=nltk.pos_tag(nltk.word_tokenize(sent))
                    #print tagged_sent
                    required_sentences.append(tagged_sent)
                    #tagged_sentences.append(tagged_sent)
                    break
            #required_sentences.append(s) 
        if element[0].encode('utf-8')=='was' and element[1].encode('utf-8')=='the':
            x=[]
            for e in element:
                x.append(e.encode('utf-8'))
            s=' '.join(x)
            required_sentences.append(s)
            for sent in sentence:
                if s in sent:
                    tagged_sent=nltk.pos_tag(nltk.word_tokenize(sent))
                    #print tagged_sent
                    required_sentences.append(tagged_sent)
                    #tagged_sentences.append(tagged_sent)
                    break
        if element[0].encode('utf-8')=='is' and element[1].encode('utf-8')=='the':
            x=[]
            for e in element:
                x.append(e.encode('utf-8'))
            s=' '.join(x)
            required_sentences.append(s)
            for sent in sentence:
                if s in sent:
                    tagged_sent=nltk.pos_tag(nltk.word_tokenize(sent))
                    #print tagged_sent
                    required_sentences.append(tagged_sent)
                    #tagged_sentences.append(tagged_sent)
                    break
        if element[0].encode('utf-8')=='has' and element[1].encode('utf-8')=='been':
            x=[]
            for e in element:
                x.append(e.encode('utf-8'))
            s=' '.join(x)
            required_sentences.append(s)
            for sent in sentence:
                if s in sent:
                    tagged_sent=nltk.pos_tag(nltk.word_tokenize(sent))
                    #print tagged_sent
                    required_sentences.append(tagged_sent)
                    #tagged_sentences.append(tagged_sent)
                    break
        if len(required_sentences)>10:
                break
        
    return required_sentences
#wiki_relations('Arvind Kejriwal')
while True:
    data=raw_input('Input the category\n')
    try:
        for e in wiki_relations(data):
            print e
    except:
        print 'no result found'
        pass
