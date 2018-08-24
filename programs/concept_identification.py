import wikipedia
import difflib
from nltk.tag.stanford import NERTagger
import nltk
import re
import wiki_distribution as wd
class node_info:
    def __init__(self):
        self.similiar=[]
        self.child={}
redundant=[]
def loose_match(s1,s2):
    seq = difflib.SequenceMatcher()
    try:
        seq.set_seqs(s1, s2)
        d=seq.ratio()*100
        d=int(d)
        return d
    except:
        return 0
"""def loose_match1(s1,s2):
    if s1<s2:
        x=len(s1)
        x=x*0.6
        x=(int)(x)
        st=s1[0:x]
        if st in s2:
            return True
    elif s2<s1:
        x=len(s1)*0.7
        x=(int)(x)
        st=s2[0:x]
        if st in s1:
            return True
    else:
        seq = difflib.SequenceMatcher()
        try:
            seq.set_seqs(s1, s2)
            d=seq.ratio()*100
            d=int(d)
            if d>=80:
                return True
        except:
            return False
    return False"""        
def clean(ele):
    word=""
    for e in ele:
        if e.isalpha():
            word=word+e
    return word
def wiki_check(cat):
    cat=clean(cat)
    try:
        wiki_text=wikipedia.summary(cat)
        #print wiki_text
        elements=wiki_text.split(" ")
        #print elements
        #cat_distri={}
        count=0
        for e in elements:
            e=e.lower()
            #e=clean(e)
            #print e            
            for ele in main_cat:
                #print ele
                if loose_match(ele,e)>=80:
                #if loose_match1(ele,e):
                    count=count+1
                    if cat_distri.has_key(ele):
                        cat_distri[ele]=cat_distri[ele]+1
                    else:
                        cat_distri[ele]=1
    
        
    except:
        print "no result"

main_cat={}
m_path='D://Thesis//data//exported_data//main_category.txt'
f3=open(m_path,'r')
x=f3.readlines()
for cat in x:
    cat=cat.rstrip("\n")
    cat=cat.lower()
    #print cat
    #node=node_info()
    main_cat[cat]=1
#print main_cat



cat_distri={}
"""sample="Italy's Fognini-Bolelli win Australian Open men's doubles title"
sentences = nltk.sent_tokenize(sample)
tokenized_sentences = [nltk.word_tokenize(sentence) for sentence in sentences]
tagged_sentences = [nltk.pos_tag(sentence) for sentence in tokenized_sentences]
print tagged_sentences
entity_n=[]
for e in tagged_sentences:
    namedEnt=nltk.ne_chunk(e,binary=True)
    entity_n = [' '.join([y[0] for y in x.leaves()]) for x in namedEnt.subtrees() if x.label() == "NE"]
    print entity_n

for en in entity_n:
    #print en
    wiki_check(en)
    print wd.wiki_relations(en)
for s in tagged_sentences:
    #print 'hello'
    for ele in s:
        #if ele[1]=='NN' or ele[1]=='NNS' or ele[1].startswith('J'):
        if ele[1].startswith('NN') or ele[1].startswith('J'):
            print ele[0].encode('utf-8')
            wiki_check(ele[0]) """
wiki_check('infrastructure')

count=sum(cat_distri.values())
for c in cat_distri:
        x=cat_distri[c]
        x=(float)(x)
        y=(x/count)*100
        print "related to", c,"with",y,"%"   
